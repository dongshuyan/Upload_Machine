import json
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from loguru import logger


def GetPicUrl(url:str):
    html_doc = requests.get(url).content.decode()
    soup = BeautifulSoup(html_doc, 'html.parser')
    pic_list = soup.find_all('img')
    for item in pic_list:
        url = item.get('src')
        if 'fapping.empornium.sx/images/' in url:
        	return url
    return None

def femp_upload(imgpath: str):
    img  = Path(imgpath)
    files = {'ImageUp': open(img, 'rb')}
    data = {'doShort': 'false', 'resize': ''}
    try:
        req = requests.post('https://fapping.empornium.sx/upload.php', data=data , files=files)
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
            f"{res.get('errorMsg') if 'errorMsg' in res else ''}")
        return None

    if 'image_id_public' not in res or res['image_id_public']=='':
        logger.warning(f"上传图片失败: {res.get('errorMsg')}")
        return None
    picurl='https://fapping.empornium.sx/'+res['image_id_public']
    return GetPicUrl(picurl)

def femp_upload_files(imgpaths: list[str],form:str='img'):
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
                imgstr=femp_upload(imgpath)
                success=1
            except Exception as r:
                success=0
                logger.warning('fapping_emp第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...原因: %s' %(r))
            if imgstr==None:
                success=0
                logger.warning('fapping_emp第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info('fapping_emp第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning('fapping_emp第'+str(imgnum)+'张图片'+imgpath+'上传失败')
    return liststr.strip()




