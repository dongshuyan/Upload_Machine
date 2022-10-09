from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def ssd_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://springsunday.net/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='504'
    elif 'tv' in file1.pathinfo.type.lower():
        select_type='502'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='501'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='505'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='503'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='506'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='507'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='508'
    else:
        select_type='509'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择来源 
    if 'remux' in file1.type.lower():
        medium_sel='4'
    elif 'bdrip' in file1.type.lower():
        medium_sel='6'
    elif file1.type=='WEB-DL':
        medium_sel='7'
    elif 'webrip' in file1.type.lower():
        medium_sel='8'
    elif file1.type=='HDTV':
        medium_sel='5'
    elif 'tvrip' in file1.type.lower():
        medium_sel='9'
    elif 'dvdrip' in file1.type.lower():
        medium_sel='10'
    elif 'dvd' in file1.type.lower():
        medium_sel='3'
    else:
        medium_sel='12'
    logger.info('已成功选择质量为'+file1.type)



    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='2'
    elif file1.Video_Format=='x264':
        codec_sel='2'
    elif file1.Video_Format=='H265':
        codec_sel='1'
    elif file1.Video_Format=='x265':
        codec_sel='1'
    else:
        codec_sel='2'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='5'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'TrueHD Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'TrueHD' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    else:
        audiocodec_sel='10'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='1'
    elif '2160' in file1.standard_sel:
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='2'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='3'
    elif '720' in file1.standard_sel:
        standard_sel='4'
    elif '480' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='2'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择地区
    if file1.country!='' :
        if '大陆' in file1.country:
            source_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            source_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            source_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            source_sel='9'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            source_sel='9'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            source_sel='9'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            source_sel='10'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            source_sel='10'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            source_sel='3'
            logger.info('国家信息已选择'+file1.country)
        else:
            source_sel='3'
            logger.info('未找到资源国家信息，已选择Other')
    else:
        source_sel='10'
    logger.info('未找到资源国家信息，已默认日本')

    if file1.pathinfo.collection==1:
        pack='yes'
    else:
        pack='no'
    
    if 'ssd' in file1.pathinfo.exclusive:
        exclusive='yes'
    else:
        exclusive='no'

    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname.replace('  ',' ').replace(' ','.'),
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url": file1.doubanurl,
            "url_vimages": file1.screenshoturl.replace('[img]','').replace('[/img]',''),
            "Media_BDInfo": file1.mediainfo,
            "color": "0",
            "font": "0",
            "size": "0",
            "type": select_type,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "source_sel" : source_sel,
            "uplver": uplver,
            "exclusive": exclusive,
            "pack": pack,
            }

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)