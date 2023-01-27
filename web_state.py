# -*- coding: utf-8 -*-
'''
本模块关于web相关的,

'''
import configparser

import requests

from log import *


class Web(Record_Log):
    '''
           配置文件节点内容增加时,需要改动
    '''
    def __init__(self,*url):
        super().__init__()
        self.url = url[0]
        self.web_path = './web.conf'
        #初始化变量,进行初始的副值
        #    是否保存网址, 默认为no(不保存)
        self.save_url = True
        #    是否保存图片, 默认为yes(保存)
        self.save_picture = True
        #    是否保存视屏, 默认为no(不保存)
        self.save_video = False
        #    保存路径, 包括保存图片 / 和保存网址的路径, 不填则为本目录下, 本脚本自动创建
        self.save_path = './'
        #    no不需要遵循, yes为循序必要的爬取规则
        self.rule_crawl = False
        #    适应本网站提取网址的通配符, 必须填
        self.wildcard_url_xpath = ""
        #    适应本网站提取标题的通配符, 必须填
        self.wildcard_title_xpath = ""
        #网站的用户名, 可以不用填, 不填为空
        self.user_name = ""
        #网站密码, 可以不用填, 不填为空
        self.user_passwd = ""
        #主页面下的网页xpath路径
        self.main_page_xpath = ""
        #主页面下的标题xpath路径
        self.main_title_xpath = ""
        #主页面下的href xpath路径
        self.main_href_xpath = ""
        self.file_log = self.Log_Config("fileLogger")
        #此列表为配置文件中网址那一栏所包含的东西
        self.argument_list = [
            "save_url",                         #0
            "save_picture",                     #1
            "save_video",
            "save_path",
            "rule_crawl",
            "wildcard_url_xpath",
            "wildcard_title_xpath",
            "user_name",
            "user_passwd",
            "main_page_xpath",
            "main_title_xpath",
            "main_href_xpath"
        ]
        self.Web_Config_Parsing()

    '''
           配置文件节点内容增加时,需要改动
           
    '''
    def Web_Config_Parsing(self):
        # print(self.web_path)
        config = configparser.ConfigParser()
        # config.sections()
        config.read(self.web_path,encoding='utf-8')      #读取配置文件
        # print(config.sections())                #读取所有节点,主节点
        # print(config.options(self.url))          #读取主节点下所有数据
        if config.has_section(self.url):
            try:
                '''     获取配置数据     '''
                self.save_url = config.get(self.url, self.argument_list[0])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[0],self.save_url))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[0],"False")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[0],"False"))

            try:
                self.save_picture = config.get(self.url, self.argument_list[1])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[1],self.save_picture))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[1], "True")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[1],"True"))

            try:
                self.save_video = config.get(self.url, self.argument_list[2])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[2],self.save_video))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[2], "False")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[2],"False"))

            try:
                self.save_path = config.get(self.url, self.argument_list[3])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[3],self.save_path))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[3], "\"./\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[3],"./"))

            try:
                self.rule_crawl = config.get(self.url, self.argument_list[4])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[4],self.rule_crawl))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[4], "False")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[4],"False"))

            try:
                self.wildcard_url_xpath = config.get(self.url, self.argument_list[5])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[5],self.wildcard_url_xpath))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[5], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[5],""))

            try:
                self.wildcard_title_xpath = config.get(self.url, self.argument_list[6])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[6], self.wildcard_title_xpath))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[6], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url, self.argument_list[6], ""))

            try:
                self.user_name = config.get(self.url, self.argument_list[7])
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[7],self.user_name))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[7], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[7],""))

            try:
                self.user_passwd = config.get(self.url, self.argument_list[8]) #读取主节点下的副节点对应的值
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[8],self.user_passwd))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[8], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[8],""))

            try:
                self.main_page_xpath = config.get(self.url, self.argument_list[9]) #读取主节点下的副节点对应的值
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[9],self.main_page_xpath))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[9], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning("在{}下{}节点下写入{}键{}值".format(self.web_path, self.url,self.argument_list[9],""))

            try:
                self.main_title_xpath = config.get(self.url, self.argument_list[10])  # 读取主节点下的副节点对应的值
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[10], self.main_title_xpath))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[10], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning(
                    "在{}下{}节点下写入{}键{}值".format(self.web_path, self.url, self.argument_list[10], ""))

            try:
                self.main_href_xpath = config.get(self.url, self.argument_list[11])  # 读取主节点下的副节点对应的值
                self.file_log.debug("读取到{}的配置为{}".format(self.argument_list[11], self.main_href_xpath))
            except configparser.NoOptionError:
                config.set(self.url, self.argument_list[11], "\"\"")
                config.write(open(self.web_path, "w"))
                self.file_log.warning(
                    "在{}下{}节点下写入{}键{}值".format(self.web_path, self.url, self.argument_list[11], ""))
        else:
            print(type(self.url))
            print(self.url)
            config.add_section(self.url)
            self.file_log.warning("在{}下写入{}节点".format(self.web_path,self.url))
            config.write(open(self.web_path, "w"))

            config.remove_section("default")  # 整个section下的所有内容都将删除

            config.write(open(self.web_path, "w"))
            self.Web_Config_Parsing()



        # v = configparser.getboolean(self.save_video)
        # config.set("mysql", "mysql_port", "69")  # 修改db_port的值为69
        # config.write(open("ini", "w"))  #创建名为ini的文件
        # 最后一个类型的处理最为有趣，因为简单地将值传给bool()
        # 是没有用的，bool('False')仍然会是True。 为解决这个问题配置解析器还提供了
        # getboolean()。 这个方法对大小写不敏感并可识别
        # 'yes' / 'no', 'on' / 'off', 'true' / 'false'和'1' / '0'等布尔值。
        #在此个配置文件中可以用英文分号来进行注释

    def Web_state(self):        #检测网站是否可以访问
        try:
            re = requests.get(self.url)
            if re.ok:
                self.file_log.info("{}是可以正常访问的".format(self.url))
                return True
            else:
                self.file_log.info("{}是无法正常访问的".format(self.url))
                return False
        except requests.exceptions.ConnectionError:
            self.file_log.critical("{} 链接超时".format(self.url))
            return False
    '''
        配置文件节点内容增加时,需要改动
        更改:把返回的列表改为键值对形势(字典)
    '''
    def Web_Create_Dict(self) -> dict:
        temp_dict = {}
        temp_dict.update({
            self.argument_list[0]:self.save_url,
            self.argument_list[1]:self.save_picture,
            self.argument_list[2]: self.save_video,
            self.argument_list[3]: self.save_path,
            self.argument_list[4]: self.rule_crawl,
            self.argument_list[5]: self.wildcard_url_xpath,
            self.argument_list[6]: self.wildcard_title_xpath,
            self.argument_list[7]: self.user_name,
            self.argument_list[8]: self.user_passwd,
            self.argument_list[9]: self.main_page_xpath,
            self.argument_list[10]: self.main_title_xpath,
            self.argument_list[11]: self.main_href_xpath,
        })
        return dict(temp_dict)





def main():
    we = Web('https://www.taobao.com')
    we.Web_Config_Parsing()
    we.Web_state()
    we.Web_Create_Dict()

if __name__ == "__main__":
    main()