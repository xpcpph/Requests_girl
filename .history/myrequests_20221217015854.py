# -*- coding: utf-8 -*-

from lxml import html
import selenium
from selenium import webdriver
from selenium import common

'''
    Repr.maxlevel --- 递归表示的深度限制，默认是6

    Repr.maxdict
    Repr.maxlist  --- 可向后两层
    Repr.maxtuple
    Repr.maxset
    Repr.maxfrozenset
    Repr.maxdeque
    Repr.maxarray ----命名对象类型的条目数限制，maxdict是4，maxarray是5，其它是6

    Repr.maxlong   ---- 表示一个整数最大字符数，默认40
    Repr.maxstring ---- 表示一个字符串最大字符数，默认30
    Repr.maxother  ---- 表示其他类型的最大字符数，默认20
'''
from web_state import *
from Tool import *
import html
import bs4
import sys
from bs4 import BeautifulSoup
from lxml import etree

com = True  # 测试用的,控制爬虫,爬起第一个主页的网址

'''
    工具类:
        1.解压gzip压缩的网页
        2.字典通过值来获取键
'''


class Dict_MiXin():
    def to_dict(self):
        self.__contains_dict(self.__dict__)

    def __contains_dict(self, attr: dict):
        result = {}
        for key, value in attr.items():
            result[key] = self.__contains_value(value)
        return result

    def __contains_value(self, value):
        if isinstance(value, Dict_MiXin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self.__contains_dict(value)
        elif isinstance(value, list):
            return [self.__contains_value(v) for v in value]
        elif hasattr(value, "__dict__"):
            return self.__contains_dict(value)


class My_Requests(Dict_MiXin, Tool_MiXin, Web):

    '''
    requests.get(‘https://github.com/timeline.json’)                                # GET请求
    requests.post(“http://httpbin.org/post”)                                        # POST请求
    requests.put(“http://httpbin.org/put”)                                          # PUT请求
    requests.delete(“http://httpbin.org/delete”)                                    # DELETE请求
    requests.head(“http://httpbin.org/get”)                                         # HEAD请求
    requests.options(“http://httpbin.org/get” )                                     # OPTIONS请求

    url_params = {'key':'value'}       #    字典传递参数，如果值为None的键不会被添加到url中
    r = requests.get('your url',params = url_params)
    print(r.url)
　　　　　　　　your url?key=value
    r.encoding                       #获取当前的编码
    r.encoding = 'utf-8'             #设置编码
    r.text                           #以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
    r.content                        #以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。
    r.headers                        #以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
    r.status_code                     #响应状态码
    r.raw                             #返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()   
    r.ok                              # 查看r.ok的布尔值便可以知道是否登陆成功
     #*特殊方法*#
    r.json()                         #Requests中内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常
    r.raise_for_status()             #失败请求(非200响应)抛出异常
    r1 = requests.get(url='http://dict.baidu.com/s', params={'wd': 'python'})      # 带参数的get请求
    r.headers                                  #返回字典类型,头信息
    r.requests.headers                         #返回发送到服务器的头信息
    r.cookies                                  #返回cookie
    r.history                                  #返回重定向信息,当然可以在请求是加上allow_redirects = false 阻止重定向


    '''

    def __init__(self, browser:str):
        Tool_MiXin().__init__()
        # Web().__init__()
        self.start_url = str()  # 初始网址
        self.browser = browser  # 浏览器
        self.web_path = "./web.conf"#配置文件路径
        self.Config_Dict = dict()  # 配置字典
        self.page_con = 0       #
        self.file_log = self.File_Log() #创建日志记录器
        self.main_title = str()     #
        self.combination = {}       #
        self.start_urls = []  # 开始列表,记录的是主页上有多少页
        self.requests_url = {}  # 爬取字典使用的是前主题:爬取网页的形式
        self.download_urls = {}#
        self.download_url = str()#

    # 获取web的配置
    def Get_Web_Config(self):
        temp_dict = Web(self.start_url)
        # print(temp_dict.Web_Create_Dict())
        self.Config_Dict = temp_dict.Web_Create_Dict().copy()

    def Get_Url(self):
        # print("这里运行吗")
        print(sys._getframe().f_code.co_name + "开始运行")
        config = configparser.ConfigParser()
        # config.sections()
        config.read(self.web_path, encoding='utf-8')  # 读取配置文件
        if config.has_section("start_urls"):
            try:
                '''     获取配置数据     '''
                print(type(config.get("root", "start_urls")))
                # start_urls.append(config.get("root", "start_urls"))
                print(self.start_urls)
                self.file_log.debug("读取到{}的配置为{}".format(
                    "start_urls", self.start_urls))
                return self.start_urls
            except configparser.NoOptionError:
                # config.set(self.url, self.argument_list[0],"False")
                # config.write(open(self.web_path, "w"))
                self.file_log.warning("没有start_urls这个选项")
                exit()

    # 删除javascript
    def Remove_Javascript(self, re) -> str:
        tree = html.fromstring(re)
        # print(tree)
        ele = tree.xpath('//script | //noscript | //style | //link')
        # print(ele)
        for e in ele:
            # print(e)
            e.getparent().remove(e)
            # print(e)

        # tostring()返回的是bytes类型，decode()转成字符串
        Html = html.tostring(tree).decode()
        html.unescape(Html)  # unescape()将字符串中的uncode变化转成中文
        return Html

    # 将html字符替换为实体字符
    def Replace_Char_Entity(self, htmlStr: str) -> str:
        import re
        '''
          替换html中常用的字符实体
          使用正常的字符替换html中特殊的字符实体
          可以添加新的字符实体到CHAR_ENTITIES 中
          CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
          :param htmlStr:
          '''
        self.htmlStr = htmlStr
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlStr)
        while sz:
            entity = sz.group()  # entity全称，如>
            # 去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
            key = sz.group('name')
            try:
                htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
            except KeyError:
                # 以空串代替
                htmlStr = re_charEntity.sub('', htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
        return htmlStr

    # 去除无意义的数据的
    def Html_Tag_Con(self, html: str) -> str:
        print(sys._getframe().f_code.co_name + "开始运行")
        import re
        """
            正则表达式匹配规则
            字符    功能
            .       匹配任意1个字符(除了\n)
            []      匹配[]中列举的一个字符
            \d      匹配数字,也就是0-9
            \D      匹配非数字,也就是匹配不是数字的字符,\d取反
            \s      匹配空白符,也就是空格\tab
            \S      匹配非空白符,\s取反
            \w      陪陪单词字符, a-z, A-Z, 0-9, _
            \W      匹配非单词字符, \w取反
            *       匹配前一个字符出现0次到无限次
            +       匹配前一个字符出现1次到无限次
            ?       匹配前一个字符出现1次或者0次
            {m}     匹配前一个字符出现m次
            {m,}    匹配前一个字符至少出现m次
            {m,n}   匹配前一个字符出现m到n次
            ^或\A   匹配字符串的开头
            $或\Z   匹配字符串的结尾
            \b      匹配\w和\W之间，即匹配单词边界
            \B      \b取反
        """
        # 兼容换行
        html = html.replace('\r\n', '\n')
        html = html.replace('\r', '\n')

        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile(
            '<\s*script[^>]*>[\S\s]*?<\s*/\s*script\s*>', re.I)  # script
        re_style = re.compile(
            '<\s*style[^>]*>[\S\s]*?<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\\s*?\/??>', re.I)  # br标签换行
        re_p = re.compile('<\/p>', re.I)  # p标签换行
        # re_h = re.compile('<[\!|/]?\w+[^>]*>', re.I)  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        re_hendstr = re.compile('^\s*|\s*$')  # 头尾空白字符
        re_lineblank = re.compile('[\t\f\v ]*')  # 空白字符
        re_linenum = re.compile('\n+')  # 连续换行保留1个

        # 处理
        # html = re_cdata.sub('', html)  # 去CDATA
        html = re_script.sub('', html)  # 去script
        html = re_style.sub('', html)  # 去style
        html = re_br.sub('\n', html)  # br标签换行
        html = re_p.sub('\n', html)  # p标签换行
        # html = re_h.sub('', html)  # 去HTML标签
        html = re_comment.sub('', html)  # 去HTML注释
        # html = re_lineblank.sub('', html)  # 去空白字符
        html = re_linenum.sub('\n', html)  # 连续换行保留1个
        html = re_hendstr.sub('', html)  # 去头尾空白字符
        # html = self.Replace_Char_Entity(html)
        # print(html)
        # with open("./html.html","w",encoding="utf-8") as fa:
        #     # print(1,html)
        #     fa.write(html)
        #     # fa.close()
        return html

    # 获取爬取字典的
    def Get_Request_Url(self, html: list, label: str, attribute_href: str, attribute_title: str) -> dict:
        print(sys._getframe().f_code.co_name + "开始运行")
        __temp = {}
        for i in html:
            href = etree.tostring(i, encoding='utf-8').decode('utf-8')
            # print(type(href))
            href = BeautifulSoup(href, "html.parser")  # 文档对象
            for i in href.find_all(label):
                # print(1,i)
                href = i[attribute_href]
                title = i[attribute_title]
                __temp[title] = href
                # self.file_log.debug("获取到{}的网址为{}".format(title,href))

        return __temp

    # 获取最后一个匹配的索引
    def last(self, list: list, str):
        _ = []
        for i in range(len(list)-1, 0, -1):
            _.append(list[i])
        return _.index(str)

    # 获取图片页面后面网址
    def Get_Request_Url_List(self, html: list, label: str, attribute_href: str) -> list:
        print(sys._getframe().f_code.co_name + "开始运行")
        __temp = []
        for i in html:
            href = etree.tostring(i, encoding='utf-8').decode('utf-8')
            # print(href)
            href = BeautifulSoup(href, "html.parser")  # 文档对象
            for i in href.find_all(label):
                # print(1,i)
                href = i[attribute_href]
                __temp.append(href)
                # self.file_log.debug("获取到图片页的网址为{}".format(href))

            _ = str()  # 空字符串
            __ = __temp[0]  # 获取第一个数据
            __ = list(__)  # 将获取到的数据转化为列表
            for i in range(0, len(__) - self.last(__, '/')):
                _ += __[i]  # 将列表转为字符串,遇到最后一个/后停止
            #  _=  https://www.meinvheisi.cn/page/
            #     print(_)
            # print(__)
            conm = 0
            for url in __temp:
                url = url.split('/')[4]
                # print(url)
                url = int(url, 10)
                if url >= conm:
                    conm = url
            __temp = []
            for i in range(1, conm+1):
                # print(1,i)
                # print(2,_ + str(i))
                __temp.append(_ + str(i))
        return __temp

    # 获取页面网址的
    def Get_Tab_Page(self, html: list):
        print(sys._getframe().f_code.co_name + "开始运行")
        # html = BeautifulSoup(html, "html.parser")  # 文档对象
        for i in html:
            href = etree.tostring(i, encoding='utf-8').decode('utf-8')
            # print(type(href))
            href = BeautifulSoup(href, "html.parser")  # 文档对象
            for i in href.find_all('a'):
                href = i["href"]
                self.start_urls.append(href)
                self.file_log.debug("将{}加入到开始列表".format(href))

    # 获取浏览器代理的
    def Get_Browser_Model(self) -> str:
        print(sys._getframe().f_code.co_name + "开始运行")
        if self.browser == "QQ浏览器":  # android QQ浏览器
            model = 'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
        elif self.browser == "Edge":  # Edge
            model = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62"
        elif self.browser == "Chrome":
            model = " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        elif self.browser == "iPhone_6":
            model = 'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"'

        else:  # Edge
            model = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62"

        return model

    # 创建网络连接
    def Chrom_Options(self):
        opt = webdriver.ChromeOptions()
        opt.headless = True  # 开启无界面版的  windows/Linus  都可以使用
        opt.add_argument(self.Get_Browser_Model())
        opt.add_argument('blink-settings = imageEnabled=flase')
        Chrome = webdriver.Chrome(options=opt)  # 创建一个会话
        return Chrome

    # 获取主网址
    def Request_Prepare(self):
        print(sys._getframe().f_code.co_name + "开始运行")
        if com == True:
            test = 235
        chrome = self.Chrom_Options()
        try:
            chrome.get(self.start_url)
            temp = chrome.page_source
            temp = self.Html_Tag_Con(temp)  # 这个是获取基本HTML的内容
            temp = etree.HTML(temp)
            # print(1,self.Config_Dict["main_page_xpath"])
            # print(2,type(self.Config_Dict["main_page_xpath"]))
            page = temp.xpath(self.Config_Dict["main_page_xpath"])
            self.Get_Tab_Page(page)
            # https://www.meinvheisi.cn/page/2
            _ = str()
            __ = self.start_urls[0]
            __ = list(__)
            for i in range(0, len(__)-1):
                _ += __[i]
            #  _=  https://www.meinvheisi.cn/page/
            #     print(_)
            # print(__)
            conm = 0
            for url in self.start_urls:
                url = url.split('/')[4]
                url = int(url, 10)
                if url >= conm:
                    conm = url
            # print(conm)
            self.start_urls = []
            for i in range(1, conm-test):
                self.start_urls.append(_ + str(i))
            print("主网页爬取列表:", self.start_urls)
        except selenium.common.exceptions.WebDriverException:
            self.file_log.critical("网络异常")
        finally:
            chrome.close()

    # 获取主页下级页面网址
    def Lower_Page(self):
        print(sys._getframe().f_code.co_name+"开始运行")
        chrome = self.Chrom_Options()
        try:
            for url in self.start_urls:
                chrome.get(url)
                temp = chrome.page_source  # 当前标签页浏览器渲染之后的网页源代码 返回为str
                temp = self.Html_Tag_Con(temp)  # 这个是获取基本HTML的内容
                temp = etree.HTML(temp)  # 转变为一个etree对象
                temp_ = temp.xpath(self.Config_Dict["main_title_xpath"])
                self.requests_url = self.Get_Request_Url(
                    temp_, 'a', "href", "title")
                print("self.requests_url:", self.requests_url)
                self.start_urls.remove(url)
        except selenium.common.exceptions.WebDriverException:
            self.file_log.critical("网络异常")
        finally:
            chrome.close()

    # 获取图片网址        未完成
    def Wildcard_Character(self):
        print(sys._getframe().f_code.co_name + "开始运行")
        chrome = self.Chrom_Options()
        try:
            for key in self.requests_url:
                chrome.get(self.requests_url[key])
                temp = chrome.page_source
                temp = self.Html_Tag_Con(temp)  # 这个是获取基本HTML的内容
                # with open("./html1.html","w",encoding="utf-8") as f:
                #     f.write(temp)
                temp = etree.HTML(temp)  # 转变为一个etree对象
                temp_ = temp.xpath(
                    "/html/body/div[3]/div/div/div[3]/div/div[2]")
                # print(temp_)
                page_url = self.Get_Request_Url_List(temp_, "a", "href")
                print("page_url:", page_url)
                if page_url == None:
                    return
                for u in page_url:
                    chrome.get(u)
                    temp = chrome.page_source
                    temp = self.Html_Tag_Con(temp)  # 这个是获取基本HTML的内容
                    temp = etree.HTML(temp)  # 转变为一个etree对象
                    try:
                        temp_ = temp.xpath(
                            self.Config_Dict["wildcard_url_xpath"])
                        self.download_urls = self.Get_Request_Url(
                            temp_, "img", "src", "alt")
                        try:
                            self.Dict_Combination(key)
                        except KeyError:
                            self.file_log.warning("没有这个键值对")
                    except KeyError:
                        self.file_log.critical("没有找到{}".format(
                            self.Config_Dict["wildcard_url_xpath"]))
                # finally:
                #     print("程序没运行")
        except selenium.common.exceptions.WebDriverException:
            self.file_log.critical("网络异常")
        finally:
            chrome.close()

    # 将拼成json类型的
    def Dict_Combination(self, key):
        print("self.download_urls:", self.download_urls)
        print(sys._getframe().f_code.co_name + "开始运行")
        for key2 in self.download_urls:
            # print("Dict_Combination",self.download_urls[key2])
            self.combination[self.start_url][key][key2] = self.download_urls[key2]
        print("self.combination:", self.combination)

    # 自定义下载图片函数
    def Load_Page(self, url: str) -> bytes:
        print(sys._getframe().f_code.co_name + "开始运行")
        response = requests.get(url)
        '''
        response.content
        - 类型：bytes
        - 解码类型： 没有指定 
        - 如何修改编码方式：response.content.deocde(“utf-8”)
        '''
        data = response.content     # 通过response.content来获取图片的数据流
        return data

    '''
            :param stater:str   为图片还是json数据
            :param subtitle:str 为三级目录名字
            :patam image_title:str 为图片名字
            :param picture_data:bytes 为图片数据
     '''

    # 保存图片
    def Save(self, stater: str, subtitle: str, image_title: str, picture_data: bytes):
        print(sys._getframe().f_code.co_name + "开始运行")
        download_main_path = os.path.join(
            "./", self.main_title)  # 主目录的标题  ./美女黑丝
        if os.path.isdir(download_main_path):
            # print("目录:{}存在".format(download_main_path))
            if stater == "image":
                download_title = os.path.join(
                    download_main_path, "Image")  # 副目录的标题     ./美女黑丝/图片/
                if os.path.isdir(download_title):
                    download_title1 = os.path.join(download_main_path,
                                                   stater, subtitle)  # 副目录的标题     ./美女黑丝/图片/[秀人网XiuRen] No.2740 @王雨纯 -翘臀美腿销魂诱惑写真
                    if os.path.isdir(download_title1):
                        # page_con2 = str(self.page_con)
                        try:
                            page_path = image_title + ".jpg"
                            page_path = os.path.join(
                                download_title1, page_path)
                            # print(page_path)
                            with open(page_path, "wb") as page_name:
                                page_name.write(picture_data)
                                self.file_log.debug("{}下载完成".format(page_path))
                        except FileNotFoundError:
                            self.file_log.warning(
                                "{}.jpg文件创建失败".format(image_title))
                        except TypeError:
                            self.file_log.warning(
                                "{}.jpg文件写入失败".format(image_title))
                    else:
                        self.file_log.debug("目录:{}不存在".format(image_title))
                        os.mkdir(download_title1)
                        self.Save(stater, subtitle, image_title, picture_data)
                else:
                    self.file_log.debug("目录:{}不存在".format(subtitle))
                    os.mkdir(download_title)
                    self.Save(stater, subtitle, image_title, picture_data)
            elif stater == "cvs":
                download_title = os.path.join(download_main_path, "cvs")
                if os.path.isdir(download_title):
                    try:
                        page_path = subtitle + ".cvs"
                        page_path = os.path.join(download_title, page_path)
                        with open(page_path, "wb") as page_name:
                            page_name.write(picture_data)
                            self.file_log.debug("{}写入完成".format(page_path))
                    except FileNotFoundError:
                        self.file_log.warning("{}.cvs文件创建失败".format(subtitle))
                    except TypeError:
                        self.file_log.warning("{}.cvs文件写入失败".format(subtitle))
                else:
                    self.file_log.debug("目录:{}不存在".format(image_title))
                    os.mkdir(download_title)
                    self.Save(stater, subtitle, image_title, picture_data)
            elif stater == "json":
                download_title = os.path.join(download_main_path, "Json")
                if os.path.isdir(download_title):
                    try:
                        page_path = subtitle + ".json"
                        page_path = os.path.join(download_title, page_path)
                        with open(page_path, "wb") as page_name:
                            page_name.write(picture_data)
                            self.file_log.debug("{}写入完成".format(page_path))
                    except FileNotFoundError:
                        self.file_log.warning("{}.json文件创建失败".format(subtitle))
                    except TypeError:
                        self.file_log.warning("{}.json文件写入失败".format(subtitle))
                else:
                    self.file_log.debug("目录:{}不存在".format(image_title))
                    os.mkdir(download_title)
                    self.Save(stater, subtitle, image_title, picture_data)
        else:
            self.file_log.debug("目录:{}不存在".format(self.main_title))
            os.mkdir(download_main_path)
            self.Save(stater, subtitle, image_title, picture_data)

    # 图片处理   可多线程处理
    def Save_Image(self, download_url: str, subtitle: str, image_title: str, main_title: str):
        # self.download_url = 'https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/41493/2.jpg'
        self.download_url = download_url
        # self.main_title = "美女黑丝"
        self.main_title = main_title
        picture_data = self.Load_Page(self.download_url)
        # self.Save("json", "[秀人网XiuRen] No.2740 @王雨纯 -翘臀美腿销魂诱惑写真","[秀人XiuRen] No.2740 王雨纯_1", picture_data)
        self.Save("image", subtitle, image_title, picture_data)

    # json处理   可多线程处理
    def Save_Json(self, json_bytes: bytes, secondary_website_url: str, main_title: str):
        self.main_title = main_title
        picture_data = json_bytes
        # self.Save("json", "[秀人网XiuRen] No.2740 @王雨纯 -翘臀美腿销魂诱惑写真","", picture_data)
        self.Save("json", secondary_website_url, "", picture_data)

    # json处理   可多线程处理
    def Save_Cvs(self, cvs_bytes: bytes, secondary_website_url: str, main_title: str):
        self.main_title = main_title
        picture_data = cvs_bytes
        # self.Save("json", "[秀人网XiuRen] No.2740 @王雨纯 -翘臀美腿销魂诱惑写真","", picture_data)
        self.Save("cvs", secondary_website_url, "", picture_data)

    # 开始爬取控制函数
    def Start_Requests(self):
        print(sys._getframe().f_code.co_name + "开始运行")
        # from selenium.webdriver.chrome import options
        self.combination[self.start_url] = {}
        self.Get_Web_Config()  # 网站各种配置配置
        self.Request_Prepare()  # 获取主网址
        self.Lower_Page()  # 获取下级页面网址
        for key1 in self.requests_url:
            if self.requests_url[key1] == None:
                print("self.requests_url[key1]:", "key:{}这是空".format(key1))
                break
            self.combination[self.start_url][key1] = {}
        self.Wildcard_Character()
        # chrome = self.Chrom_Options()
        try:
            # print(self.start_urls)
            # print(self.combination)
            # self.Save_Image()
            pass
        except selenium.common.exceptions.WebDriverException:
            self.file_log.critical("网络异常")
        finally:
            # chrome.close()
            with open("./test.json", "w", encoding="utf-8") as f:
                f.write(str(self.combination))
        """
        from selenium import webdriver

        browser = webdriver.Chrome()
        browser = webdriver.Firefox()
        browser = webdriver.Edge()
        browser = webdriver.PhantomJS()
        browser = webdriver.Safari()
        查找节点的方法:
            find_element_by_id()
            find_element_by_name()
            find_element_by_xpath()
            find_element_by_link_text()
            find_element_by_partial_link_text()
            find_element_by_tag_name()
            find_element_by_class_name()
            find_element_by_css_selector() 
            如果符合条件的节点有多个，则再使用find_element()系列的方法就只能得到匹配列表中第
              一个符合条件的节点了，要想拿到所有匹配成功的节点，则需要使用find_elements()系列的
              方法。
        """


def main():
    re = My_Requests(url="https://www.meinvheisi.cn/ ", browser="Chrome")
    # re.Save_Image("https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/37781/1.jpg",
    #                     "[喵糖映画] VOL.254 @绮太郎 粉系水手萌妹",
    #                     "[喵糖映画] VOL.254 绮太郎 粉系水手萌妹_1",
    #                     "美女黑丝")
    # re.Save_Json(
    #     bytes("{\"[喵糖映画] VOL.254 @绮太郎 粉系水手萌妹\": {\"[喵糖映画] VOL.254 绮太郎 粉系水手萌妹_1\": \"https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/37781/1.jpg\",\
    #             \"[喵糖映画] VOL.254 绮太郎 粉系水手萌妹_2\": \"https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/37781/2.jpg\"}}",encoding="utf-8"
    #             ),
    #     "[喵糖映画] VOL.254 @绮太郎 粉系水手萌妹",
    #     "美女黑丝")
    re.Save_Cvs(
        bytes("{\"[喵糖映画] VOL.254 @绮太郎 粉系水手萌妹\": {\"[喵糖映画] VOL.254 绮太郎 粉系水手萌妹_1\": \"https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/37781/1.jpg\",\
                \"[喵糖映画] VOL.254 绮太郎 粉系水手萌妹_2\": \"https://img.91cinema.cn/tjg/index.php?url=https://tjg.gzhuibei.com/a/1/37781/2.jpg\"}}", encoding="utf-8"
              ),
        "[喵糖映画] VOL.254 @绮太郎 粉系水手萌妹",
        "美女黑丝")
    # re.Start_Requests()
    # a = list("https://www.meinvheisi.cn/dalumeinv_19179/10")
    # t = re.test(a)
    # print(a)
    # print(t)

    re.Save()


if __name__ == '__main__':
    main()
