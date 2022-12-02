from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def ihdbits_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://ihdbits.me/takeupload.php"
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
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='402'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='404'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='409'
    else:
        select_type='405'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择来源
    if 'web' in file1.type.lower():
        source_sel='3'
    elif (file1.type=='bluray' or 'bd' in file1.type.lower()) and '2160' in file1.standard_sel:
        source_sel='2'
    elif file1.type=='bluray' or 'bd' in file1.type.lower():
        source_sel='1'
    elif 'dvd' in file1.type.lower()  :
        source_sel='6'
    elif file1.type=='HDTV':
        source_sel='4'
    elif file1.type=='remux':
        source_sel='6'
    else:
        source_sel='6'
    logger.info('已成功填写来源为'+file1.type)

    #选择媒介
    if 'web' in file1.type.lower() and 'dl' in file1.type.lower():
        medium_sel='9'
    elif (file1.type=='bluray') and '2160' in file1.standard_sel:
        medium_sel='2'
    elif file1.type=='bluray':
        medium_sel='1'
    elif 'rip' in file1.type.lower() and  'web' in file1.type.lower():
        medium_sel='11'
    elif 'rip' in file1.type.lower() and 'dvd' in file1.type.lower():
        medium_sel='7'
    elif 'rip' in file1.type.lower()  :
        medium_sel='7'
    elif 'HDTV' in file1.type.upper() and '2160' in file1.standard_sel:
        medium_sel='5'
    elif 'HDTV' in file1.type.upper():
        medium_sel='5'
    elif 'remux' in file1.type.lower()and '2160' in file1.standard_sel:
        medium_sel='6'
    elif 'remux' in file1.type.lower():
        medium_sel='3'
    elif 'dvd' in file1.type.lower():
        medium_sel='7'
    else:
        medium_sel='9'
    logger.info('已成功选择媒介为'+file1.type)


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='1'
    elif file1.Video_Format=='H265':
        codec_sel='3'
    elif file1.Video_Format=='x265':
        codec_sel='3'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)


    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'TRUEHD ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'OPUS' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'TAA' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())


    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='4'
    elif '2160' in file1.standard_sel:
        standard_sel='5'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '480' in file1.standard_sel:
        standard_sel='6'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)

    if 'rip' in file1.type.lower():
        processing_sel='2'
        logger.info('处理已成功选择为Encode')
    else:
        processing_sel='1'
        logger.info('处理已成功选择为Raw')

    #选择制作组
    if 'IHDBITS' in file1.sub.upper():
        team_sel='1'
    elif 'IHDTV' in file1.sub.upper():
        team_sel='6'
    elif 'IHDWEB' in file1.sub.upper():
        team_sel='7'
    elif 'IHD' in file1.sub.upper():
        team_sel='3'
    elif 'TTG' in file1.sub.upper():
        team_sel='2'
    elif 'WIKI' in file1.sub.upper():
        team_sel='4'
    elif 'CHDBITS' in file1.sub.upper():
        team_sel='8'
    elif 'M-TEAM' in file1.sub.upper():
        team_sel='9'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'IHD' in file1.sub.upper():
        tags.append(3)
        logger.info('已选择官方')
    if file1.pathinfo.transfer==0:
        tags.append(9)
        logger.info('已选择原创')
    if 'ihdbits' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    '''
    if '粤' in file1.language:
        tags.append(10)
        logger.info('已选择粤语')
    '''
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
            "url": file1.imdburl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "source_sel" : source_sel,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
            }
    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)