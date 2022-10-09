from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def pter_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://pterclub.com/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    else:
        select_type='403'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择来源 
    if file1.type=='WEB-DL':
        source_sel='5'
    elif 'rip' in file1.type.lower() or file1.type=='bluray'  :
        source_sel='6'
    elif file1.type=='HDTV':
        source_sel='4'
    elif file1.type=='remux':
        source_sel='3'
    else:
        source_sel='6'
    logger.info('已成功选择质量为'+file1.type)
    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            team_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            team_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            team_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            team_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            team_sel='5'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            team_sel='6'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            team_sel='7'
            logger.info('国家信息已选择'+file1.country)
        else:
            team_sel='6'
            logger.info('未找到资源国家信息，已默认日本')
    else:
        team_sel='6'
        logger.info('未找到资源国家信息，已默认日本')


    jinzhuan = 'no'
    guoyu    = 'no'
    zhongzi  = 'no'
    pr       = 'no'
    guanfang = 'no'
    uplver   = 'no'
    if 'audience' in file1.pathinfo.exclusive :
        jinzhuan = 'yes'
    if '国' in file1.language or '中' in file1.language:
        guoyu    = 'yes'
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        zhongzi  = 'yes'
    if file1.transfer==0:
        pr = 'yes'
    if 'PTER' in file1.sub.upper():
        guanfang = 'yes'
    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='yes'

        

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            
    
    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.imdburl,
            "douban": file1.doubanurl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content.replace('[quote=','[hide=').replace('[/quote','[/hide'),
            "type": select_type,
            "source_sel": source_sel,
            "team_sel": team_sel,
            }
    buttomlist=["uplver","jinzhuan","guoyu","zhongzi","pr","guanfang"]
    for item in buttomlist:
        if eval(item+"=='yes'"):
            exec('other_data["'+item+'"]="yes"')
            

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)