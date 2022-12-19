from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def hdpt_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://hdpt.xyz/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
        tags.append(18)
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='409'
    elif 'cartoon' in file1.pathinfo.type.lower():
        select_type='412'
        tags.append(18)
    else:
        select_type='405'
        tags.append(18)
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择媒介
    if file1.type=='WEB-DL':
        medium_sel='10'
    elif 'webrip' in file1.type.lower():
        medium_sel='11'
    elif 'rip' in file1.type.lower():
        medium_sel='7'
    elif 'hdtv'in file1.type.lower():
        medium_sel='5'
    elif 'remux' in file1.type.lower():
        medium_sel='3'
    else:
        medium_sel='15'
    logger.info('已成功选择质量为'+file1.type)
   


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='1'
    elif file1.Video_Format=='H265':
        codec_sel='6'
    elif file1.Video_Format=='x265':
        codec_sel='6'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='5'
    elif '2160' in file1.standard_sel:
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='4'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
   #选择处理
    if 'rip' in file1.type.lower():
        processing_sel='2'
    else:
        processing_sel='1'
    logger.info('已选择处理为'+('rip' in file1.type.lower())*'Encode'+(1-('rip' in file1.type.lower()))*'Raw')

    #选择制作组
    if 'HDS' in file1.sub.upper():
        team_sel='1'
    elif 'CHD' in file1.sub.upper():
        team_sel='2'
    elif 'MYSILU' in file1.sub.upper():
        team_sel='3'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    elif 'HDH' in file1.sub.upper():
        team_sel='7'
    elif 'OURTV' in file1.sub.upper():
        team_sel='8'
    elif 'NGB' in file1.sub.upper():
        team_sel='9'
    elif 'U2' in file1.sub.upper():
        team_sel='10'
    elif 'LHD' in file1.sub.upper():
        team_sel='11'
    elif 'CHDBITS' in file1.sub.upper():
        team_sel='12'
    elif 'PTER' in file1.sub.upper():
        team_sel='13'
    elif 'CMCT' in file1.sub.upper():
        team_sel='14'
    elif 'FRDS' in file1.sub.upper():
        team_sel='15'
    elif 'HARES' in file1.sub.upper():
        team_sel='16'
    elif 'HDPT' in file1.sub.upper():
        team_sel='18'
    else:
        team_sel='17'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'hdpt' in file1.sub.lower():
        tags.append(3)
        logger.info('已选择官方')
    if file1.pathinfo.transfer==0:
        tags.append(21)
        logger.info('已选择原创')
    if 'hdpt' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')

    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
            }

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)