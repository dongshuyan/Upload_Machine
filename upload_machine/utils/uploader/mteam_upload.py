from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def mteam_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://kp.m-team.cc/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==1:
        if '480' in file1.standard_sel:
            select_type='403'
        else:
            select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        if 'remux' in file1.type.lower():
            select_type='439'
        elif 'dvd' in file1.type.lower() and 'iso' in file1.type.lower():
            select_type='420'
        elif 'blu' in file1.type.lower() or 'bdmv' in file1.type.lower() or 'iso' in file1.type.lower():
            select_type='421'
        elif '480' in file1.standard_sel:
            select_type='401'
        else:
            select_type='419'
        select_type='401'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='434'
    else:
        select_type='405'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='1'
    elif file1.Video_Format=='H265':
        codec_sel='16'
    elif file1.Video_Format=='x265':
        codec_sel='16'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            processing_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='6'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='5'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='6'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='6'
            logger.info('未找到资源国家信息，已选择其他')
    else:
        processing_sel='4'
        logger.info('未找到资源国家信息，已默认日本')

    #选择制作组
    if 'MTeam' in file1.sub.upper():
        team_sel='9'
    elif 'LowPower-Raws' in file1.sub.upper():
        team_sel='22'
    else:
        team_sel='0'
    logger.info('制作组已成功选择为'+file1.sub)

    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            
    other_data = {
            "type": select_type,
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.imdburl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "codec_sel": codec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            "team_sel": '8',
            "uplver": uplver,
            }

    if '国' in file1.language or '中' in file1.language:
        other_data['l_dub']='yes'
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        other_data['l_sub']='yes'
        logger.info('已选择中字')
    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)