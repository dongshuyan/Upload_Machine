from upload_machine.utils.para_ctrl.readyaml import readyaml
from upload_machine.utils.para_ctrl.readargs import readargs
from upload_machine.utils.para_ctrl.readyaml import write_yaml
import os
from loguru import logger

def read_para():
    args = readargs()

    iu=0#img upload
    su=0#sign
    ru=0#resources upload
    if not args.img_upload+args.sign+args.upload+args.douban_info+args.media_img==1:
        logger.error('参数输入错误，上传模式 -u,签到模式 -s,上传图床模式 -iu,获取豆瓣信息 -di, 获取视频截图链接 -mi, 必须且只能选择一个。')
        raise ValueError ('参数输入错误，上传模式 -u,签到模式 -s,上传图床模式 -iu,获取豆瓣信息 -di, 获取视频截图链接 -mi, 必须且只能选择一个。')


    au_data   = readyaml(args.yaml_path)
    basic_data = readyaml(args.basic_path)
    merge_para(basic_data,au_data)

    if 'basic' in au_data and 'workpath' in au_data['basic']:
        if not os.path.exists(au_data['basic']['workpath']):
            logger.info('检测到workpath目录并未创建，正在新建文件夹：'+au_data['basic']['workpath'])
            os.makedirs(au_data['basic']['workpath'])
        itemlist=['record_path','screenshot_path']
        for item in itemlist:
            if not item in au_data['basic']:
                au_data['basic'][item]=os.path.join(au_data['basic']['workpath'],item)
                if not os.path.exists(au_data['basic'][item]):
                    logger.info('检测到'+item+'目录并未创建，正在新建文件夹：'+au_data['basic'][item])
                    os.makedirs(au_data['basic'][item])

    au_data['yaml_path']=args.yaml_path
    write_yaml(au_data)
    
    au_data['mod']=args.media_img*'media_img'+args.img_upload*'img_upload'+args.sign*'sign'+args.upload*'upload'+args.douban_info*'douban_info'

    if args.upload:
        if not 'path info' in au_data or len(au_data['path info'])==0:
            logger.error('参数输入错误，发布资源请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，发布资源请至少输入一个本地文件地址')
        for item in au_data['path info']:
            if not 'path' in au_data['path info'][item] or au_data['path info'][item]['path']==None or au_data['path info'][item]['path']=='':
                logger.error('参数输入错误，'+item+'请至少输入一个本地文件地址')
                raise ValueError ('参数输入错误，'+item+'请至少输入一个本地文件地址')
            if 'type' in au_data['path info'][item] and not ( 'anime' in au_data['path info'][item]['type'].lower() or 'tv' in au_data['path info'][item]['type'].lower() or 'movie' in au_data['path info'][item]['type'].lower()):
                logger.error('参数输入错误，'+item+'的type类型暂不支持')
                raise ValueError ('参数输入错误，'+item+'的type类型暂不支持')
        if not 'qbinfo' in au_data:
            logger.error('参数输入错误，未找到qbinfo')
            raise ValueError ('参数输入错误，未找到qbinfo')
        if not 'start' in au_data['qbinfo'] or not (int(au_data['qbinfo']['start'])==1 or int(au_data['qbinfo']['start'])==0):
            au_data['qbinfo']['start']=0
            logger.warning('未找到qbinfo中的start(添加到qb的种子是否自动开始)参数,已设置为0(不自动开始)')



    
    if args.img_upload:
        if 'img_host' in args and not args.img_host=='':
            au_data['img_host']=args.img_host
        else:
            au_data['img_host']=''

        if 'img_form' in args and not args.img_form=='':
            au_data['img_form']=args.img_form
        else:
            au_data['img_form']='img'

        filelist=[]
        if 'img_file' in args and args.img_file==None:
            logger.error('参数输入错误，上传图片请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，上传图片请至少输入一个本地文件地址')
        for item in args.img_file:
            for imgitem in item:
                if not imgitem in filelist:
                    filelist.append(imgitem)
        if len(filelist)==0:
            logger.error('参数输入错误，上传图片请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，上传图片请至少输入一个本地文件地址')
        au_data['imgfilelist']=filelist

    if args.douban_info:
        
        if not 'douban_url' in args or ( args.douban_info==None or args.douban_info==''):
            logger.error('参数输入错误，请输入--douban-url 豆瓣链接')
            raise ValueError ('参数输入错误，请输入--douban-url 豆瓣链接')
        
        au_data['douban_url']=args.douban_url

    if args.media_img:

        if not 'media_file' in args or ( args.media_file==None or args.media_file==''):
            logger.error('参数输入错误，请输入media-file 视频文件路径')
            raise ValueError ('参数输入错误，请输入media-file 视频文件路径')

        if not 'basic' in au_data or not 'picture_num' in au_data['basic'] or ( au_data['basic']['picture_num']==None or au_data['basic']['picture_num']==''):
            logger.warning('未找到yaml文件中截图数量参数picture_num,已设置为3')
            if not 'basic' in au_data:
                au_data['basic']=dict()
            au_data['basic']['picture_num']=3

        if not 'basic' in au_data or not 'screenshot_path' in au_data['basic'] or ( au_data['basic']['screenshot_path']==None or au_data['basic']['screenshot_path']==''):
            logger.error('参数输入错误，请前往yaml文件配置截图路径参数screenshot_path')
            raise ValueError ('参数输入错误，请前往yaml文件配置截图路径参数screenshot_path')

        if 'img_host' in args and not args.img_host=='':
            au_data['img_host']=args.img_host
        else:
            au_data['img_host']=''

        if 'img_form' in args and not args.img_form=='':
            au_data['img_form']=args.img_form
        else:
            au_data['img_form']='img'

        if 'img_num' in args and not (args.img_num=='' or args.img_num==None) :
            au_data['basic']['picture_num']=int(args.img_num)



        au_data['media_file']=args.media_file







    return au_data

def merge_para(dict1,dict2):
    '''
    将dict1中的内容合并入dict2,如果有相同内容保持dict2
    '''
    if not (type(dict1)==dict and type(dict2)==dict):
        return 
    for item in dict1:
        if item in dict2:
            merge_para(dict1[item],dict2[item])
        else:
            dict2[item]=dict1[item]

