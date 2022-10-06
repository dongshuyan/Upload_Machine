from loguru import logger
import json
import os.path

class site(object):
    def __init__(self,sitename,sitedict):
        self.sitename   = sitename
        self.exist_cookie=False
        self.exist_password=False
        self.uplver =1
        self.enable =0
        self.check = False


        try:
            self.uplver =int(sitedict['uplver'])
        except:
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1

        if not (self.uplver==0 or self.uplver==1):
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1


        try:
            self.enable =int(sitedict['enable'])
        except:
            logger.warning(sitename+'站点enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0

        if not (self.enable==0 or self.enable==1):
            logger.warning(sitename+'站点匿名发布enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0
        '''
        if 'tracker' in sitedict and not sitedict['tracker']==None:
            self.tracker = sitedict['tracker']
        else:
            sitedict['tracker']='https://tracker.pterclub.com/announce'
        '''
        if 'cookie' in sitedict :
            self.cookie=sitedict['cookie']
            self.exist_cookie=True
        else:
            self.cookie=''
            self.exist_cookie=False

        if 'check' in sitedict :
            if str(sitedict['check']=='1'):
                self.check=True
            else:
                self.check=False
        if 'username' in sitedict and not sitedict['username']==None and 'password' in sitedict and not sitedict['password']==None:
            self.username   = sitedict['username']
            self.password   = sitedict['password']
            self.exist_password=True

        if self.enable==1 and (not self.exist_cookie and not self.exist_password):
            logger.error('未找到'+sitename+' 站点的cookie信息以及用户名密码信息，请至少填写一个')
            raise ValueError ('未找到'+sitename+' 站点的cookie信息以及用户名密码信息，请至少填写一个')

    def print(self):

        print('Site info:')
        print('sitename:'  ,self.sitename  )
        print('enable:'    ,self.enable    )
        print('url:'       ,self.url       )
        print('loginurl:'  ,self.loginurl  )
        print('uploadurl:' ,self.uploadurl )
        print('tracker:'   ,self.tracker   )
        if self.exist_password:
            print('username:'  ,self.username  )
            print('password:'  ,self.password  )
        else:
            print('username:未设置或未识别')
            print('password:未设置或未识别')
        if self.exist_cookie:
            print('cookie:',self.cookie)
        else:
            print('cookiefile:未设置或未识别')
        print('')

def makesites(siteinfo):
    sites=dict()
    for item in siteinfo:
        sites[item]=site(item,siteinfo[item])
    return sites








