from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def lemonhd_upload(web,file1,record_path,qbinfo,basic,hashlist):
    if 'anime' in file1.pathinfo.type.lower():
        return lemonhd_upload_anime(web,file1,record_path,qbinfo,basic,hashlist)
    elif 'tv' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo,basic,hashlist,'https://lemonhd.org/takeupload_tv.php')
    elif 'movie' in file1.pathinfo.type.lower():
        return lemonhd_upload_tv(web,file1,record_path,qbinfo,basic,hashlist,'https://lemonhd.org/takeupload_movie.php')



def lemonhd_upload_anime(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://lemonhd.org/takeupload_animate.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    

    #选择媒介
    if file1.type=='WEB-DL':
        animate_category='7'
    elif 'bdrip' in file1.type.lower() :
        animate_category='2'
    elif 'hdtvrip' in file1.type.lower() :
        animate_category='6'
    elif 'hdtv' in file1.type.lower():
        animate_category='5'
    elif 'remux' in file1.type.lower():
        animate_category='10'
    elif 'dvdrip' in file1.type.lower() :
        animate_category='4'
    else:
        animate_category='7'
    logger.info('已成功选择质量为'+file1.type)


    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='12'
    elif file1.Video_Format=='H265':
        codec_sel='10'
    elif file1.Video_Format=='x265':
        codec_sel='11'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='8'
    elif 'DTS-HD HR' in file1.Audio_Format.upper() or 'DTS-HDHR' in file1.Audio_Format.upper():
        audiocodec_sel='104'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'TrueHD Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'TrueHD' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    else:
        audiocodec_sel='8'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='2'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='4'
    elif '480' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='2'
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
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='5'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='5'
            logger.info('未找到资源国家信息，已默认其他')
    else:
        processing_sel='4'
        logger.info('未找到资源国家信息，已默认日本')

    
    
    tag_jz='no'
    tag_gy='no'
    tag_zz='no'
    uplver='no'
    if 'lemonhd' in file1.pathinfo.exclusive and ('league' in file1.sub.lower() or 'lhd' in file1.sub.lower() or 'cint' in file1.sub.lower() or 'i18n' in file1.sub.lower() ):
        tag_jz='yes'
    if '国' in file1.language or '中' in file1.language:
        tag_gy='yes'
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tag_zz='yes'
    if siteinfo.uplver==1:
        uplver='yes'


    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "douban_url": file1.doubanurl,
            "url" : file1.imdburl,
            "bangumi_url": file1.bgmurl,
            "anidb_url": file1.anidburl,
            "cn_name": file1.chinesename,
            "en_name": file1.englishname,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "year": str(file1.year),
            "animate_category": animate_category,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            }
    buttomlist=["uplver","tag_jz","tag_zz","tag_gy"]
    for item in buttomlist:
        if eval(item+"=='yes'"):
            exec('other_data["'+item+'"]="yes"')
    #官组        
    if 'league' in file1.sub.lower():
        other_data['descr']=file1.douban_info+'\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-info-s3.png[/img]\n[quote=Mediainfo]\n'+file1.mediainfo+'\n[/quote]\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-screen-s3.png[/img]\n'+file1.screenshoturl

    if 'movie' in file1.pathinfo.type.lower():
        other_data['animate_type']='1'
        logger.info('已成功选择类型为movie')
        other_data['edition_sel']='1'
        logger.info('已成功选择类型为原版/普通版')
    else:
        if file1.pathinfo.collection==0:
            other_data['animate_type']='3'
            logger.info('已成功选择类型为TV')  
        else:
            other_data['animate_type']='6'
            logger.info('已成功选择类型为collection')

    if file1.pathinfo.complete==0:
        other_data['is_complete']='yes'
        logger.info('已成功选择未完结')
        other_data['series']='第'+file1.episodename+'话'
        
    elif file1.pathinfo.complete==1:
        other_data['series']='TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)+' Fin'
    else:
        other_data['series']='TV '+str(file1.pathinfo.min).zfill(2)+'-'+str(file1.pathinfo.max).zfill(2)
    logger.info('已成功填写集数')

    if 'i18n' in file1.sub.lower():
        other_data['team_sel']='9'
    elif 'lhd' in file1.sub.lower():
        other_data['team_sel']='14'
    elif 'leaguehd' in file1.sub.lower():
        other_data['team_sel']='8'
    elif 'leaguenf' in file1.sub.lower():
        other_data['team_sel']='12'
    elif 'leaguetv' in file1.sub.lower():
        other_data['team_sel']='10'
    elif 'leaguecd' in file1.sub.lower():
        other_data['team_sel']='11'
    elif 'leagueweb' in file1.sub.lower():
        other_data['team_sel']='13'
    elif 'cint' in file1.sub.lower():
        other_data['team_sel']='15'
    else:
        other_data['source_author']=file1.sub
    
    #选择来源

    if file1.pathinfo.transfer==1:
        other_data['original']='1'
        logger.info('已选择来源为转载')
        other_data['from_url']=file1.from_url
        logger.info('已成功填写转载地址')
    elif file1.pathinfo.transfer==0:
        other_data['original']='2'
        logger.info('已选择来源为原创')
    else:
        other_data['original']='1'
        logger.info('已默认来源为转载')
        other_data['from_url']=file1.from_url
        logger.info('已成功填写转载地址')

    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)








