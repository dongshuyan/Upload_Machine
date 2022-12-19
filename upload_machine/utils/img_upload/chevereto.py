import re
import json
from pathlib import Path
from typing import Optional
import requests
from loguru import logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def url_to_domain(url):
     o = urlparse(url)
     domain = o.hostname
     return domain.split('.')[-2]

def get_token(url:str,cookie:str):
    headers={
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    try:
        response=requests.get(url=url,headers=headers)
    except Exception as r:
        logger.warning('获取token失败，原因: %s' %(r))
        return ''
    content=response.text
    soup=BeautifulSoup(content,'lxml')
    for link in soup.find_all("a"):
        links=link.get("href") 
        if 'auth_token' in links:
            return links[links.find('auth_token')+11:]
    return ''

def chevereto_api_upload(imgpath: str, url: str, api_key: str):
    img  = Path(imgpath)
    data = {'key': api_key}
    files = {'source': open(img, 'rb')}
    try:
        req = requests.post(f'{url}/api/1/upload', data=data, files=files)
    except Exception as r:
        logger.warning('requests 获取失败，原因: %s' %(r))
    try:
        res = req.json()
        logger.trace(res)
    except json.decoder.JSONDecodeError:
        res = {}
    if not req.ok:
        logger.trace(req.content)
        logger.warning(
            f"上传图片失败: HTTP {req.status_code}, reason: {req.reason} "
            f"{res['error'].get('message') if 'error' in res else ''}")
        return None
    if 'error' in res:
        logger.warning(f"上传图片失败: [{res['error'].get('code')}]{res['error'].get('message')}")
        return None
    if 'image' not in res or 'url' not in res['image']:
        logger.warning(f"图片直链获取失败")
        return None
    return res['image']['url']


def chevereto_cookie_upload(imgpath: str, url: str, cookie: str):
    auth_token=get_token(url,cookie)
    if auth_token=='':
        logger.warning('未找到auth_token')
        return None

    img  = Path(imgpath)
    headers = {'cookie': cookie}
    data = {'type': 'file', 'action': 'upload', 'nsfw': 0, 'auth_token': auth_token}
    files = {'source': open(img, 'rb')}

    try:
        req = requests.post(f'{url}/json', data=data, files=files, headers=headers)
    except Exception as r:
        logger.warning('requests 获取失败，原因: %s' %(r))
    try:
        res = req.json()
        logger.trace(res)
    except json.decoder.JSONDecodeError:
        res = {}
    if not req.ok:
        logger.warning(
            f"上传图片失败: HTTP {req.status_code}, reason: {req.reason} "
            f"{res['error'].get('message') if 'error' in res else ''}")
        return None
    if 'error' in res:
        logger.warning(f"上传图片失败: [{res['error'].get('code')}] {res['error'].get('context')} {res['error'].get('message')}")
        return None
    if 'status_code' in res and res.get('status_code') != 200:
        logger.warning(f"上传图片失败: [{res['status_code']}] {res.get('status_txt')}")
        return None 
    if 'image' not in res or 'url' not in res['image']:
        logger.warning(f"图片直链获取失败")
        return None
    return res['image']['url']

def chevereto_api_upload_files(imgpaths: list,url: str, api_key: str, form='img'):
    liststr=''
    imgnum=0
    domain=url_to_domain(url)
    for imgpath in imgpaths:
        imgnum=imgnum+1
        trynum=0
        success=0
        imgstr=''
        while success==0 and trynum<5:
            trynum=trynum+1
            try:
                imgstr=chevereto_api_upload(imgpath,url,api_key)
                success=1
            except Exception as r:
                success=0
                logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...原因: %s' %(r))
            if imgstr==None:
                success=0
                logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info(domain+'第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'上传失败')
    return liststr.strip()

def chevereto_cookie_upload_files(imgpaths: list,url: str, cookie: str, form='img'):
    liststr=''
    imgnum=0
    domain=url_to_domain(url)
    for imgpath in imgpaths:
        imgnum=imgnum+1
        trynum=0
        success=0
        imgstr=''
        while success==0 and trynum<5:
            trynum=trynum+1
            try:
                imgstr=chevereto_cookie_upload(imgpath,url,cookie)
                success=1
            except Exception as r:
                success=0
                logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...原因: %s' %(r))
            if imgstr==None:
                success=0
                logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'第'+str(trynum)+'次上传失败，正在重试...')
        if success==1:
            if form.lower()=='img':
                liststr=liststr+imgstr+'\n'
            elif form.lower()=='bbcode':
                liststr=liststr+'[img]'+imgstr+'[/img]\n'
            else:
                liststr=liststr+imgstr+'\n'
            logger.info(domain+'第'+str(imgnum)+'张图片上传成功！')
        else:
            logger.warning(domain+'第'+str(imgnum)+'张图片'+imgpath+'上传失败')
    return liststr.strip()

#p1="/Users/moyu/Downloads/在线视频十大品牌-视频app排行榜-视频网站排行榜-买购品牌网 (2).png"
#p2="/Users/moyu/Downloads/zhizhu.jpg"
#imgpaths=[p1,p2]
#key='chv_SVbN_71d381f1cefd83182c17337618060ed19f00232f809b12b6f1eeb8f5c5180714b1d0bb2b4b91f265dbbd0c4ea336eb840a637b92bdb7ba41c71c36c862a442a4'
#url='https://www.picgo.net/api/1/upload'
#print(chevereto_api_upload(p,url,key))
#print(chevereto_api_upload_files(imgpaths,url,key,'bbcode'))




#auth_token='5b22483f1d360d3aab9c51ff95e18e0e2fb3aaf2'
#url='https://s3.pterclub.com'
#cookie='KEEP_LOGIN=a4Np%3A575db23e5a8bb04e125711db411b9c18cee2c10dfa6e5ffce3be1d3a068c55c3c93f822a509746e5e84bdb71bc15b87bdf11e1a1361fda194cb5373fd9ff81fbaaef26119313e7a9b7e1aa96fde2032a64b451a87702ca42997bbdf1e7f8f11394991b795c%3A1658856793; PHPSESSID=t6usd4455j8dle6jr71oc6jpkm'
#p='/Users/moyu/Downloads/1.png'
#auth_token='2ff56e94fe9a5e817dfb5a20211df8677d1243f0'
#cookie='PHPSESSID=7a5tf1pcrpttglphd0rlid7rpq; AGREE_CONSENT=1; KEEP_LOGIN=CPT%3A11717c9cc52cbcd96397bd68d2178737bfd4839973ff561f4401af4c59ba84c4b30af45e5b8cb497b4d79e7bb5653f7b670f5bd6be833ae6dc122e63c63c54391e4782918be061dbbcf1776136dbe14c28040551e2730c59c358091cf6fc8625804a1d3647a19bc2%3A1658892099'
#url='https://jerking.empornium.ph'
#print(chevereto_cookie_upload(p,url,cookie,auth_token))





