import json
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import requests
from loguru import logger

def smms_upload(imgpath: str, api_key: str):
    img  = Path(imgpath)
    headers = {'Authorization': api_key}
    files = {'smfile': open(img, 'rb'), 'format': 'json'}
    try:
        #req = requests.post('https://sm.ms/api/v2/upload', headers=headers, files=files)
        req = requests.post('https://smms.app/api/v2/upload', headers=headers, files=files)
    except Exception as r:
        logger.warning('requests 获取失败，原因: %s' %(r))
        return None
    try:
        res = req.json()
    except json.decoder.JSONDecodeError:
        logger.warning('返回结果获取失败')
        res = {}
    if not req.ok:
        logger.warning(
            f"上传图片失败: HTTP {req.status_code}, reason: {req.reason} "
            f"{res.get('msg') if 'msg' in res else ''}")
        return None
    if not res.get('success') and res.get('code') != 'image_repeated':
        logger.warning(f"上传图片失败: [{res.get('code')}]{res.get('message')}")
        return None
    if res.get('code') == 'image_repeated':
        return res.get('images')
    if 'data' not in res or 'url' not in res['data']:
        logger.warning(f"图片直链获取失败")
        return None
    return res['data']['url']

def smms_upload_files(imgpaths: list, api_key: str, form='img'):
    liststr=''
    imgnum=0
    for imgpath in imgpaths:
        imgnum=imgnum+1
        trynum=0
        success=0
        imgstr=''
        while success==0 and trynum<5:
            trynum=trynum+1
            try:
                imgstr=smms_upload(imgpath,api_key)
                success=1
            except Exception as r:
                success=0
                logger.warning('SMMS第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...原因: %s' %(r))
            if imgstr==None:
                success=0
                logger.warning('SMMS第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info('SMMS第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning('SMMS第'+str(imgnum)+'张图片'+imgpath+'上传失败')
    return liststr.strip()

#p1="/Users/moyu/Downloads/在线视频十大品牌-视频app排行榜-视频网站排行榜-买购品牌网 (2).png"
#p2="/Users/moyu/Downloads/zhizhu.jpg"
#imgpaths=[p1,p2]
#key='7ubkPohmLV4LcAUjB5FsDmI0DWvaPo28'
#print(smms_upload(p,key))
#print(smms_upload_files(imgpaths,key,'bbcode'))
