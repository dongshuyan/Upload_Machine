from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def hdsky_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://hdsky.me/takeupload.php"
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
            select_type='411'
        else:
            select_type='413'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='412'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    else:
        select_type='409'
    logger.info('已成功填写类型为'+file1.pathinfo.type)


    #选择来源 
    if file1.type=='WEB-DL':
        medium_sel='11'
    elif 'rip' in file1.type.lower() or file1.type=='bluray'  :
        medium_sel='7'
    elif file1.type=='HDTV':
        medium_sel='5'
    elif file1.type=='remux':
        medium_sel='3'
    else:
        medium_sel='7'
    logger.info('已成功选择质量为'+file1.type)
   


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='10'
    elif file1.Video_Format=='H265':
        codec_sel='12'
    elif file1.Video_Format=='x265':
        codec_sel='13'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='6'
    elif 'DTS-HDMA:X 7.1' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'DTS-HDMA' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'TRUEHD ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'DTS-HD HR' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'PCM' in file1.Audio_Format.upper():
        audiocodec_sel='19'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'DSD' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    elif 'Dolby Digital Plus Dolby Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='21'
    elif 'Dolby Digital Plus' in file1.Audio_Format.upper():
        audiocodec_sel='20'
    else:
        audiocodec_sel='7'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '2160' in file1.standard_sel:
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
    

    #选择制作组
    if 'HDSKY' in file1.sub.upper():
        team_sel='6'
        tags.append(12)
    elif 'HDS3D' in file1.sub.upper():
        team_sel='28'
        tags.append(12)
    elif 'HDSTV' in file1.sub.upper():
        team_sel='9'
        tags.append(12)
    elif 'HDSWEB' in file1.sub.upper() and file1.pathinfo.collection==1:
        team_sel='35'
        tags.append(12)
    elif 'HDSWEB' in file1.sub.upper():
        team_sel='31'
        tags.append(12)
    elif 'HDSPAD' in file1.sub.upper():
        team_sel='18'
        tags.append(12)
    elif 'HDSCD' in file1.sub.upper():
        team_sel='22'
        tags.append(12)
    elif 'hdspecial' in file1.sub.lower():
        team_sel='34'
        tags.append(12)
    elif 'BMDRU' in file1.sub.upper():
        team_sel='30'
        tags.append(12)
    elif 'AREA11' in file1.sub.upper():
        team_sel='25'
        tags.append(12)
    elif 'HDSAB' in file1.sub.upper():
        team_sel='36'
        tags.append(12)
    elif 'HDS' in file1.sub.upper():
        team_sel='1'
        tags.append(12)
    elif file1.transfer==0:
        team_sel='24'
    elif file1.transfer==1:
        team_sel='27'
    else:
        team_sel='27'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'hdsky' in file1.pathinfo.exclusive :
        tags.append(2)
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
    if file1.transfer==0:
        tags.append(14)
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
            "url_douban": file1.doubanurl,
            "nfo": "",
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "type": select_type,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "option_sel[]": tags,
            }

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    

    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)