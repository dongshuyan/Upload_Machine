import os
from loguru import logger
from urllib.parse import quote
from urllib.parse import unquote
import re
import requests
from upload_machine.utils.para_ctrl.readyaml import write_yaml
from shutil import move

def findnum(name):
    num=re.findall(r" ([0-9]{1,2}) ",name)
    if len(num)!=0:
        sty=" "+num[0]+" "
        stz=" XX "
        stx=" "+num[0]+" "
        return num[0],sty,stz,stx
    num=re.findall(r"第([0-9]{1,2})話",name)
    if len(num)!=0:
        sty='第'+num[0]+'話'
        stz="第XX話"
        stx='第'+num[0]+'話'
        return num[0],sty,stz,stx
    num=re.findall(r"第([0-9]{1,2})话",name)
    if len(num)!=0:
        sty='第'+num[0]+'话'
        stz="第XX话"
        stx='第'+num[0]+'话'
        return num[0],sty,stz,stx
    num=re.findall(r"E([0-9]{1,2})",name)
    if len(num)!=0:
        sty='第'+num[0]+'话'
        stz="第XX话"
        stx='第'+num[0]+'话'
        return num[0],sty,stz,stx
    num=re.findall(r"_([0-9]{1,2})_",name)
    if len(num)!=0:
        sty='_'+num[0]+'_'
        stz="_XX_"
        stx='_'+num[0]+'_'
        return num[0],sty,stz,stx
    num=re.findall(r"\[([0-9]{1,2})\D",name)
    if len(num)!=0:
        sty="\["+num[0]+"\]"
        stz="[XX]"
        stx="["+num[0]+"]"
        return num[0],sty,stz,stx
    num=re.findall(r"\D([0-9]{1,2})\]",name)
    if len(num)!=0:
        sty="\["+num[0]+"\]"
        stz="[XX]"
        stx="["+num[0]+"]"
        return num[0],sty,stz,stx
    num=re.findall(r"-([0-9]{1,2})\D",name)
    if len(num)!=0:
        sty='-'+num[0]
        stz="-XX"
        stx="-"+num[0]
        return num[0],sty,stz,stx
    num=re.findall(r"\D([0-9]{1,2})\D",name)
    if len(num)!=0:
        sty=num[0]
        stz="XX"
        stx=num[0]
        return num[0],sty,stz,stx  
    
    num=re.findall(r"([0-9]{1,2})",name)
    if len(num)!=0:
        sty=num[0]
        stz="XX"
        stx=num[0]
        return num[0],sty,stz,stx     
    return '-1','-1','XX','-1'

def finddoubanurl(name):
    logger.info('正在寻找 '+name+' 的豆瓣链接，请稍等...')
    url_encode_name = quote(name.replace(' ',''))
    url='https://www.douban.com/search?q='+url_encode_name
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {
            'user-agent': user_agent,
            'referer': url,
            }
    r=requests.models.Response()
    try:
        r = requests.get(url,headers=headers,timeout=30)
    except:
        logger.warning('寻找豆瓣链接失败')
        
    for item in re.findall('/?url=(.*)%2F',r.text):
        item=unquote(item)
        if ('movie.douban.com'in item) and ('/subject/' in item or '/movie/' in item) :
            logger.info('已找到 '+name+' 的豆瓣链接为:\n'+item+'\n')
            res=input('请确认豆瓣链接正确性,如果正确回复y,否则回复正确的豆瓣链接:\n')
            if res.strip().lower()=='y':
                logger.info('已确认 '+name+' 的豆瓣链接为:'+item+'\n')
                return item
            else :
                logger.info('已确认 '+name+' 的豆瓣链接为:'+res+'\n')
                return res
    return ''

def findbgmurl(name):
    logger.info('正在寻找 '+name+' 的Bangumi链接，请稍等...')
    url_encode_name = quote(name)
    url='https://bgm.tv/subject_search/'+url_encode_name+'?cat=2'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {
            'user-agent': user_agent,
            'referer': url,
            }
    r = requests.get(url,headers=headers,timeout=30)
    ans=re.findall('href="/subject/(\d*)',r.text)
    if len(ans)>0:
        logger.info('已找到 '+name+' 的Bangumi链接为:\n'+'https://bgm.tv/subject/'+ans[0]+'\n')
        res=input('请确认Bangumi链接正确性,如果正确回复y,否则回复正确的Bangumi链接,若不需要则直接输入回车:\n')
        if res.strip().lower()=='y':
            logger.info('已确认 '+name+' 的Bangumi链接为:'+'https://bgm.tv/subject/'+ans[0]+'\n')
            return 'https://bgm.tv/subject/'+ans[0]
        else :
            logger.info('已确认 '+name+' 的Bangumi链接为:'+res+'\n')
            return res
    return ''

