import os
from loguru import logger
from upload_machine.utils.img_upload.chevereto import chevereto_api_upload_files,chevereto_cookie_upload_files
from upload_machine.utils.img_upload.ptpimg import ptpimg_upload_files
from upload_machine.utils.img_upload.smms import smms_upload_files
from upload_machine.utils.img_upload.fapping_emp import femp_upload_files
from upload_machine.utils.img_upload.imgbox import imgbox_upload_files


def existitem(imgdata,item):
    if item in imgdata and not(imgdata[item]=='') and not imgdata[item]==None:
        return True
    return False

def createimgdict(imgdata):
    imgdict=dict()
    imghostlist=['ptpimg','picgo','smms','pter','emp','femp','imgbox','chd','freeimage']
    for item in imghostlist:
        imgdict[item]=False
    if existitem(imgdata,'ptpimg') and existitem(imgdata['ptpimg'],'apikey'):
        imgdict['ptpimg']=True
    if existitem(imgdata,'picgo') and existitem(imgdata['picgo'],'apikey') and existitem(imgdata['picgo'],'url') :
        imgdict['picgo']=True
    if existitem(imgdata,'smms') and existitem(imgdata['smms'],'apikey'):
        imgdict['smms']=True
    if existitem(imgdata,'pter')  and existitem(imgdata['pter'],'url') and existitem(imgdata['pter'],'cookie') :
        imgdict['pter']=True
    if existitem(imgdata,'emp')  and existitem(imgdata['emp'],'url') and existitem(imgdata['emp'],'cookie') :
        imgdict['emp']=True
    if existitem(imgdata,'chd')  and existitem(imgdata['chd'],'url') and existitem(imgdata['chd'],'cookie') :
        imgdict['chd']=True
    if existitem(imgdata,'freeimage')  and existitem(imgdata['freeimage'],'url') and existitem(imgdata['freeimage'],'cookie') :
        imgdict['freeimage']=True
    imgdict['femp']=True
    imgdict['imgbox']=True
    listnum=1
    seq=[]
    while (existitem(imgdata['seq'],(listnum))):
        seq.append(imgdata['seq'][(listnum)])
        listnum=listnum+1
    return imgdata,imgdict,seq

def img_upload_seq(imgdata,seq:list[str],imglist:list[str],form:str='img'):
    for i in range(len(seq)):
        res=img_upload(imgdata=imgdata,imglist=imglist,host=seq[i],form=form,fail=True)
        if not (res==''):
            return res

def img_upload(imgdata,imglist:list[str],host:str='',form:str='img',fail:bool=False,chevereto_url:str='',chevereto_apikey:str='',chevereto_cookie:str=''):
    imgdata,imgdict,seq=createimgdict(imgdata)
    success=True
    res=''
    if host=='':
    	host=seq[0]
    if 'ptpimg'in host.lower():
        host='ptpimg'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=ptpimg_upload_files(imgpaths=imglist,api_key=imgdata[host]['apikey'],form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'picgo' in host.lower():
        host='picgo'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=chevereto_api_upload_files(imgpaths=imglist,url=imgdata[host]['url'].strip('/'),api_key=imgdata[host]['apikey'],form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'smms' in host.lower():
        host='smms'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=smms_upload_files(imgpaths=imglist,api_key=imgdata[host]['apikey'],form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'pter' in host.lower():
        host='pter'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=chevereto_cookie_upload_files(imgpaths=imglist,url=imgdata[host]['url'].strip('/'), cookie=imgdata[host]['cookie'], form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'femp' in host.lower():
        host='femp'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=femp_upload_files(imgpaths=imglist, form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'emp' in host.lower():
        host='emp'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=chevereto_cookie_upload_files(imgpaths=imglist,url=imgdata[host]['url'].strip('/'), cookie=imgdata[host]['cookie'], form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'imgbox' in host.lower():
        host='imgbox'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=imgbox_upload_files(imgpaths=imglist, form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'chd' in host.lower():
        host='chd'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=chevereto_cookie_upload_files(imgpaths=imglist,url=imgdata[host]['url'].strip('/'), cookie=imgdata[host]['cookie'], form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'freeimage' in host.lower():
        host='freeimage'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=chevereto_cookie_upload_files(imgpaths=imglist,url=imgdata[host]['url'].strip('/'), cookie=imgdata[host]['cookie'], form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'chevereto_api' in host.lower():
        host='chevereto_api'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if not (chevereto_url=='' or chevereto_apikey==''):
            res=chevereto_api_upload_files(imgpaths=imglist,url=chevereto_url,api_key=chevereto_apikey,form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    elif 'chevereto_cookie' in host.lower():
        host='chevereto_cookie'
        logger.info('正在尝试使用'+host+'上传图片,请稍等...')
        if not (chevereto_url=='' or chevereto_cookie==''):
            res=chevereto_cookie_upload_files(imgpaths=imglist,url=chevereto_url, cookie=chevereto_cookie, form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    else:
        host='ptpimg'
        logger.info('未找到该图床，正在尝试使用'+host+'上传图片,请稍等...')
        if imgdict[host]==True:
            res=ptpimg_upload_files(imgpaths=imglist,api_key=imgdata[host]['apikey'],form=form)
        else:
            success=False
            logger.warning('图床'+host+'配置信息缺失')
        if res=='':
            success=False
    if success:
        logger.info('上传成功！')
        return res
    else:
        logger.warning('上传失败！')
        if fail==False:
            return img_upload_seq(imgdata=imgdata,seq=seq,imglist=imglist,form=form)
        else:
            return ''
