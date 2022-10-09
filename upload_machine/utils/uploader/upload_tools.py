from loguru import logger
from qbittorrentapi import Client
import time
import datetime
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import re
import qbittorrentapi
from http.cookies import SimpleCookie


def afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist):
    if r.status_code==200:
        logger.info('已发布成功')
    else:
        logger.warning('发布种子发生错误，错误代码:'+str(r.status_code)+' ,错误信息:'+str(r.reason))
        return False,fileinfo+' 发布种子发生错误，错误代码:'+str(r.status_code)+' ,错误信息:'+str(r.reason)
    String_url =finduploadurl(r)
    downloadurl=finddownloadurl(r)
    if downloadurl=='已存在':
        return True,fileinfo+'种子发布失败,失败原因:种子'+downloadurl+',当前网址:'+String_url
    recordupload(os.path.join(record_path,siteinfo.sitename+'_torrent.csv'),file1,String_url,downloadurl)
    if downloadurl !='':
        res=qbseed(url=downloadurl,filepath=file1.downloadpath,qbinfo=qbinfo,category=file1.pathinfo.category,hashlist=hashlist)
        if res:
            return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+String_url
        else:
            return True,fileinfo+'种子发布成功,但是添加种子失败,请手动添加种子，种子链接:'+downloadurl+',当前网址:'+String_url
    else:
        logger.warning('正在记录错误的请求返回值')
        errorfile=os.path.join(record_path,'errorhtml.html')
        f=open(errorfile,'w', encoding='utf-8')
        f.write(r.text)
        f.close()
        return False,fileinfo+'未找到下载链接,当前网址:'+String_url+' ,请求的返回值已保存至:'+errorfile

def cookies_raw2jar(raw: str) -> dict:
    """
    Arrange Cookies from raw using SimpleCookies
    """
    if not raw:
        raise ValueError("The Cookies is not allowed to be empty.")
    cookie = SimpleCookie(raw)
    return {key: morsel.value for key, morsel in cookie.items()}

def recordupload(torrent_file,file1,String_url,downloadurl):
    logger.info('正在记录发布的资源到'+torrent_file)
    if not os.path.exists(torrent_file):
        if 'win32' in sys.platform:
            f = open(torrent_file,'w+',encoding='utf-8-sig',errors='ignore')
        else:
            f = open(torrent_file,'w+',encoding='utf-8-sig')

        f.write('中文名,集数,发布日期,资源链接,资源下载链接\n0\n')
        f.close()

    if 'win32' in sys.platform:
        with open(torrent_file, 'r',encoding='utf-8-sig',errors='ignore') as f1:
            list1 = f1.readlines()
    else:
        with open(torrent_file, 'r') as f1:
            list1 = f1.readlines()
    while list1[-1].strip()=='':
        a=list1.pop(-1)
        del(a)
    
    try:
        num=int(list1[-1].replace(',','').strip())
        a=list1.pop(-1)
        del(a)
    except:
        num=0
    if len(list1)>0:
        list1[-1]=list1[-1].strip()+'\n'

    now = datetime.datetime.now()

    filestr=''.join(list1)
    newstr=''

    newstr=newstr+file1.chinesename.replace(',',' ')+','
    if not ('anime' in file1.pathinfo.type.lower() or 'tv' in file1.pathinfo.type.lower()) or file1.pathinfo.collection==0:
        newstr=newstr+file1.episodename.zfill(2)+','
    else:
        newstr=newstr+'第'+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)+'集 合集,'
    newstr=newstr+str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+','
    newstr=newstr+str(String_url)+','
    newstr=newstr+str(downloadurl)+'\n'

    logger.debug(newstr)

    filestr=filestr+newstr+str(num+1)+'\n'
    if 'win32' in sys.platform:
        f = open(torrent_file,'w+',encoding='utf-8-sig',errors='ignore')
    else:
        f = open(torrent_file,'w+',encoding='utf-8-sig')
    f.write(filestr)
    f.close()
    logger.info('记录完毕')

def finduploadurl(res):
    logger.info('正在寻找发布页面链接')
    String_url = res.url
    if not('&uploaded' in String_url):
        logger.warning(String_url+'未找到发布页面网址')
        return '未找到发布页面网址'
    String_url =String_url.split('&uploaded')[0]
    return String_url


