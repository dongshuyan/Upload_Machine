import json
from pathlib import Path
import requests
from loguru import logger


def sharkimg_upload(imgpath: str, token: str):
    img = Path(imgpath)
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}

    files = {'file': open(img, 'rb')}
    try:
        req = requests.post('https://img.sharkpt.net/api/v1/upload', headers=headers, files=files)
        req.encoding = 'utf-8'
    except Exception as r:
        logger.warning('requests 获取失败，原因: %s' % (r))
        return None
    try:
        res = req.json()
    except json.decoder.JSONDecodeError:
        res = {}
    if not req.ok or ('status' in res and res['status'] != True):
        logger.warning(req.content)
        logger.warning(f"上传图片失败: HTTP {req.status_code}, reason: {res.message}")
        return None
    if 'data' not in res or 'links' not in res['data'] or 'url' not in res['data']['links']:
        logger.warning(f"图片直链获取失败")
        return None
    return res['data']['links']['url']


def sharkimg_upload_files(imgpaths: list, token: str, form='img'):
    liststr = ''
    imgnum = 0
    for imgpath in imgpaths:
        imgnum = imgnum + 1
        trynum = 0
        success = 0
        imgstr = ''
        while success == 0 and trynum < 5:
            trynum = trynum + 1
            try:
                imgstr = sharkimg_upload(imgpath, token)
                success = 1
            except Exception as r:
                success = 0
                logger.warning('SHARKIMG第' + str(imgnum) + '张图片' + imgpath + '第' + str(trynum) +
                               '次上传失败，失败原因: %s\n正在重试...' % (r))
            if imgstr == None:
                success = 0
                logger.warning('SHARKIMG第' + str(imgnum) + '张图片' + imgpath + '第' + str(trynum) + '次上传失败，正在重试...')
        if success == 1:
            if form.lower() == 'img':
                liststr = liststr + imgstr + '\n'
            elif form.lower() == 'bbcode':
                liststr = liststr + '[img]' + imgstr + '[/img]\n'
            else:
                liststr = liststr + imgstr + '\n'
            logger.info('SHARKIMG第' + str(imgnum) + '张图片上传成功！')
        else:
            logger.warning('SHARKIMG第' + str(imgnum) + '张图片' + imgpath + '上传失败')
            return ''
    return liststr.strip()