def lemonhd_upload_tv(siteinfo,file1,record_path,qbinfo,basic,hashlist,up_url):
    post_url = up_url
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename

    #选择版本
    edition_sel='1'
    logger.info('版本已选择原版')



    #选择媒介
    if file1.type=='WEB-DL':
        medium_sel='11'
    elif 'rip' in file1.type.lower() :
        medium_sel='7'
    elif 'hdtvrip' in file1.type.lower() :
        medium_sel='7'
    elif 'hdtv' in file1.type.lower():
        medium_sel='5'
    elif 'remux' in file1.type.lower():
        medium_sel='3'
    elif 'dvd' in file1.type.lower() :
        medium_sel='6'
    else:
        medium_sel='7'
    logger.info('已成功选择媒介为'+file1.type)



    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='12'
    elif file1.Video_Format=='H265':
        codec_sel='10'
    elif file1.Video_Format=='x265':
        codec_sel='11'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='8'
    elif 'DTS-HD HR' in file1.Audio_Format.upper() or 'DTS-HDHR' in file1.Audio_Format.upper():
        audiocodec_sel='104'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='5'
    elif 'TrueHD Atmos' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='15'
    elif 'TrueHD' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='11'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='9'
    elif 'OGG' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'AC3' in file1.Audio_Format.upper() or 'DD' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    else:
        audiocodec_sel='8'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='6'
    elif '2160' in file1.standard_sel:
        standard_sel='1'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='2'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='2'
    elif '720' in file1.standard_sel:
        standard_sel='4'
    elif '480' in file1.standard_sel:
        standard_sel='5'
    else:
        standard_sel='2'
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
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='5'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='5'
            logger.info('未找到资源国家信息，已默认其他')
    else:
        processing_sel='4'
        logger.info('未找到资源国家信息，已默认日本')
    
    
    tag_jz='no'
    tag_gy='no'
    tag_zz='no'
    uplver='no'
    if 'lemonhd' in file1.pathinfo.exclusive and ('league' in file1.sub.lower() or 'lhd' in file1.sub.lower() or 'cint' in file1.sub.lower() or 'i18n' in file1.sub.lower() ):
        tag_jz='yes'
    if '国' in file1.language or '中' in file1.language:
        tag_gy='yes'
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tag_zz='yes'
    if siteinfo.uplver==1:
        uplver='yes'
    

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "douban_url": file1.doubanurl,
            "url" : file1.imdburl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.content,
            "edition_sel" : edition_sel,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            }

    buttomlist=["uplver","tag_jz","tag_zz","tag_gy"]
    for item in buttomlist:
        if eval(item+"=='yes'"):
            exec('other_data["'+item+'"]="yes"')

    #官组        
    if 'league' in file1.sub.lower():
        other_data['descr']=file1.douban_info+'\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-info-s3.png[/img]\n[quote=Mediainfo]\n'+file1.mediainfo+'\n[/quote]\n[img]https://imgbox.leaguehd.com/images/2022/07/29/Movie-screen-s3.png[/img]\n'+file1.screenshoturl
    
    if 'tv' in file1.pathinfo.type.lower():
        if 'show' in file1.pathinfo.type.lower():
            other_data['type']='403'
            logger.info('已成功选择类型为TV Shows(综艺)')
        else:
            other_data['type']='402'
            logger.info('已成功选择类型为TV Series(电视剧)')
        if file1.pathinfo.complete==1:
            other_data['is_complete']='yes'

        other_data['t_season']=file1.season
        
        if file1.pathinfo.collection==0:
            other_data['series']='E'+file1.episodename
        elif file1.pathinfo.complete==1:
            other_data['series']='E'+str(file1.pathinfo.min).zfill(2)+'-E'+str(file1.pathinfo.max).zfill(2)+' Fin'
        else:
            other_data['series']='E'+str(file1.pathinfo.min).zfill(2)+'-E'+str(file1.pathinfo.max).zfill(2)
        logger.info('已成功填写集数')
    
    if 'movie' in file1.pathinfo.type.lower():
        other_data['type']='401'

    #选择制作组
    if 'i18n' in file1.sub.lower():
        other_data['team_sel']='9'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'lhd' in file1.sub.lower():
        other_data['team_sel']='14'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'leaguehd' in file1.sub.lower():
        other_data['team_sel']='8'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'leaguenf' in file1.sub.lower():
        other_data['team_sel']='12'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'leaguetv' in file1.sub.lower():
        other_data['team_sel']='10'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'leaguecd' in file1.sub.lower():
        other_data['team_sel']='11'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'leagueweb' in file1.sub.lower():
        other_data['team_sel']='13'
        logger.info('制作组已成功选择为'+file1.sub)
    elif 'cint' in file1.sub.lower():
        other_data['team_sel']='15'
        logger.info('制作组已成功选择为'+file1.sub)
    else:
        logger.info('非官组资源')
    
    if file1.pathinfo.transfer==1:
        other_data['from_url']=file1.from_url
        logger.info('已成功填写转载地址')


    scraper=cloudscraper.create_scraper()
    r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)