def finddownloadurl(res):
    logger.info('正在寻找页面下载链接')
    o = urlparse(res.url)
    o = o.scheme+'://'+o.hostname+'/download.php?'
    #白兔特判
    if 'hare' in o:
        link = re.findall('(https://club\.hares\.top/download\.php\?downhash=.*)\</p',res.text)
        if len(link)>0:
            return link[0]
        else:
            if '已存在' in res.text:
                logger.warning('该种子已存在')
                return '已存在'
            logger.warning('未找到下载链接')
            return ''
    #白兔特判结束
    soup = BeautifulSoup(res.text,'lxml')
    for a in soup.find_all('a'):
        link=''
        try:
            link = a['href']
        except:
            logger.warning('该a标签未找到href属性')
        if o in link:
            logger.info('成功获得下载链接'+link)
            return link

    for a in soup.find_all('a'):
        link=''
        try:
            link = a['href']
        except:
            logger.warning('该a标签未找到href属性')
        if len(re.findall(r'download.php\?id=[0-9]+&',link))>0:
            o = urlparse(res.url)
            if link.startswith('download.php'):
                link=o.scheme+'://'+o.hostname+'/'+link
            logger.info('成功获得下载链接'+link)
            return link

    logger.warning('未找到下载链接')
    if '已存在' in res.text:
        logger.warning('该种子已存在')
        return '已存在'
    return ''



def qbseed(url,filepath,qbinfo,is_skip_checking=False,is_paused=True,category=None,hashlist=[]):
    logger.info('正在添加资源到Qbittorrent,请稍等...')

    is_paused=True
    try:
        client = Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
    except:
        logger.warning('Qbittorrent WEBUI登录失败,将种子添加到QB任务失败')
        return False

    logger.info('正在登录Qbittorrent WEBUI')
    try:
        client.auth_log_in()
    except:
        logger.warning('Qbittorrent WEBUI信息错误，登录失败，请检查au.yaml文件里的url、用户名、密码')
        return False
    logger.info('成功登录Qbittorrent WEBUI')
    try:
        tor_num=len(client.torrents_info())
    except Exception as err:
        tor_num=0    
    tor_num_new=tor_num
    trynum=0
    while tor_num_new==tor_num:
        trynum=trynum+1
        if trynum>12:
            logger.warning('添加种子失败,种子下载链接为:'+url+'   请自行手动添加')
            return True
        logger.info('正在第'+str(trynum)+'次添加种子')
        try:
            res=client.torrents_add(urls=url,save_path=filepath,is_skip_checking=is_skip_checking,is_paused=is_paused,use_auto_torrent_management=None,category=category)
        except Exception as r:
            logger.warning('添加种子进入qb出错，错误信息: %s' %(r))
            continue
            #raise ValueError ('添加种子进入qbittorrent出错，程序结束')
        if 'Ok' in res:
            logger.info('返回值显示成功添加种子')
        else:
            logger.warning('添加种子失败，返回值为:'+str(res))
        time.sleep(1)
        try:
            tor_num_new=len(client.torrents_info())
        except Exception as r:
            tor_num_new=tor_num
            logger.warning('计算种子数量出错，错误信息: %s' %(r))
        if tor_num_new==tor_num:
            time.sleep(5)
            try:
                tor_num_new=len(client.torrents_info())
            except Exception as r:
                tor_num_new=tor_num
                logger.warning('计算种子数量出错，错误信息: %s' %(r))

    logger.info('已经成功添加种子')
    addtime=0
    to=None
    try:
        torrentlist=client.torrents.info()
    except Exception as r:
        torrentlist=[]
        logger.warning('获取种子信息出错，错误信息: %s' %(r))
    for item in torrentlist:
        if item.added_on>addtime:
            addtime=item.added_on
            to=item
    if type(to)!=qbittorrentapi.torrents.TorrentDictionary:
        logger.warning('未找到最新的种子')
        return True
    if not to._torrent_hash in hashlist:
        hashlist.append(to._torrent_hash)

    if 'lemonhd' in url:
        logger.info('发现lemonhd的种子,正在更改tracker...')
        for item in to.trackers:
            if 'url' in item and 'leaguehd' in item['url']:
                tracker=item['url']
                if 'http:' in tracker:
                    try:
                        to.edit_tracker(orig_url=tracker,new_url=tracker.replace('http:','https:'))
                    except Exception as r:
                        logger.error('更改tracker失败，原因: %s' %(r))

    return True
