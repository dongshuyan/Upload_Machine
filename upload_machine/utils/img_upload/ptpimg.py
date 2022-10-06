import json
from pathlib import Path
import requests
from urllib.parse import urlparse
from loguru import logger

def ptpimg_upload(imgpath: str, api_key: str):
    img  = Path(imgpath)
    data = {'api_key': api_key}
    files = {'file-upload[0]': open(img, 'rb')}
    try:
        req = requests.post('https://ptpimg.me/upload.php', data=data, files=files)
    except Exception as r:
        logger.warning('requests 获取失败，原因: %s' %(r))
        return None
    try:
        res = req.json()
    except json.decoder.JSONDecodeError:
        res = {}
    if not req.ok:
        logger.warning(req.content)
        logger.warning(f"上传图片失败: HTTP {req.status_code}, reason: {req.reason}")
        return None
    if len(res) < 1 or 'code' not in res[0] or 'ext' not in res[0]:
        logger.warning(f"图片直链获取失败")
        return None
    return f"https://ptpimg.me/{res[0].get('code')}.{res[0].get('ext')}"


def ptpimg_upload_files(imgpaths: list, api_key: str, form='img'):
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
                imgstr=ptpimg_upload(imgpath,api_key)
                success=1
            except Exception as r:
                success=0
                logger.warning('PTPIMG第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，失败原因: %s\n正在重试...' %(r))
            if imgstr==None:
                success=0
                logger.warning('PTPIMG第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info('PTPIMG第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning('PTPIMG第'+str(imgnum)+'张图片'+imgpath+'上传失败')
            return ''
    return liststr.strip()
    

#p1="/Users/moyu/Downloads/在线视频十大品牌-视频app排行榜-视频网站排行榜-买购品牌网 (2).png"
#p2="/Users/moyu/Downloads/zhizhu.jpg"
#imgpaths=[p1,p2]
#key='de2a51b1-d5fc-45d0-8429-9c53a0c36468'
#print(ptpimg_upload(p,key))
#print(ptpimg_upload_files(imgpaths,key,'bbcode'))





