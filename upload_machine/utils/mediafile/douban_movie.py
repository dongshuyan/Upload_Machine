# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import json


class MoviePageParse:
    def __init__(self, movie_id:int = 0, movie_url:str = '',cookie:str = ''):
        """
        初始化
        :param movie_id:
        :param movie_info_html:
        """
        self.movie_id = movie_id
        self.movie_url = movie_url
        if movie_id==0 and movie_url=='':
            raise Exception('豆瓣链接与豆瓣id至少输入一个')
        elif movie_id==0:
            try:
                movie_id=int(re.findall('/subject/(\d+)/',movie_url)[0])
            except Exception as err:
                raise Exception('豆瓣链接填写错误')
            movie_url='https://movie.douban.com/subject/' + str(movie_id)+'/'
        elif movie_url.strip()=='':
            movie_url='https://movie.douban.com/subject/' + str(movie_id)+'/'
        else:
            movie_url='https://movie.douban.com/subject/' + str(movie_id)+'/'
        
        self.movie_id = movie_id
        self.movie_url = movie_url
        self.cookie = cookie

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
        headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Cookie': cookie,
                'Sec-Fetch-Dest': 'document' ,
                'Sec-Fetch-Mode': 'navigate' ,
                'Sec-Fetch-Site': 'none' ,
                'Sec-Fetch-User': '?1' ,
                'Upgrade-Insecure-Requests': '1' ,
                'User-Agent': user_agent,
                'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0' ,
                'sec-ch-ua-platform': '"macOS"',
            }
        movie_info_html = requests.get(movie_url,headers=headers,timeout=20).text
        self.movie_info_html=movie_info_html
        self.film_soup = BeautifulSoup(self.movie_info_html, 'lxml')

    def _get_movie_name(self):
        """
        获取电影姓名
        :param film_soup:
        :return:
        """
        try:
            name = str(self.film_soup.find('span', property='v:itemreviewed').text)
        except Exception as err:
            name = ''
            #info span.pl:contains("又名")
        return name

    def _get_movie_names(self):
        """
        获取电影姓名
        :param film_soup:
        :return:
        """
        try:
            chinesename = self.film_soup.title.text.replace('(豆瓣)','').strip()
        except Exception as err:
            chinesename = ''
        
        try:
            originalTitle = self._get_movie_name().replace(chinesename,'').strip()
        except Exception as err:
            originalTitle = ''
        
        akaTitles=[]
        try:
            akaTitles=self.film_soup.find('span', class_='pl',text=re.compile("又名")).next_sibling.text.strip().split(' / ')
        except Exception as err:
            akaTitles = []

        if originalTitle=='':
            originalTitle=chinesename
            if len(akaTitles)>0:
                translatedTitle=akaTitles[0]
            else:
                translatedTitle=chinesename
        else:
            translatedTitle=chinesename
        
        

        names={
            'chinesename': chinesename,
            'originalTitle': originalTitle,
            'translatedTitle': translatedTitle,
            'akaTitles': akaTitles,
        }
        return names

    def _get_movie_imdb(self):
        """
        获取imdb
        :param film_soup:
        :return:
        """
        try:
            imdb=self.film_soup.find('span', class_='pl',text=re.compile("IMDb")).next_sibling.text.strip()
        except Exception as err:
            imdb = ''
        return imdb
    
    def _get_movie_imdbscore(self):
        """
        获取imdb分数
        :param film_soup:
        :return:
        """
        imdb=self._get_movie_imdb()
        if imdb.strip()=='':
            imdbrating={
                'rating': 0,
                'ratingCount': 0,
            }
            return imdbrating

        url='http://p.media-imdb.com/static-content/documents/v1/title/'+imdb+'/ratings%3Fjsonp=imdb.rating.run:imdb.api.title.ratings/data.json'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
        headers={
            'referrer': 'http://p.media-imdb.com/',
            'User-Agent': user_agent,
        }
        r= requests.get(url,headers=headers,timeout=20)
        
        
        rating=0
        ratingCount=0

        try:
            data=r.text[16:-1]
            data2 = json.loads(data)
            rating=data2['resource']['rating']
            ratingCount=data2['resource']['ratingCount']
        except Exception as err:
            rating=0
            ratingCount=0

        imdbrating={
            'rating': rating,
            'ratingCount': ratingCount,
        }
        return imdbrating

    def _get_movie_year(self):
        """
        获取电影年份
        :param film_soup:
        :return:
        """
        try:
            year = str(self.film_soup.find('span', class_='year').text)
        except Exception as err:
            year = ''
        
        year=re.findall('\d\d\d\d',year)

        try:
            year = int(year[0])
        except Exception as err:
            year = 2022

        return year

    def _get_movie_image_url(self):
        """
        获取电影图片链接
        :return:
        """
        try:
            image_url = str(self.film_soup.find('img', title='点击看更多海报')['src'])
        except Exception as err:
            image_url = ''
        try:
            image_url='https://img9.doubanio.com/view/photo/l_ratio_poster/public/'+re.findall('(p\d+).',image_url)[0]+'.jpg'
        except Exception as err:
            image_url = ''
        #image_url=image_url.replace(re.findall('img[0-9]\.doubanio\.com',image_url)[0],'img9.doubanio.com')
        return image_url

    def _get_movie_directors(self):
        """
        获取电影导演信息
        :param film_soup:
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            directors = []
            directors_text = re.search(r'导演</span>: <span class="attrs">.*</span><br/>', film_info).group()
            directors_text = directors_text.replace('导演</span>: <span class="attrs">', '').replace('</span><br/>',
                                                                                                   '').replace(
                '</span>', '')
            directors_text_list = directors_text.split('</a>')
            while '' in directors_text_list:
                directors_text_list.remove('')
            for director in directors_text_list:
                director_name = re.sub(r'<a.*>', '', director).replace('/', '').replace(' ', '')
                if 'celebrity' in director:
                    director_href = re.search(r'href="/celebrity/\d{0,15}/"', director).group().replace('href=',
                                                                                                        '').replace('"',
                                                                                                                    '')
                else:
                    director_href = ''
                directors.append({'name': director_name, 'href': director_href})
        except Exception as err:
            directors = []

        return directors

    def _get_movie_writers(self):
        """
        获取电影编剧信息
        :param film_soup:
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            writers = []
            writers_text = re.search(r'编剧</span>: <span class="attrs">.*</span><br/>', film_info).group()
            writers_text = writers_text.replace('编剧</span>: <span class="attrs">', '').replace('</span><br/>',
                                                                                               '').replace(
                '</span>', '')
            writers_text_list = writers_text.split('</a>')
            while '' in writers_text_list:
                writers_text_list.remove('')
            for writer in writers_text_list:
                writer_name = re.sub(r'<a.*>', '', writer).replace('/', '').replace(' ', '')
                if 'celebrity' in writer:
                    writer_href = re.search(r'href="/celebrity/\d{0,15}/"', writer).group().replace('href=',
                                                                                                    '').replace('"', '')
                else:
                    writer_href = ''
                writers.append({'name': writer_name, 'href': writer_href})
        except Exception as err:
            writers = []

        return writers

    def _get_movie_actors(self):
        """
        获取电影演员信息
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            actors = []
            actors_text = re.search(r'主演</span>: <span class="attrs">.*</span><br/>', film_info).group()
            actors_text = actors_text.replace('主演</span>: <span class="attrs">', '').replace('</span><br/>',
                                                                                             '').replace(
                '</span>', '')
            actors_text_list = actors_text.split('</a>')
            while '' in actors_text_list:
                actors_text_list.remove('')
            for actor in actors_text_list:
                actor_name = re.sub(r'<a.*>', '', actor).replace('/', '').replace(' ', '')
                if 'celebrity' in actor:
                    actor_href = re.search(r'href="/celebrity/\d{0,15}/"', actor).group().replace('href=', '').replace(
                        '"', '')
                else:
                    actor_href = ''
                actors.append({'name': actor_name, 'href': actor_href})
        except Exception as err:
            actors = []
        return actors

    def _get_movie_genres(self):
        """
        获取电影类型
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            genres = []
            genres_text = re.search(r'类型:</span> .*<br/>', film_info).group()
            genres_text = genres_text.replace('类型:</span> ', '').replace('<br/>', '')
            genres_text_list = genres_text.split('</span>')
            while '' in genres_text_list:
                genres_text_list.remove('')
            for genre in genres_text_list:
                genre_name = re.sub(r'<span.*>', '', genre).replace('/', '').replace(' ', '')
                genres.append(genre_name)
        except Exception as err:
            genres = []

        return genres

    def _get_movie_countries(self):
        """
        获取电影制片国家/地区
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            countries_text = re.search(r'制片国家/地区:</span>.*<br/>', film_info).group()
            countries_text = countries_text.replace('制片国家/地区:</span>', '').replace('<br/>', '')
            countries = [country.replace(' ', '') for country in countries_text.split('/')]
        except Exception as err:
            countries = []

        return countries

    def _get_movie_languages(self):
        """
        获取电影语言
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            languages_text = re.search(r'语言:</span>.*<br/>', film_info).group()
            languages_text = languages_text.replace('语言:</span>', '').replace('<br/>', '')
            languages = [language.replace(' ', '') for language in languages_text.split('/')]
        except Exception as err:
            languages = []

        return languages

    def _get_movie_pubdates(self):
        """
        获取电影上映时间
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            pubdates = []
            try:
                release_text = re.search(r'上映日期:</span> .*<br/>', film_info).group()
                release_text = release_text.replace('上映日期:</span> ', '').replace('<br/>', '')
                pubdates_text_list = release_text.split('</span>')
            except:
                premiere_text = re.search(r'首播:</span>.*<br/>', film_info).group()
                premiere_text = premiere_text.replace('首播:</span> ', '').replace('<br/>', '')
                pubdates_text_list = premiere_text.split('</span>')
            while '' in pubdates_text_list:
                pubdates_text_list.remove('')
            for pubdate in pubdates_text_list:
                pubdate_name = re.sub(r'<span.*>', '', pubdate).replace('/', '').replace(' ', '')
                pubdates.append(pubdate_name)
        except Exception as err:
            pubdates = []
        return pubdates

    def _get_movie_episodes(self):
        """
        获取电影集数
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            episodes_text = re.search(r'集数:</span>.*<br/>', film_info).group()
            episodes_text = episodes_text.replace('集数:</span>', '').replace('<br/>', '').replace(' ', '')
            episodes = episodes_text
        except Exception as err:
            episodes = '1'
        return episodes

    def _get_movie_durations(self):
        """
        获取电影片长
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            durations = []
            durations_text = re.search(r'片长:</span> .*<br/>', film_info).group()
            durations_text = durations_text.replace('片长:</span> ', '').replace('<br/>', '')
            durations_text_list = durations_text.split('</span>')
            while '' in durations_text_list:
                durations_text_list.remove('')
            for duration in durations_text_list:
                duration_name = re.sub(r'<span.*>', '', duration).replace('/', '').replace(' ', '')
                durations.append(duration_name)
        except Exception as err:
            durations = []

        return durations

    def _get_movie_other_names(self):
        """
        获取电影其他名称
        :return:
        """
        try:
            film_info = str(self.film_soup.find('div', {'id': 'info'}))
            other_names = []
            other_names_text = re.search('又名:</span>.*<br/>', film_info).group()
            other_names_text = other_names_text.replace('又名:</span>', '').replace('<br/>', '')
            other_names_text_list = other_names_text.split('/')
            while '' in other_names_text_list:
                other_names_text_list.remove('')
            for other_name in other_names_text_list:
                name = other_name.replace('/', '')#.replace(' ', '')
                other_names.append(name)
        except Exception as err:
            other_names = []

        return other_names

    def _get_movie_summary(self):
        """
        获取电影简介
        :return:
        """
        try:
            try:
                # all content
                summary = str(self.film_soup.find('span', class_='all hidden').text)
                summary = summary.replace('\n', '').replace('\u3000', '').replace(' ', '')
            except Exception as err:
                # short content
                summary = str(self.film_soup.find('span', property='v:summary').text)
                summary = summary.replace('\n', '').replace('\u3000', '').replace(' ', '')
        except Exception as err:
            summary = ''
        return summary

    def _get_movie_rating(self):
        """
        获取电影评分
        :return:
        """
        try:
            average = str(self.film_soup.find('strong', property='v:average').text)
            reviews_count = str(self.film_soup.find('span', property='v:votes').text)
            rating = {
                'average': average,
                'reviews_count': reviews_count
            }
        except Exception as err:
            rating = {
                'average': '',
                'reviews_count': ''
            }
        return rating
    def _get_movie_awards(self):
        awards_url='https://movie.douban.com/subject/'+str(self.movie_id)+'/awards/'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
        headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Cookie': self.cookie,
                'Sec-Fetch-Dest': 'document' ,
                'Sec-Fetch-Mode': 'navigate' ,
                'Sec-Fetch-Site': 'none' ,
                'Sec-Fetch-User': '?1' ,
                'Upgrade-Insecure-Requests': '1' ,
                'User-Agent': user_agent,
                'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0' ,
                'sec-ch-ua-platform': '"macOS"',
            }
        r=requests.get(awards_url,headers=headers,timeout=20)
        award_soup = BeautifulSoup(r.text, 'lxml')
        awardlist=award_soup.find_all('div',class_='awards')
        awards=[]
        for awarditem in awardlist:
            title=awarditem.find('h2').text.replace('\n',' ').strip()
            contentlist=awarditem.find_all('ul',class_="award")
            content=[]
            for contentitem in contentlist:
                content.append(contentitem.text.replace('\n',' ').strip())
            tempitem={
                'title':title,
                'content':content,
            }
            awards.append(tempitem)
        return awards
    def parse(self):
        """
        获取电影信息（包含电视剧、综艺、动漫、纪录片、短片）
        :return:
        """
        #name = self._get_movie_name()  # 电影姓名
        names =self._get_movie_names()
        year=self._get_movie_year()
        image_url = self._get_movie_image_url()  # 电影图片链接
        directors = self._get_movie_directors()  # 电影导演
        writers = self._get_movie_writers()  # 电影编剧
        actors = self._get_movie_actors()  # 电影演员
        genres = self._get_movie_genres()  # 电影类型
        countries = self._get_movie_countries()  # 电影制片国家/地区
        languages = self._get_movie_languages()  # 电影语言
        pubdates = self._get_movie_pubdates()  # 电影上映时间
        episodes = self._get_movie_episodes()  # 电影集数
        durations = self._get_movie_durations()  # 电影片长
        other_names = self._get_movie_other_names()  # 电影其他名称
        summary = self._get_movie_summary()  # 电影简介
        rating = self._get_movie_rating()  # 电影评分
        imdb= self._get_movie_imdb()
        imdbrating=self._get_movie_imdbscore()
        awards = self._get_movie_awards()


        movie_info_json = {
            'id': self.movie_id,
            'image_url': image_url,
            'names': names,
            'year': year,
            'directors': directors,
            'writers': writers,
            'actors': actors,
            'genres': genres,
            'countries': countries,
            'languages': languages,
            'pubdates': pubdates,
            'episodes': episodes,
            'durations': durations,
            'other_names': other_names,
            'summary': summary,
            'rating': rating,
            'imdb': imdb,
            'imdbrating': imdbrating,
            'awards':awards,
        }
        return movie_info_json
    def info(self):
        data=self.parse()
        douban_info=''
        if (data['image_url']):
            imgurl=re.findall('img[0-9]\.doubanio\.com',data['image_url'])
            douban_info = douban_info+"[img]" + data['image_url'].replace(imgurl[0],'img9.doubanio.com') + "[/img]\n"
            #self.picture=data['pic']
        if (data['names']['translatedTitle']):
            douban_info = douban_info+ "\n◎译\u3000\u3000名　" + '/'.join([data['names']['translatedTitle']]+data['names']['akaTitles']);
        if (data['names']['originalTitle']) :
            douban_info += "\n◎片\u3000\u3000名　" + data['names']['originalTitle']
        if (data['year']):
            douban_info += "\n◎年\u3000\u3000代　" + str(data['year'])
        if (data['countries'] and len(data['countries']) > 0) :
            douban_info += "\n◎产\u3000\u3000地　" + " / ".join(data['countries'])
        if (data['genres'] and len(data['genres']) > 0):
            douban_info += "\n◎类\u3000\u3000别　" + " / ".join(data['genres'])
        if (data['languages'] and len(data['languages']) > 0) :
            douban_info += "\n◎语\u3000\u3000言　" + " / ".join(data['languages'])
        if (data['pubdates'] and len(data['pubdates']) > 0) :
            douban_info += "\n◎上映日期　" + " / ".join(data['pubdates'])     
        if (data['imdb'].strip()!='') :
            if (data['imdbrating']) :
                douban_info += "\n◎IMDb评分  " + str(data['imdbrating']['rating']) + "/10 from " + str(data['imdbrating']['ratingCount']) + " users"
            douban_info += "\n◎IMDb链接  https://www.imdb.com/title/" + data['imdb']+"/"
        if (data['rating']) :
            douban_info += "\n◎豆瓣评分　" + str(data['rating']['average']) + "/10 from " + str(data['rating']['reviews_count']) + " users";
        if (self.movie_url) :
            douban_info += "\n◎豆瓣链接　" + self.movie_url
        if (data['durations'] and len(data['durations']) > 0) :
            douban_info += "\n◎片　　长　" + " / ".join(data['durations'])
        if (data['episodes']) :
            douban_info += "\n◎集\u3000\u3000数　" + data['episodes']
        if (data['directors'] and len(data['directors']) > 0) :
            for i in range (len(data['directors'])):
                if i==0:
                    douban_info += "\n◎导　　演　" + (data['directors'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['directors'][i]['name'])

        if (data['writers'] and len(data['writers']) > 0) :
            for i in range (len(data['writers'])):
                if i==0:
                    douban_info += "\n◎编　　剧　" + (data['writers'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['writers'][i]['name'])

        if (data['actors'] and len(data['actors']) > 0) :
            for i in range (len(data['actors'])):
                if i==0:
                    douban_info += "\n◎主　　演　" + (data['actors'][i]['name'])
                else:
                    douban_info += "\n　　　　　  " + (data['actors'][i]['name'])

        if ('tags' in data and data['tags'] and len(data['tags']) > 0) :
            douban_info += "\n\n\n◎标　　签　" + " | ".join(data['tags'])
       
        if (data['summary']) :
            douban_info += "\n\n◎简　　介　" + "\n\n " +(data['summary'])
        else:
            douban_info += "\n\n◎简　　介　" + "\n\n 暂无相关剧情介绍"

        if ('awards' in data and data['awards'] and len(data['awards']) > 0) :
            awardstr=''
            for item in data['awards']:
                awardstr=awardstr+"\n\n　　" + item['title'];
                for itemc in item['content']:
                    awardstr=awardstr+"\n　　" + itemc
            douban_info += "\n\n◎获奖情况　" + awardstr

        douban_info =douban_info+ "\n\n"
        self.douban_info=douban_info
        return douban_info


