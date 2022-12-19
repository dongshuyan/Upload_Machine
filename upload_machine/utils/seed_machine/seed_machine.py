from loguru import logger
from upload_machine.utils.para_ctrl.readyaml import write_yaml
import os
from upload_machine.utils.pathinfo.pathinfo import findnum
from upload_machine.utils.mediafile.mediafile import mediafile
from upload_machine.utils.uploader.auto_upload import auto_upload
from shutil import move
from qbittorrentapi import Client
import time
import datetime


def get_newhash(qbinfo):
    logger.info('正在查找最新发布的种子的hash...')
    logger.info('正在登录Qbittorrent WEBUI页面...')
    try:
        client = Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
    except Exception as r:
        logger.warning('Qbittorrent WEBUI登录失败，错误信息: %s' %(r))
        logger.warning('获取最新种子hash失败')
        return ''
    logger.info('正在登录Qbittorrent WEBUI账号..')
    try:
        client.auth_log_in()
    except Exception as r:
        logger.warning('Qbittorrent WEBUI信息错误，登录失败，请检查au.yaml文件里的url、用户名、密码，错误信息: %s' %(r))
        logger.warning('获取最新种子hash失败')
        return ''
    addtime=0
    torrentlist=client.torrents.info()
    for item in torrentlist:
        if item.added_on>addtime:
            addtime=item.added_on
            to=item
    return to._torrent_hash

def start_hash(qbinfo,hashlist):
    if hash=='':
        logger.warning('hash为空，并没有开始任何种子')
        return 
    logger.info('正在查找最新发布的种子的hash...')
    logger.info('正在登录Qbittorrent WEBUI页面...')
    try:
        client = Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
    except Exception as r:
        logger.warning('Qbittorrent WEBUI登录失败,错误信息: %s' %(r))
        return 
    logger.info('正在登录Qbittorrent WEBUI账号..')
    try:
        client.auth_log_in()
    except Exception as r:
        logger.warning('Qbittorrent WEBUI信息错误，登录失败，请检查au.yaml文件里的url、用户名、密码，错误信息: %s' %(r))
        return 
    for tohash in hashlist:
        try:
            client.torrents_resume(torrent_hashes=tohash)
        except Exception as r:
            logger.warning('开始种子发生错误,错误信息: %s' %(r))
    






