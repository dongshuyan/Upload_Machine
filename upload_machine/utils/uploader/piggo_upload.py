from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def piggo_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://piggo.me/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='405'
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='408'
    else:
        select_type='409'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择来源 
    if 'web' in file1.type.lower() and 'rip' in file1.type.lower():
        source_sel='10'
    elif 'web' in file1.type.lower():
        source_sel='7'
    elif (file1.type=='bluray' or 'bd' in file1.type.lower()) and '2160' in file1.standard_sel:
        source_sel='8'
    elif file1.type=='bluray' or 'bd' in file1.type.lower():
        source_sel='1'
    elif 'dvd' in file1.type.lower()  :
        source_sel='3'
    elif file1.type=='HDTV':
        source_sel='4'
    elif file1.type=='remux':
        source_sel='1'
    else:
        source_sel='6'
    logger.info('已成功选择质量为'+file1.type)
   


    #选择媒介
    if file1.type=='WEB-DL':
        medium_sel='11'
    elif 'rip' in file1.type.lower() or file1.type=='bluray'  :
        medium_sel='7'
    elif file1.type=='HDTV':
        medium_sel='5'
    elif file1.type=='Remux':
        medium_sel='3'
    elif (file1.type=='bluray' or 'bd' in file1.type.lower()) and '2160' in file1.standard_sel:
        medium_sel='10'
    elif file1.type=='bluray' or 'bd' in file1.type.lower():
        medium_sel='1'
    elif 'dvd' in file1.type.lower()  :
        medium_sel='6'
    elif 'rip' in file1.type.lower():
        medium_sel='7'
    else:
        medium_sel='7'
    logger.info('已成功填写媒介为'+file1.type)


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
    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'TRUEHD ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    else:
        audiocodec_sel='6'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        logger.warning('站点不允许发布'+file1.standard_sel+'资源')
        return False,fileinfo+'站点不允许发布'+file1.standard_sel+'资源'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    #选择制作组
    if 'HDS' in file1.sub.upper():
        team_sel='1'
    elif 'CHD' in file1.sub.upper():
        team_sel='2'
    elif 'MYSILU' in file1.sub.upper():
        team_sel='3'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    elif 'CMCT' in file1.sub.upper():
        team_sel='6'
    elif 'PIGGOHD' in file1.sub.upper():
        team_sel='7'
    elif 'PIGGOWEB'.upper() in file1.sub.upper():
        team_sel='8'
    elif 'PiGoNF'.upper() in file1.sub.upper():
        team_sel='9'
    elif 'PigoAD'.upper() in file1.sub.upper():
        team_sel='10'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)


    if 'piggo' in file1.pathinfo.exclusive :
        tags.append(1)
    if 'PIGO' in file1.sub.upper():
        tags.append(3)
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
    if file1.pathinfo.collection==1:
        tags.append(11)
    if file1.pathinfo.complete==1:
        tags.append(13)
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.complete==0:
        tags.append(14)
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath

    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            
    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.imdburl,
            "pt_gen": file1.doubanurl,
            "nfo": "",
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "technical_info": file1.mediainfo,
            "type": select_type,
            "source_sel[4]": source_sel,
            "medium_sel[4]": medium_sel,
            "codec_sel[4]": codec_sel,
            "audiocodec_sel[4]": audiocodec_sel,
            "standard_sel[4]": standard_sel,
            "team_sel[4]": team_sel,
            "processing_sel[4]": 1,
            "uplver": uplver,
            "tags[4][]": tags,
            }
    scraper=cloudscraper.create_scraper()
    success_upload=0
    try_upload=0
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)