def findeps(pathlist):
    eps=[]
    for path in pathlist:
        if not os.path.exists(path):
            continue
        ls = os.listdir(path)
        ls.sort()
        for i in ls:
            c_path = os.path.join(path, i)
            if (os.path.isdir(c_path)) or (i.startswith('.')) or (not(  os.path.splitext(i)[1].lower()== ('.mp4') or os.path.splitext(i)[1].lower()== ('.mkv')  or os.path.splitext(i)[1].lower()== ('.avi') or os.path.splitext(i)[1].lower()== ('.ts')    )):
                continue
            epnum=int(findnum(i)[0])
            if epnum==-1:
                logger.error(c_path+' 这个文件，文件名为:'+i+',没找到集数信息，请用户检查，如果确定是程序没有抽取成功请联系作者')
                raise ValueError (c_path+' 这个文件，文件名为:'+i+',没找到集数信息，请用户检查，如果确定是程序没有抽取成功请联系作者')
            if not epnum in eps:
                eps.append(epnum)
    eps.sort()
    return eps





class pathinfo(object):
    def __init__(self,pathid,infodict,sites,basic):
        self.pathid=pathid
        self.sites=[]
        self.exclusive=[]
        self.infodict=infodict
        self.max=1
        self.min=1
        #必须有的属性
        attr_must=['path','chinesename','englishname','sub']
        for item in attr_must:
            if not item in infodict or infodict[item]==None:
                logger.error('未识别'+pathid+' 中的'+item+'信息')
                raise ValueError ('未识别'+pathid+' 中的'+item+'信息')
            else:
                exec('self.'+item+'=infodict[item]')
                exec('self.exist_'+item+'=True')

        

        #可有可无的属性,后面写入配置文件
        attr_disp=['type','collection','complete','enable','doubanurl']
        for item in attr_disp:
            if not item in infodict or infodict[item]==None:
                exec('self.'+item+'=""')
                exec('infodict[item]=None')
                exec('self.exist_'+item+'=False')
            else:
                exec('self.'+item+'=infodict[item]')
                exec('self.exist_'+item+'=True')

        #可有可无的属性,后面不写入配置文件
        attr_disp=['video_type','video_format','audio_format','year','zeroday_name','exinfo','seasonnum','imdb_url','bgm_url','anidb_url','transfer','txt_info','audio_info','from_url','contenttail','contenthead','screenshot','small_descr']
        for item in attr_disp:
            if not item in infodict or infodict[item]==None:
                exec('self.'+item+'=""')
                exec('self.exist_'+item+'=False')
            else:
                exec('self.'+item+'=infodict[item]')
                exec('self.exist_'+item+'=True')
        
        
        pathstr=os.path.basename(self.path)
        if (self.exist_chinesename and self.exist_englishname and self.exist_sub):
            if self.exinfo!='':
                self.exinfo='['+self.exinfo+']'
            if self.seasonnum=='':
                self.seasonnum=1
                self.season='S01'
            else:
                try:
                    self.seasonnum=int(self.seasonnum)
                    self.season='S'+str(self.seasonnum).zfill(2)
                except:
                    logger.error('季度输入错误')
                    raise ValueError (pathid+'季度输入错误')

        elif   (len(pathstr.split('-'))==4)  :

            path1=os.path.basename(self.path)
            if self.seasonnum!='':
                try:
                    self.seasonnum=int(self.seasonnum)
                    self.season='S'+str(self.seasonnum).zfill(2)
                except:
                    logger.error('季度输入错误')
                    raise ValueError (pathid+'季度输入错误')
            if self.sub=='':
                self.sub               = path1.split('-')[-1].strip()
                infodict['sub']=self.sub
            if self.englishname=='': 
                self.englishname       = path1.split('-')[-2].strip()
                seasons=re.findall("S[0-9]{1,2}",self.englishname) 
                if len(seasons)==0 and self.seasonnum=='':
                    self.season='S01'
                    self.seasonnum=1

                else:
                    if self.seasonnum=='':
                        self.seasonnum=int(seasons[0][1:])
                        self.season='S'+str(self.seasonnum).zfill(2)
                        infodict['seasonnum']=self.seasonnum
                    self.englishname=self.englishname.replace(self.season,'').strip()
                infodict['englishname']=self.englishname
            if self.chinesename=='':
                self.chinesename       =path1.split('-')[-3].strip()
                if len(re.findall("第.*季",self.chinesename))>0:
                    self.chinesename=self.chinesename.replace(re.findall("第.*季",self.chinesename)[0],'')
                    self.chinesename=self.chinesename.strip()
                infodict['chinesename']=self.chinesename
            if self.exinfo=='':
                self.exinfo            =re.findall('\[.*\]',pathstr.split('-')[0].strip())
                if len(self.exinfo)>0:
                    self.exinfo=self.exinfo[0]
                    infodict['exinfo']=self.exinfo
                else:
                    self.exinfo=''
            else:
                self.exinfo='['+self.exinfo+']'

            

        else:
            logger.error(pathid+' 信息异常，中文名，英文名，制作小组名有缺失，请补齐后重发')
            raise ValueError (pathid+' 信息异常，中文名，英文名，制作小组名有缺失，请补齐后重发')
        
        pathitem=self.chinesename

        if not self.exist_type:
            logger.warning('未识别路径'+infodict['path']+'的type（资源类型）信息')
            res=100
            while not(res>0 and res<4):
                res=input('请输入资源类型对应的数字:\n1.动漫 2.电视剧 3.电影\n')
                try:
                    res=int(res)
                except:
                    res=100
                if not(res>0 and res<4):
                    logger.warning('输入有误，请重新输入')
            if res==1:
                self.type='anime'
                infodict['type']='anime'
            elif res==2:
                self.type='tv'
                infodict['type']='tv'
            elif res==3:
                self.type='movie'
                infodict['type']='movie'
            else:
                logger.error(pathid+' 中type(资源类型)输入错误')
                raise ValueError (pathid+' 中type(资源类型)输入错误')


        self.downloadpath=''
        if not 'downloadpath' in infodict or infodict['downloadpath']==None:
            if (self.collection or 'movie' in self.type) == 1 and ('new_folder' in basic and basic['new_folder']==0):
                self.downloadpath=os.path.dirname( self.path)
            else:
                self.downloadpath=self.path
        else:
            self.downloadpath=infodict['downloadpath']

        self.category=None
        if not 'category' in infodict or infodict['category']==None:
            self.category=None
        else:
            self.category=infodict['category']

        if self.complete=='':
            self.complete=0
        else:
            self.complete=int(self.complete)

        
        if ('anime' in self.type or 'tv' in self.type) and not self.exist_collection:
            res=100
            while not(res==0 or res==1):
                res=input('未识别路径'+pathid+'的collection（资源是否按合集发布）信息,请重新输入选项对应的数字:\n0:发布单集,1:发布合集\n')
                try:
                    res=int(res)
                except:
                    res=100
                if not(res==0 or res==1):
                    logger.warning('输入有误，请重新输入')
            if res==0:
                self.collection =0
                infodict['collection']=0
            elif res==1:
                self.collection =1
                infodict['collection']=1
            else:
                logger.error('未识别路径'+pathid+'的collection（资源是否按合集发布）信息')
                raise ValueError ('未识别路径'+pathid+'的collection（资源是否按合集发布）信息')


        if self.exist_enable:
            try:
                self.enable =int(self.enable)
            except:
                logger.warning('未识别路径'+pathid+'的enable（资源是否发布）信息,已设置为0（不发）')
                self.enable =0
                infodict['enable']=0
            if not (self.enable==0 or self.enable==1):
                logger.warning('未识别路径'+pathid+'的enable（资源是否发布）信息,已设置为0（不发）')
                self.enable =0
                infodict['enable']=0
        else:
            logger.warning('未识别路径'+pathid+'的enable（资源是否发布）信息,已设置为0（不发）')
            self.enable =0
            infodict['enable']=0

        if self.exist_collection:
            try:
                self.collection =int(self.collection)
            except:
                logger.warning('未识别路径'+pathid+'的collection（资源是否以合集发布）信息,已设置为0（单集发布）')
                self.collection =0
                infodict['collection']=0
            if not (self.collection==0 or self.collection==1):
                logger.warning('未识别路径'+pathid+'的collection（资源是否以合集发布）信息,已设置为0（单集发布）')
                self.collection =0
                infodict['collection']=0
        else:
            logger.warning('未识别路径'+pathid+'的collection（资源是否以合集发布）信息,已设置为0（单集发布）')
            self.collection =0
            infodict['collection']=0

        if self.exist_transfer:
            try:
                self.transfer =int(self.transfer)
            except:
                logger.warning('未识别路径'+pathid+'的transfer(资源是否为转载)信息,已设置为1（默认资源为转载）')
                self.transfer =1
                infodict['transfer']=1
            if not (self.transfer==0 or self.transfer==1):
                logger.warning('未识别路径'+pathid+'的transfer(资源是否为转载)信息,已设置为1（默认资源为转载）')
                self.transfer =1
                infodict['transfer']=1
        else:
            logger.warning('未识别路径'+pathid+'的transfer(资源是否为转载)信息,已设置为1（默认资源为转载）')
            self.transfer =1
            infodict['transfer']=1

        if self.transfer==1 and not self.exist_from_url:
            logger.warning('未识别路径'+pathid+'from_url(转载资源原链接)信息')
            self.from_url = 'https://mikanani.me/'
            infodict['from_url']='https://mikanani.me/'

        if self.exist_complete:
            try:
                self.complete =int(self.complete)
            except:
                logger.warning('未识别路径'+pathid+'的complete(资源是否为完结)信息,已设置为0（未完结）')
                self.complete =0
                infodict['complete']=0
            if not (self.complete==0 or self.complete==1):
                logger.warning('未识别路径'+pathid+'的complete(资源是否为完结)信息,已设置为0（未完结）')
                self.complete =0
                infodict['complete']=0
        else:
            logger.warning('未识别路径'+pathid+'的complete(资源是否为完结)信息,已设置为0（未完结）')
            self.complete =0
            infodict['complete']=0
            


        
        for siteitem in sites:
            if sites[siteitem].enable==0:
                continue
            self.sites.append(siteitem)
            if (not siteitem in infodict) or (infodict[siteitem]==None):
                logger.warning('未找到路径'+pathitem+'在'+siteitem+'的站点信息,已设置为不发')
                exec('self.'+siteitem+'_done=[]')
                exec('self.'+siteitem+'_max_done=10000')
                exec('self.'+siteitem+'_min_done=-1')
                infodict[siteitem]=None
            else:
                exec('self.'+siteitem+'_done='+'str(infodict[siteitem]).split(",")')
                exec('self.'+siteitem+'_max_done=-1')
                exec('self.'+siteitem+'_min_done=10000')
                for i in range(eval('len(self.'+siteitem+'_done)')):
                    #self.done[i]= int(self.done[i])
                    exec('self.'+siteitem+'_done[i]='+'int(self.'+siteitem+'_done[i])')
                    if eval('self.'+siteitem+'_done[i]>self.'+siteitem+'_max_done'):
                        exec('self.'+siteitem+'_max_done=self.'+siteitem+'_done[i]')
                    if eval('self.'+siteitem+'_done[i]<self.'+siteitem+'_min_done'):
                        exec('self.'+siteitem+'_min_done=self.'+siteitem+'_done[i]')
                exec('self.'+siteitem+'_done.sort()')
        
        if 'exclusive' in infodict and infodict['exclusive']!=None:
            self.exclusive=infodict['exclusive'].split(",")
            self.exclusive=[i.strip().lower() for i in self.exclusive]

        season_ch=''
        season_ch=season_ch+'第'
        if self.seasonnum==1:
            season_ch=season_ch+'一'
        elif self.seasonnum==2:
            season_ch=season_ch+'二'
        elif self.seasonnum==3:
            season_ch=season_ch+'三'
        elif self.seasonnum==4:
            season_ch=season_ch+'四'
        elif self.seasonnum==5:
            season_ch=season_ch+'五'
        elif self.seasonnum==6:
            season_ch=season_ch+'六'
        elif self.seasonnum==7:
            season_ch=season_ch+'七'
        elif self.seasonnum==8:
            season_ch=season_ch+'八'
        elif self.seasonnum==9:
            season_ch=season_ch+'九'
        elif self.seasonnum==10:
            season_ch=season_ch+'十'
        elif self.seasonnum==11:
            season_ch=season_ch+'十一'
        elif self.seasonnum==12:
            season_ch=season_ch+'十二'
        elif self.seasonnum==13:
            season_ch=season_ch+'十三'
        elif self.seasonnum==14:
            season_ch=season_ch+'十四'
        elif self.seasonnum==15:
            season_ch=season_ch+'十五'
        else:
            season_ch=season_ch+str(self.seasonnum)
        season_ch=season_ch+'季'
        self.season_ch=season_ch
        
        if ('anime' in self.type.lower() or 'tv' in self.type.lower()):
            
            

            if self.zeroday_name=='':
                self.eps=findeps([self.path])
            else:
                self.eps=findeps([self.path,os.path.join(self.path,self.zeroday_name)])
            if (len(self.eps)<1):
                raise Exception('路径'+pathid+' : '+self.infodict['path']+'中没找到视频文件')
            self.min=self.eps[0]
            self.max=self.eps[-1]
            '''
            if (not self.exist_bgm_url) and 'anime' in self.type:
                if self.seasonnum>1:
                    self.bgm_url=findbgmurl(self.chinesename.strip()+' '+self.season_ch.strip())
                else:
                    self.bgm_url=findbgmurl(self.chinesename.strip())
                if self.bgm_url=='':
                    #logger.error('未找到 '+self.chinesename+' 对应的Bangumi地址。')
                    logger.warning('未找到 '+self.chinesename+' 对应的Bangumi地址。暂设置为空，如果需要请手动前往au.yaml设置')
                    infodict['bgm_url']=None
                else:
                    infodict['bgm_url']=self.bgm_url
            '''

        if (not self.exist_doubanurl):
            if ('anime' in self.type or 'tv' in self.type):
                if self.seasonnum>1:
                    self.doubanurl=finddoubanurl(self.chinesename.strip()+' '+self.season_ch.strip())
                else:
                    self.doubanurl=finddoubanurl(self.chinesename.strip())
            else:
                self.doubanurl=finddoubanurl(self.chinesename.strip())
            if self.doubanurl=='':
                logger.warning('未找到 '+self.chinesename+' 对应的豆瓣地址')
                res=input('未找到 '+self.chinesename+' 对应的豆瓣地址。请手动输入正确的豆瓣链接:\n')
                self.doubanurl=res
                infodict['doubanurl']=res
            else:
                infodict['doubanurl']=self.doubanurl




        if ('anime' in self.type or 'tv' in self.type):
            if len(self.eps) == self.max-self.min+1:
                self.lack=False
            else:
                self.lack=True
            if self.lack:
                self.lackeps=[]
                for i in range(self.min,self.max+1):
                    if not i in self.eps:
                        self.lackeps.append(i)
                logger.warning('识别到路径'+pathid+' 中资源存在部分集数缺失,缺失集数:'+str(self.lackeps))
                res=100
                while not(res==0 or res==1):
                    res=input('识别到路径'+pathid+' 中资源存在部分集数缺失,缺失集数为:'+str(self.lackeps)+'。是否仍然继续发布？请回复选项对应的数字\n0:先不发布，退出程序 1:无视警告,仍然发布\n')
                    try:
                        res=int(res)
                    except:
                        res=100
                    if not(res==0 or res==1):
                        logger.warning('输入有误，请重新输入')
                if res==0:
                    logger.error('识别到路径'+pathid+' 中资源存在部分集数缺失,用户退出程序')
                    raise ValueError ('识别到路径'+pathid+' 中资源存在部分集数缺失,用户退出程序')

            

    def print(self):
        attr=['path','type','collection','enable','doubanurl','imdb_url','bgm_url','anidb_url','from_url','transfer','sub','englishname','chinesename']
        print('Path info:')
        for item in attr:
            exec('print("'+item+':"  ,self.'+item+'  )')
        

        series_attr=['season','seasonnum','eps','min','max']
        if (self.type=='anime' or self.type=='tv'):
            for item in series_attr:
                exec('print("'+item+':"  ,self.'+item+'  )')
            for item in self.sites:
                exec('print("'+item+'_done:"  ,self.'+item+'_done  )')
                exec('print("'+item+'_min_done:"  ,self.'+item+'_min_done  )')
                exec('print("'+item+'_max_done:"  ,self.'+item+'_max_done  )')

        if ('anime' in self.type or 'tv' in self.type) :
            print('self.lack:',self.lack)
            if self.lack:
                print('self.lackeps:',self.lackeps)
        print('')


def findpathinfo(yamlinfo,sites):
    paths=yamlinfo['path info']
    pathlist=[]
    for item in paths:
        pathlist.append(pathinfo(item,paths[item],sites,yamlinfo['basic']))
    write_yaml(yamlinfo)
    #a=input('checkpath')
    return pathlist


