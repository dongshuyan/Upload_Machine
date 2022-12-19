import json
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import requests
from loguru import logger
import os

def redleaves_upload(imgpath: str):
    file = {"file" : (os.path.basename(imgpath), open(imgpath,'rb'),'image/'+os.path.splitext(imgpath)[-1])}
    r = requests.post('https://img.leaves.red/api/v1/upload',files=file)
    if r.status_code == 200:
        res = json.loads(r.text)
        if res['status']:
            logger.info(f'Uploading image succeed!')
            return res['data']['links']['url']
    logger.error(f'Redleaves uploading image failed:'+str(r.status_code))
    return None

def redleaves_upload_files(imgpaths: list[str], form='img'):
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
                imgstr=redleaves_upload(imgpath)
                success=1
            except Exception as r:
                success=0
                logger.warning('redleaves第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，失败原因: %s\n正在重试...' %(r))
            if imgstr==None:
                success=0
                logger.warning('Redleaves第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info('Redleaves第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning('Redleaves第'+str(imgnum)+'张图片'+imgpath+'上传失败')
            return ''
    return liststr.strip()
