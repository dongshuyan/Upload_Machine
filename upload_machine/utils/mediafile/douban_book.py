# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


class BookPageParse:
    def __init__(self, book_id:int = 0, book_url:str = '',cookie:str = ''):
        """
        初始化
        :param book_id:
        :param book_info_html:
        """

        if book_id==0 and book_url=='':
            raise Exception('豆瓣链接与豆瓣id至少输入一个')
        elif book_id==0:
            try:
                book_id=int(re.findall('/subject/(\d+)/',book_url)[0])
            except Exception as err:
                raise Exception('豆瓣链接填写错误')
            book_url='https://book.douban.com/subject/' + str(book_id)+'/'
        elif book_url.strip()=='':
            book_url='https://book.douban.com/subject/' + str(book_id)+'/'
        
        self.book_id = book_id
        self.book_url = book_url
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
        book_info_html = requests.get(book_url,headers=headers,timeout=20).text
        self.book_info_html=book_info_html
        self.book_soup = BeautifulSoup(self.book_info_html, 'lxml')

    def _get_book_name(self):
        """
        得到书籍名称
        :return:
        """
        try:
            name = self.book_soup.find('span', property="v:itemreviewed").text
        except Exception as err:
            name = ''
        return name

    def _get_book_image_url(self):
        """
        得到书籍图片链接
        :return:
        """
        try:
            image_url = str(self.book_soup.find('img', rel='v:photo')['src'])
        except Exception as err:
            image_url = ''
        return image_url

    def _get_book_subtitle(self):
        """
        获取书籍副标题
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            subtitle_str = str(re.search(r'副标题:</span>.*<br/>', book_info).group())
            subtitle = subtitle_str.replace('副标题:</span>', '').replace('<br/>', '').replace(' ', '')
        except Exception as err:
            subtitle = ''
        return subtitle

    def _get_book_origin_name(self):
        """
        获取书籍原作名
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            origin_name_str = str(re.search(r'原作名:</span>.*<br/>', book_info).group())
            origin_name = origin_name_str.replace('原作名:</span>', '').replace('<br/>', '')
        except Exception as err:
            origin_name = ''
        return origin_name.strip()

    def _get_book_author(self):
        """
        得到图书作者信息
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            book_info = book_info.replace('\n', '').replace(' ', '').replace('\xa0', '')
            if '作者</span>:' in book_info:
                book_author_str = str(re.search(r'作者</span>:.*?<br/>', book_info).group())
            else:
                book_author_str = re.search(r'作者:</span>.*?<br/>', book_info).group()
            book_author_list = book_author_str.split('</a>')
            author_list = []
            for i in range(0, len(book_author_list) - 1):
                author_str = book_author_list[i]
                author_name = re.sub(r'.*>', '', author_str)
                author_href = ''
                if '/author/' in author_str:
                    author_href = str(re.findall(r'href=".*"', author_str)[0]).replace('href=', '').replace('"', '')
                    author_href = author_href.replace('https://book.douban.com', '')
                author = {
                    'name': author_name,
                    'href': author_href
                }
                author_list.append(author)
        except Exception as err:
            author_list = []
        return author_list

    def _get_book_translator(self):
        """
        得到书籍译者
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            book_info = book_info.replace('\n', '').replace(' ', '').replace('\xa0', '')
            if '译者</span>:' in book_info:
                book_translator_str = str(re.search('译者</span>:.*?<br/>', book_info).group())
            else:
                book_translator_str = re.search('译者:</span>.*?<br/>', book_info).group()
            book_translator_list = book_translator_str.split('</a>')
            translator_list = []
            for i in range(0, len(book_translator_list) - 1):
                translator_str = book_translator_list[i]
                translator_name = str(re.sub(r'.*>', '', translator_str))
                translator_href = ''
                if '/author/' in translator_str:
                    translator_href = str(re.findall(r'href=".*"', translator_str)[0]).replace('href=', '').replace('"',
                                                                                                                    '')
                    translator_href = translator_href.replace('https://book.douban.com', '')
                translator = {
                    'name': translator_name,
                    'href': translator_href
                }
                translator_list.append(translator)
        except Exception as err:
            translator_list = []
        return translator_list

    def _get_book_press(self):
        """
        得到图书出版社信息
        :return:
        """

        try:
            book_info = self.book_soup.find('div', id='info')
            pressinfo=book_info.find('span',class_='pl',text=re.compile("出版社"))
            press_text = pressinfo.findNextSibling('a').text
            press = press_text.replace('出版社:</span>', '').replace(' ', '').replace('<br/>', '')
        except Exception as err:
            press = ''
            
        try:
            href=pressinfo.findNextSibling('a').attrs['href']
        except Exception as err:
            href = ''

        press={
            'name': press.strip(),
            'href': href,
        }
        return press
    
    def _get_book_producers(self):
        """
        得到图书出品方信息
        :return:
        """
        try:
            book_info = self.book_soup.find('div', id='info')
            producersinfo=book_info.find('span',class_='pl',text=re.compile("出品方"))
            producers_text = producersinfo.findNextSibling('a').text
            href=producersinfo.findNextSibling('a').attrs['href']
            producers = producers_text.replace('出品方:</span>', '').replace(' ', '').replace('<br/>', '')
        except Exception as err:
            producers = ''

        try:
            href=producersinfo.findNextSibling('a').attrs['href']
        except Exception as err:
            href=''

        producers={
            'name': producers.strip(),
            'href': href,
        }

        return producers
    
    def _get_book_series(self):
        """
        得到图书出品方信息
        :return:
        """
        try:
            book_info = self.book_soup.find('div', id='info')
            seriesinfo=book_info.find('span',class_='pl',text=re.compile("丛书"))
            series_text = seriesinfo.findNextSibling('a').text
            series = series_text.replace('丛书:</span>', '').replace(' ', '').replace('<br/>', '')
        except Exception as err:
            series = ''
        
        try:
            href=seriesinfo.findNextSibling('a').attrs['href']
        except Exception as err:
            href=''

        series={
            'name': series.strip(),
            'href': href,
        }

        return series
    
    def _get_book_ISBN(self):
        """
        得到图书ISBN信息
        :return:
        """
        try:
            book_info = self.book_soup.find('div', id='info')
            isbninfo=book_info.find('span',class_='pl',text=re.compile("ISBN"))
            isbn=isbninfo.next_sibling.text.strip()
        except Exception as err:
            isbn = ''
        return isbn
    
    def _get_book_pack(self):
        """
        得到图书ISBN信息
        :return:
        """
        try:
            book_info = self.book_soup.find('div', id='info')
            packinfo=book_info.find('span',class_='pl',text=re.compile("装帧"))
            pack=packinfo.next_sibling.text.strip()
        except Exception as err:
            pack = ''
        return pack

    def _get_book_publish_year(self):
        """
        书籍出版年份
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            publish_year_str = str(re.search(r'出版年:</span>.*<br/>', book_info).group())
            publish_year_str = publish_year_str.replace('出版年:</span>', '').replace('<br/>', '').replace(' ', '')
            publish_year = re.sub('<a.*>', '', publish_year_str)
        except Exception as err:
            publish_year = ''
        return publish_year

    def _get_book_page_num(self):
        """
        得到书籍页面
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            page_num_str = str(re.search(r'页数:</span>.*<br/>', book_info).group())
            page_num_str = page_num_str.replace('页数:</span>', '').replace('<br/>', '').replace(' ', '')
            page_num = re.sub('<a.*>', '', page_num_str)
        except Exception as err:
            page_num = ''
        return page_num

    def _get_book_price(self):
        """
        得到书籍价格
        :return:
        """
        try:
            book_info = str(self.book_soup.find('div', id='info'))
            price_str = str(re.search(r'定价:</span>.*<br/>', book_info).group())
            price_str = price_str.replace('定价:</span>', '').replace('<br/>', '').replace(' ', '')
            price = re.sub('<a.*>', '', price_str)
        except Exception as err:
            price = ''
        return price

    def _get_book_content_abstract(self):
        """
        得到图书内容简介
        :return:
        """
        try:
            try:
                content_abstract = str(self.book_soup.find('span', class_='all hidden').text)
                content_abstract = content_abstract.replace(' ', '').replace('\n', '').replace('\u3000', '')
                content_abstract = str(re.sub('.*;}', '', content_abstract))
            except:
                content_abstract = str(self.book_soup.find_all('div', class_='intro')[0].text)
                content_abstract = content_abstract.replace(' ', '').replace('\n', '').replace('\u3000', '')
        except Exception as err:
            content_abstract = ''
        return content_abstract

    def _get_book_catalog(self):
        """
        得到图书目录
        :return:
        """
        try:
            try:
                catalog_id = 'dir_' + str(self.book_id) + '_full'
                catalog = str(self.book_soup.find('div', id=catalog_id).text)
                catalog = catalog.replace(' ', '')
            except:
                catalog_id = 'dir_' + str(self.book_id) + '_short'
                catalog = str(self.book_soup.find('div', id=catalog_id).text)
                catalog = catalog.replace(' ', '')
        except Exception as err:
            catalog = ''
        return catalog

    def _get_book_rating(self):
        """
        得到书籍评分
        :return:
        """
        try:
            average = str(self.book_soup.find('strong', property='v:average').text)
            reviews_count = str(self.book_soup.find('a', class_='rating_people').text)
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

    def parse(self):
        """
        获取书籍信息
        :return:
        """
        name = self._get_book_name()  # 书籍名称
        image_url = self._get_book_image_url()  # 书籍图片链接
        subtitle = self._get_book_subtitle()  # 书籍副标题
        origin_name = self._get_book_origin_name()  # 原作名
        author = self._get_book_author()  # 书籍作者
        translator = self._get_book_translator()  # 书籍译者
        press = self._get_book_press()  # 书籍出版社
        publish_year = self._get_book_publish_year()  # 书籍出版年份
        price = self._get_book_price()  # 书籍价格
        page_num = self._get_book_page_num()  # 书籍页数
        content_abstract = self._get_book_content_abstract()  # 图书内容简介
        catalog = self._get_book_catalog()  # 图书目录
        rating = self._get_book_rating()  # 书籍评分
        isbn = self._get_book_ISBN() #ISBN
        producers = self._get_book_producers() #出品方
        series = self._get_book_series() #丛书
        pack = self._get_book_pack() #装帧

        book_info_json = {
            'id': self.book_id,
            'image_url': image_url,
            'name': name,
            'subtitle': subtitle,
            'author': author,
            'press': press,
            'producers': producers,
            'origin_name': origin_name,
            'translator': translator,
            'publish_year': publish_year,
            'page_num': page_num,
            'price': price,
            'pack' : pack,
            'series': series,
            'ISBN': isbn,
            'content_abstract': content_abstract,
            'catalog': catalog,
            'rating': rating
        }
        return book_info_json

    def info(self):
        data=self.parse()
        douban_info=''
        if (data['image_url']):
            imgurl=re.findall('img[0-9]\.doubanio\.com',data['image_url'])
            douban_info = douban_info+"[img]" + data['image_url'].replace(imgurl[0],'img9.doubanio.com') + "[/img]\n"
        if (data['name']):
            douban_info = douban_info+ "\n◎书\u3000\u3000名　" + data['name'];
        if (data['author']) :
            douban_info += "\n◎作\u3000\u3000者　" + data['author'][0]['name']
        if (data['press']) :
            douban_info += "\n◎出版\u3000社　" + data['press']['name']
        if (data['producers']) :
            douban_info += "\n◎出品\u3000方　" + data['producers']['name']
        if (data['origin_name']) :
            douban_info += "\n◎原作名称　" + data['origin_name']
        if (data['translator']) :
            douban_info += "\n◎译\u3000\u3000者　" + data['translator'][0]['name']
        if (data['publish_year']) :
            douban_info += "\n◎出版年月　" + data['publish_year']
        if (data['page_num']) :
            douban_info += "\n◎页\u3000\u3000数　" + str(data['page_num'])
        if (data['price']) :
            douban_info += "\n◎定\u3000\u3000价　" + data['price']
        if (data['pack']) :
            douban_info += "\n◎装\u3000\u3000帧　" + data['pack']
        if (data['series']) :
            douban_info += "\n◎从\u3000\u3000书　" + data['series']['name']
        if (data['ISBN']) :
            douban_info += "\n◎I S B N　 " + data['ISBN']
        if (data['price']) :
            douban_info += "\n◎定\u3000\u3000价　" + data['price']
        if (data['rating']) :
            douban_info += "\n◎豆瓣评分　" + str(data['rating']['average']) + "/10 from " + str(re.findall('\d+',data['rating']['reviews_count'])[0]) + " users";
        if (self.book_url) :
            douban_info += "\n◎豆瓣链接　" + self.book_url
        if (data['catalog']):
            douban_info += "\n◎目\u3000\u3000录　" + str(data['catalog'])
        if (data['content_abstract']) :
            douban_info += "\n\n◎简　　介　" + "\n\n " +(data['content_abstract'])
        else:
            douban_info += "\n\n◎简　　介　" + "\n\n 暂无相关剧情介绍"
        douban_info =douban_info+ "\n\n"
        self.douban_info=douban_info
        return douban_info

