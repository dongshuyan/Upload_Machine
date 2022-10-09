from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def hare_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://club.hares.top/takeupload.php"
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
        select_type='415'
    else:
        select_type='415'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择媒介
    if 'web' in file1.type.lower():
        medium_sel='5'
    elif (file1.type=='bluray') and '2160' in file1.standard_sel:
        medium_sel='1'
    elif file1.type=='bluray':
        medium_sel='2'
    elif 'rip' in file1.type.lower()  :
        medium_sel='4'
    elif file1.type=='HDTV' and '2160' in file1.standard_sel:
        medium_sel='6'
    elif file1.type=='HDTV':
        medium_sel='8'
    elif file1.type=='remux':
        medium_sel='3'
    else:
        medium_sel='5'
    logger.info('已成功填写来源为'+file1.type)
   


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='8'
    elif file1.Video_Format=='H265':
        codec_sel='6'
    elif file1.Video_Format=='x265':
        codec_sel='7'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'TrueHD Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'TrueHD' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='5'
    elif '2160' in file1.standard_sel:
        standard_sel='6'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='1'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='3'
    elif '1440' in file1.standard_sel:
        standard_sel='7'
    else:
        standard_sel='1'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            processing_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='9'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='10'
            logger.info('未找到资源国家信息，已选择其他')
    else:
        processing_sel='10'
        logger.info('未找到资源国家信息，已默认其他')

    #选择制作组
    if 'HARESWEB' in file1.sub.upper():
        team_sel='2'
    elif 'HARESTV' in file1.sub.upper():
        team_sel='3'
    elif 'HARES' in file1.sub.upper():
        team_sel='1'
    elif 'CHD' in file1.sub.upper():
        team_sel='4'
    elif 'HDS' in file1.sub.upper():
        team_sel='5'
    elif 'WIKI' in file1.sub.upper():
        team_sel='6'
    elif 'CMCT' in file1.sub.upper():
        team_sel='8'
    elif 'BEAST' in file1.sub.upper():
        team_sel='9'
    elif 'HDC' in file1.sub.upper():
        team_sel='10'
    elif 'FRDS' in file1.sub.upper():
        team_sel='11'
    elif 'PTER' in file1.sub.upper():
        team_sel='12'
    elif 'BHD' in file1.sub.upper():
        team_sel='13'
    elif 'PTH' in file1.sub.upper():
        team_sel='14'
    else:
        team_sel='15'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'hare' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if 'HARES' in file1.sub.upper():
        tags.append(3)
        logger.info('已选择官方')
    if file1.pathinfo.transfer==0:
        tags.append(4)
        logger.info('已选择原创')
    if '国' in file1.language or '中' in file1.language:
        tags.append(6)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(9)
        logger.info('已选择中字')
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.complete==0:
        tags.append(16)
        logger.info('已选择追更')

    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname.replace('  ',' ').replace(' ','.'),
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "pt_gen[douban][link]": file1.doubanurl,
            "pt_gen[imdb][link]" : file1.imdburl,
            "pt_gen[bangumi][link]" : file1.bgmurl,
            "url_poster" : re.findall(r'\[img\](.*)\[/img\]',file1.douban_info),
            "screenshots" : file1.screenshoturl.replace('[img]','').replace('[/img]',''),
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.douban_info,
            "technical_info" : file1.mediainfo,
            "type": select_type,
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