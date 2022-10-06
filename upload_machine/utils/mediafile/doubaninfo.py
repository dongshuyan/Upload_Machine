import os
from loguru import logger
import time
import requests
import re
import json
import sys
from upload_machine.utils.mediafile.douban_book import *
from upload_machine.utils.mediafile.douban_movie import *

def getdoubaninfo(url:str='',cookie:str=''):
    if 'movie.douban.com' in url:
        if cookie.strip()=='':
            page_parse=MoviePageParse(movie_url=url)
        else:
            page_parse=MoviePageParse(movie_url=url,cookie=cookie)
    elif 'book.douban.com' in url:
        if cookie.strip()=='':
            page_parse=BookPageParse(book_url=url)
        else:
            page_parse=BookPageParse(book_url=url,cookie=cookie)
    else:
        raise Exception('豆瓣链接填写错误')
    print('\n'+page_parse.info())


def ptgen_douban_info(doubanurl):
    url='https://api.iyuu.cn/App.Movie.Ptgen?url='+doubanurl
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {
            'user-agent': user_agent,
            'referer': url,
        }
    logger.info('正在获取豆瓣信息')
    try:
        r = requests.get(url,headers=headers,timeout=20)
    except Exception as r:
        logger.error('获取豆瓣信息失败，原因: %s' %(r))
        return 

    logger.info('获取豆瓣信息完毕，正在处理信息，请稍等...')
    
    try:
        info_json=r.json()
        logger.trace(info_json)
    except Exception as r:
        logger.warning('获取豆瓣信息转换json格式失败，原因: %s' %(r))
        return
    
    if not r.ok:
        logger.trace(r.content)
        logger.warning(
            f"获取豆瓣信息失败: HTTP {r.status_code}, reason: {r.reason} ")
        return 

    if 'data' not in info_json or 'format' not in info_json['data']:
        logger.warning(f"豆瓣信息获取失败")
        return 
    
    info=info_json['data']['format']
    info=info[0:info.find('<a')]
    
    imgurl=re.findall('img[0-9]\.doubanio\.com',info)
    if len(imgurl)>0:
        info=info.replace(imgurl[0],'img9.doubanio.com')
    return info
    
def lemon_douban_info(doubanurl):
    url='https://movieinfo.leaguehd.com/doubanAjax.php?url='+doubanurl
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {
            'user-agent': user_agent,
            'referer': url,
        }
    logger.info('正在获取豆瓣信息，请稍等...')
    try:
        r = requests.get(url,headers=headers,timeout=20)
    except Exception as r:
        logger.warning('通过柠檬获取豆瓣信息失败，原因: %s' %(r))
        return

    logger.info('获取豆瓣信息完毕，正在处理信息，请稍等...')
    try:
        data=r.json()
    except Exception as r:
        logger.warning('通过柠檬获取豆瓣信息转换json格式失败，原因: %s' %(r))
        return

    douban_info=''
    
    if (data['pic']):
        imgurl=re.findall('img[0-9]\.doubanio\.com',data['pic'])
        douban_info = douban_info+"[img]" + data['pic'].replace(imgurl[0],'img9.doubanio.com') + "[/img]\n"
    if (data['allName']):
        douban_info = douban_info+ "\n◎译\u3000\u3000名　" + '/'.join(data['allName']);
    if (data['name']) :
        douban_info += "\n◎片\u3000\u3000名　" + data['name']
    if (data['year']):
        douban_info += "\n◎年\u3000\u3000代　" + data['year']
    if (data['country'] and len(data['country']) > 0) :
        douban_info += "\n◎产\u3000\u3000地　" + " / ".join(data['country'])
    if (data['genre'] and len(data['genre']) > 0):
        douban_info += "\n◎类\u3000\u3000别　" + " / ".join(data['genre'])
    if (data['language'] and len(data['language']) > 0) :
        douban_info += "\n◎语\u3000\u3000言　" + " / ".join(data['language'])
    if (data['release'] and len(data['release']) > 0) :
        douban_info += "\n◎上映日期　" + " / ".join(data['release'])
    if (data['firstRelease'] and len(data['firstRelease']) > 0) :
        douban_info += "\n◎首\u3000\u3000播　" + " / ".join(data['firstRelease'])
    if (data['num']) :
        douban_info += "\n◎集\u3000\u3000数　" + data['num']
    if (data['imdbRating']) :
        douban_info += "\n◎IMDb评分  " + data['imdbRating'] + "/10 from " + data['imdbVotes'] + " users"
    if (data['imdbUrl']) :
        douban_info += "\n◎IMDb链接  " + data['imdbUrl']
    if (data['rating']) :
        douban_info += "\n◎豆瓣评分　" + data['rating'] + "/10 from " + data['votes'] + " users";
    if (data['url']) :
        douban_info += "\n◎豆瓣链接　" + data['url']
    if (data['runtime'] and len(data['runtime']) > 0) :
        douban_info += "\n◎片　　长　" + " / ".join(data['runtime'])

    if (data['director'] and len(data['director']) > 0) :
        for i in range (len(data['director'])):
            if i==0:
                douban_info += "\n◎导　　演　" + (data['director'][i]['name'])
            else:
                douban_info += "\n　　　　　  " + (data['director'][i]['name'])

    if (data['writer'] and len(data['writer']) > 0) :
        for i in range (len(data['writer'])):
            if i==0:
                douban_info += "\n◎编　　剧　" + (data['writer'][i]['name'])
            else:
                douban_info += "\n　　　　　  " + (data['writer'][i]['name'])

    if (data['cast'] and len(data['cast']) > 0) :
        for i in range (len(data['cast'])):
            if i==0:
                douban_info += "\n◎主　　演　" + (data['cast'][i]['name'])
            else:
                douban_info += "\n　　　　　  " + (data['cast'][i]['name'])

    if (data['tags'] and len(data['tags']) > 0) :
        douban_info += "\n\n\n◎标　　签　" + " | ".join(data['tags'])
    if (data['plot']) :
        douban_info=douban_info[0:douban_info.find('<a')]
        plotstr=data['plot']
        plotstr=plotstr[0:plotstr.find('<a')]
        douban_info += "\n\n◎简　　介　" + "\n\n " +(plotstr)

    if (data['awards'] and len(data['awards']) > 0) :
        awardstr=''
        for item in data['awards']:
            awardstr=awardstr+"\n\n　　" + item['title'];
            for itemc in item['content']:
                awardstr=awardstr+"\n　　" + itemc
        douban_info += "\n\n◎获奖情况　" + awardstr

    douban_info =douban_info+ "\n\n"
    return douban_info


def doubaninfo(doubanurl):
    res=None
    trynum=0
    while res==None:
        trynum=trynum+1
        if trynum>10:
            print('获取失败')
            return 
        res=ptgen_douban_info(doubanurl)
        if res==None:
            res=lemon_douban_info(doubanurl)
        if res==None:
            time.sleep(3)
    print('\n'+res)
    return 