def seedmachine_single(pathinfo,sites,pathyaml,basic,qbinfo,imgdata,hashlist):
    '''
    para:
        pathinfo
        sites 
        pathyaml 用于更新yaml中发布信息
        basic
        qbinfo  
    '''
    logger.info('正在发布路径'+pathinfo.path+'下资源')
    log_error=''
    log_succ=''
    logstr=''
    errornum=0
    succnum=0
    for pathep in pathinfo.eps:

        #判断此集有没有站点要发布,此集合收纳还没有发布过本集的站点
        site_upload=[]
        for siteitem in sites:
            #发布过此集的站点略过
            if sites[siteitem].enable==1 and not( eval('pathinfo.'+siteitem+'_max_done==10000')) and not eval('pathep in pathinfo.'+siteitem+'_done'):
                site_upload.append(sites[siteitem])

        #如果没有站点要发布就略过本集
        if len(site_upload)==0:
            continue

        ls = os.listdir(pathinfo.path)
        filepath=''
        for i in ls:
            c_path=os.path.join(pathinfo.path, i)
            if (os.path.isdir(c_path)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
                continue
            if int(findnum(i)[0])==pathep:
                filepath=c_path
                break
        move_suc=0
        move_newpath=''
        move_oldpath=''
        
        if filepath=='' and pathinfo.zeroday_name!='':
            zeroday_path=os.path.join(pathinfo.path,pathinfo.zeroday_name)
            ls = os.listdir(zeroday_path)
            filepath=''
            for i in ls:
                c_path=os.path.join(zeroday_path, i)
                if (os.path.isdir(c_path)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
                    continue
                if int(findnum(i)[0])==pathep:
                    move_oldpath=os.path.dirname(c_path)
                    filepath=move(c_path,pathinfo.path)
                    move_newpath=filepath
                    move_suc=1
                    break
    
        if filepath=='':
            logger.error('未找到文件夹'+pathinfo.path+'下第'+str(pathep)+'集资源')
            raise ValueError ('未找到文件夹'+pathinfo.path+'下第'+str(pathep)+'集资源')

        #获取file全部信息
        file1=mediafile(filepath,pathinfo,basic,imgdata)
        if not pathinfo.imdb_url=='' and pathyaml['imdb_url']==None:
            pathyaml['imdb_url']=pathinfo.imdb_url
        
        
        
        logger.info('正在发布路径'+pathinfo.path+'下第'+str(pathep)+'集资源:'+filepath)
        logger.info('正在抓取资源信息,请稍后...')
        file1.getfullinfo()
        for siteitem in site_upload:
            if siteitem.enable==0:
                continue
            logger.info('正在'+siteitem.sitename+'站点发布路径'+pathinfo.chinesename+'第'+str(pathep)+'集资源')
            upload_success=False
            uploadtime=0
            #用模板获取mediainfo
            file1.updatemediainfo(siteitem.mediainfo_template_file)
            while upload_success==False and uploadtime<3:
                uploadtime=uploadtime+1
                logger.info('第'+str(uploadtime)+'次尝试发布')

                try:
                    upload_success,logstr=auto_upload(siteitem,file1,basic['record_path'],qbinfo,basic,hashlist)
                except Exception as r:
                    logger.warning('发布资源发生错误，错误信息: %s' %(r))
                    upload_success=False

                if not upload_success:
                    logger.warning(siteitem.sitename+'第'+str(uploadtime)+'次发布任务失败')
                    logger.warning(logstr)
                    file1.mktorrent()

            if not upload_success:
                logger.warning(siteitem.sitename+'发布任务失败，本站暂停发种')
                siteitem.enable=0
                errornum=errornum+1
                log_error=log_error+str(errornum)+':\t'+siteitem.sitename+'   \t'+logstr+'\n'
                logger.warning(logstr)
            elif '已存在' in  logstr:
                errornum=errornum+1
                log_error=log_error+str(errornum)+':\t'+siteitem.sitename+'   \t'+logstr+'\n'
                logger.warning(logstr)
                #记录已发布的种子
                exec('pathinfo.'+siteitem.sitename+'_done.append(pathep)')
                exec('pathinfo.'+siteitem.sitename+'_done.sort()')
                exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
            else:
                succnum=succnum+1
                log_succ=log_succ+str(succnum)+':\t'+siteitem.sitename+'   \t'+logstr+'\n'
                logger.info(logstr)
                #记录已发布的种子
                exec('pathinfo.'+siteitem.sitename+'_done.append(pathep)')
                exec('pathinfo.'+siteitem.sitename+'_done.sort()')
                exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
                #deletetorrent(basic['screenshot_path'])
            #a=input('check')
            
        del(file1)
        if move_suc==1 and os.path.exists(move_newpath) and os.path.exists(move_oldpath):
            logger.info('正在尝试将文件：'+move_newpath+'移动回原位：'+move_oldpath)
            try:
                move_newpath=move(move_newpath,move_oldpath)
                move_suc=0
            except Exception as r:
                logger.warning('移动文件'+move_newpath+'到'+move_oldpath+'链接失败，原因: %s' %(r))
            
    logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
    return log_error,log_succ

def seedmachine(pathinfo,sites,pathyaml,basic,qbinfo,imgdata,hashlist):
    '''
    para:
        pathinfo
        sites 
        pathyaml 用于更新yaml中发布信息
        basic
        qbinfo  
    '''
    logger.info('正在发布路径'+pathinfo.path+'下资源')
    log_error=''
    log_succ=''
    logstr=''
    errornum=0
    succnum=0
    site_upload=[]
    for siteitem in sites:
        #发布过此集的站点略过
        if sites[siteitem].enable==1 and not( eval('pathinfo.'+siteitem+'_max_done==10000')) and not eval('-1 in pathinfo.'+siteitem+'_done'):
            site_upload.append(sites[siteitem])

    #如果没有站点要发布就略过本集
    if len(site_upload)==0:
        logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
        return log_error,log_succ


    #获取file全部信息
    file1=mediafile(pathinfo.path,pathinfo,basic,imgdata)
    if not pathinfo.imdb_url=='' and pathyaml['imdb_url']==None:
        pathyaml['imdb_url']=pathinfo.imdb_url

    logger.info('正在'+siteitem+'站点发布路径'+pathinfo.path+'下资源')
    logger.info('正在抓取资源信息,请稍后...')
    file1.getfullinfo()

    for siteitem in site_upload:
        if siteitem.enable==0:
            continue
        logger.info('正在'+siteitem.sitename+'站点发布'+pathinfo.chinesename+'资源')
        upload_success=False
        uploadtime=0
        #用模板获取mediainfo
        file1.updatemediainfo(siteitem.mediainfo_template_file)
        while upload_success==False and uploadtime<3:
            uploadtime=uploadtime+1
            logger.info('第'+str(uploadtime)+'次尝试发布')
            print("正在准备登录"+siteitem.sitename)


            upload_success,logstr=auto_upload(siteitem,file1,basic['record_path'],qbinfo,basic,hashlist)
            if not upload_success:
                logger.warning(siteitem.sitename+'第'+str(uploadtime)+'次发布任务失败')
                logger.warning(logstr)
                #file1.mktorrent()

        if not upload_success:
            logger.warning(siteitem.sitename+'发布任务失败，本站暂停发种')
            siteitem.enable=0
            errornum=errornum+1
            log_error=log_error+str(errornum)+':\t'+siteitem.sitename+'  \t'+logstr+'\n'
            logger.warning(logstr)
        elif '已存在' in  logstr:
            errornum=errornum+1
            log_error=log_error+str(errornum)+':\t'+siteitem.sitename+'   \t'+logstr+'\n'
            logger.warning(logstr)
            #记录已发布的种子
            exec('pathinfo.'+siteitem.sitename+'_done.append(-1)')
            exec('pathinfo.'+siteitem.sitename+'_done.sort()')
            exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
        else:
            succnum=succnum+1
            log_succ=log_succ+str(succnum)+':\t'+siteitem.sitename+'   \t'+logstr+'\n'
            logger.info(logstr)
            #记录已发布的种子
            exec('pathinfo.'+siteitem.sitename+'_done.append(-1)')
            exec('pathinfo.'+siteitem.sitename+'_done.sort()')
            exec('pathyaml["'+siteitem.sitename+'"]=",".join([str(i) for i in pathinfo.'+siteitem.sitename+'_done])')
            #deletetorrent(basic['screenshot_path'])
        #a=input('check')
            
    del(file1)  
    logger.info('路径'+pathinfo.path+'下资源已全部发布完毕')
    return log_error,log_succ



def start_machine(pathlist,sites,yamlinfo):
    log_allsucc=''
    log_allerror=''
    hashlist=[]
    for path in pathlist:
        if path.enable==0:
            logger.info('路径'+path.path+'的enable被设置为0，已忽略')
            continue
        if (path.type=='anime' or path.type=='tv') and path.collection==0:
            log_error,log_succ=seedmachine_single(path,sites,yamlinfo['path info'][path.pathid],yamlinfo['basic'],yamlinfo['qbinfo'],yamlinfo['image hosting'],hashlist)
        else:
            log_error,log_succ=seedmachine(path,sites,yamlinfo['path info'][path.pathid],yamlinfo['basic'],yamlinfo['qbinfo'],yamlinfo['image hosting'],hashlist)
        write_yaml(yamlinfo)
        if not log_succ=='':
            log_allsucc=log_allsucc+log_succ+'\n'
            logger.info(log_succ)
        print('\n')
        if not log_error=='':
            log_allerror=log_allerror+log_error+'\n'
            logger.error(log_error)

    if 'start' in yamlinfo['qbinfo'] and  yamlinfo['qbinfo']['start']==1:
        logger.info('检测到需要开始种子，正在开始种子...')
        try:
            start_hash(yamlinfo['qbinfo'],hashlist)
        except Exception as r:
            logger.warning('开始种子发生错误,错误信息: %s' %(r))




    print('\n\n以下种子已成功发布:')
    print('*'*100)
    #print(log_allsucc.strip())
    print('\033[1;35m'+log_allsucc.strip()+'\033[0m')
    print('*'*100+'\n\n')
    

    logger.trace('\n\n以下种子已成功发布:')
    logger.trace('*'*100)
    logger.trace(log_allsucc.strip())
    logger.trace('*'*100+'\n\n')

    print('以下种子发布失败:')
    print('&'*100)
    if log_allerror.strip()=='':
        print('\033[1;31;40m 无 \033[0m')
    else:
        print('\033[1;31;40m'+log_allerror.strip()+'\033[0m')
    #print(log_allerror.strip())
    print('&'*100+'\n\n')

    logger.trace('以下种子发布失败:')
    logger.trace('&'*100)
    logger.trace(log_allerror.strip())
    logger.trace('&'*100+'\n\n')


