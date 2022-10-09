from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def wintersakura_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://wintersakura.net/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='413'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==1:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='417'
        else:
            select_type='402'
    elif 'tv' in file1.pathinfo.type.lower() and file1.pathinfo.collection==0:
        if '大陆' in file1.country or '香港' in file1.country or '台湾' in file1.country:
            select_type='402'
        else:
            select_type='416'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='410'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='406'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='407'
    else:
        select_type='409'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择质量
    if file1.type=='WEB-DL':
        medium_sel='21'
    elif 'rip' in file1.type.lower() or file1.type=='bluray'  :
        medium_sel='15'
    elif file1.type=='HDTV':
        medium_sel='16'
    elif file1.type=='Remux':
        medium_sel='14'
    else:
        medium_sel='15'
    logger.info('已成功选择质量为'+file1.type)
   


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='6'
    elif file1.Video_Format=='x264':
        codec_sel='8'
    elif file1.Video_Format=='H265':
        codec_sel='9'
    elif file1.Video_Format=='x265':
        codec_sel='7'
    else:
        codec_sel='6'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='19'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='8'
    elif 'TrueHD Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'TrueHD' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='16'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='20'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='23'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='21'
    else:
        audiocodec_sel='19'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

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
    

    #选择制作组
    if 'wsub' in file1.sub.lower():
        team_sel='12'
    elif 'sakura academic' in file1.sub.lower():
        team_sel='19'
    elif 'wsdiy' in file1.sub.lower():
        team_sel='11'
    elif 'wscode' in file1.sub.lower():
        team_sel='16'
    elif 'sakuraweb' in file1.sub.lower():
        team_sel='18'
    elif 'bhd' in file1.sub.lower():
        team_sel='9'
    elif 'chd' in file1.sub.lower():
        team_sel='2'
    elif 'hds' in file1.sub.lower():
        team_sel='1'
    elif 'hdc' in file1.sub.lower():
        team_sel='14'
    elif 'mteam' in file1.sub.lower():
        team_sel='13'
    elif 'ttg' in file1.sub.lower():
        team_sel='15'
    elif 'cmct' in file1.sub.lower():
        team_sel='6'
    elif 'frds' in file1.sub.lower():
        team_sel='7'
    elif 'pter' in file1.sub.lower():
        team_sel='8'
    elif 'tjupt' in file1.sub.lower():
        team_sel='17'
    else:
        team_sel='5'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'sakura academic' in file1.sub.lower():
        tags.append(15)
        logger.info('已选择Sakura Academic')
    if 'sakuraweb' in file1.sub.lower():
        tags.append(14)
        logger.info('已选择Sakura WEB')
    if 'wsub' in file1.sub.lower():
        tags.append(13)
        logger.info('已选择Sakura SUB')
    if 'sakura' in file1.sub.lower() or 'wsub' in file1.sub.lower():
        tags.append(3)
        logger.info('已选择官方标签')
    if 'wintersakura' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')
    if file1.pathinfo.transfer==0:
        tags.append(8)
        logger.info('已选择原创')

    
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
            "pt_gen": file1.doubanurl,
            "url" : file1.imdburl,
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
            "tags[]": tags,
            }

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)