from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def zhuque_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://zhuque.in/api/torrent/upload"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='503'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==1:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='502'
        else:
            select_type='502'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='502'
        else:
            select_type='502'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='501'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='504'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='599'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='599'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='599'
    elif 'music' in file1.pathinfo.type.lower():
        select_type='599'
    else:
        select_type='599'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择媒介
    if 'web' in file1.type.lower() and 'dl' in file1.type.lower():
        medium_sel='309'
    elif (file1.type=='bluray') and '2160' in file1.standard_sel:
        medium_sel='301'
    elif file1.type=='bluray':
        medium_sel='303'
    elif 'rip' in file1.type.lower() and  'web' in file1.type.lower():
        medium_sel='306'
    elif 'rip' in file1.type.lower() and 'dvd' in file1.type.lower():
        medium_sel='306'
    elif 'rip' in file1.type.lower()  :
        medium_sel='306'
    elif 'HDTV' in file1.type.upper() and '2160' in file1.standard_sel:
        medium_sel='307'
    elif 'HDTV' in file1.type.upper():
        medium_sel='308'
    elif 'remux' in file1.type.lower():
        medium_sel='305'
    elif 'dvd' in file1.type.lower():
        medium_sel='399'
    else:
        medium_sel='399'
    logger.info('已成功选择媒介为'+file1.type)


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='101'
    elif file1.Video_Format=='x264':
        codec_sel='103'
    elif file1.Video_Format=='H265':
        codec_sel='102'
    elif file1.Video_Format=='x265':
        codec_sel='104'
    else:
        codec_sel='101'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='201'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='204'
    elif 'TRUEHD ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='206'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='210'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='205'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='209'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='299'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='299'
    elif 'DDP' in file1.Audio_Format.upper():
        audiocodec_sel='207'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='208'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='203'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='202'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='299'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='299'
    else:
        audiocodec_sel='299'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='499'
    elif '2160' in file1.standard_sel:
        standard_sel='404'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='403'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='402'
    elif '720' in file1.standard_sel:
        standard_sel='401'
    elif '480' in file1.standard_sel:
        standard_sel='499'
    else:
        standard_sel='499'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    

    #选择制作组
    if 'ZHUQUE' in file1.sub.upper():
        team_sel='4001'
    elif 'HARES' in file1.sub.upper():
        team_sel='4101'
    elif 'HARESWEB' in file1.sub.upper():
        team_sel='4102'
    elif 'HARESTV' in file1.sub.upper():
        team_sel='4103'
    elif 'OURBITS' in file1.sub.upper():
        team_sel='4201'
    elif 'OURTV' in file1.sub.upper():
        team_sel='4202'
    elif 'FLTTH' in file1.sub.upper():
        team_sel='4203'
    elif 'ILOVETV' in file1.sub.upper():
        team_sel='4204'
    elif 'MTEAM' in file1.sub.upper():
        team_sel='4211'
    elif 'GEEK' in file1.sub.upper():
        team_sel='4212'
    elif 'CMCT' in file1.sub.upper():
        team_sel='4221'
    elif 'CMCTV' in file1.sub.upper():
        team_sel='4222'
    elif 'DREAM' in file1.sub.upper():
        team_sel='4241'
    elif 'DBTV' in file1.sub.upper():
        team_sel='4242'
    elif 'QHSTUDIO' in file1.sub.upper():
        team_sel='4243'
    else:
        team_sel='4999'
    logger.info('制作组已成功选择为'+file1.sub)
    

    if 'ZHUQUE' in file1.sub.upper():
        tags.append(601)
        logger.info('已选择官方')
    if 'zhuque' in file1.pathinfo.exclusive :
        tags.append(602)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(603)
        logger.info('已选择国语')
    '''
    if '粤' in file1.language:
        tags.append(10)
        logger.info('已选择粤语')
    '''
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(604)
        logger.info('已选择中字')

    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='true'
    else:
        uplver='false'

    torrent_file = file1.torrentpath
    #file_tup = ("torrent", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
    file_tup = {'file': open(torrent_file, 'rb')}

    other_data = {
            "title": file1.uploadname,
            "subtitle": file1.small_descr+file1.pathinfo.exinfo,
            "doubanid": re.findall('subject/(\d+)',file1.doubanurl)[0],
            "screenshot": file1.screenshoturl.replace('[img]','').replace('[/img]',''),
            "mediainfo": file1.mediainfo,
            "category": select_type,
            "medium": medium_sel,
            "videoCoding": codec_sel,
            "audioCoding": audiocodec_sel,
            "resolution": standard_sel,
            "group": team_sel,
            "anonymous": uplver,
            "tags": ','.join(tags),
            }

    scraper=cloudscraper.create_scraper()
    
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)