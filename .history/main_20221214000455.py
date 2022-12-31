# -*- coding: utf-8 -*-
'''
这是一个主程序入口,他通过调用各个模块来实行,信息的记录和图片的下载,网站的存活检测等
# https://www.meinvheisi.cn/     美女黑丝
# https://www.acg45.com/         瑶华映画
#暂时适配这两个网站
#函数名使用首字母大写的方式
#变量名使用全小写的方式

一共有三种日志：
    一.错误日志：将记录的是所有程序运行错误的日志
    二.运行日志：将记录的是爬虫所有爬取的网址或图片等一系列运行是的日志
    三.下载日志：将记录的是所有的下的图片和视频

@   Decorator装饰器
->  在定义函数后使用告诉开发者本函数的返回类型

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('followall', domain='scrapinghub.com')
process.start() # the script will block here until the crawling is finished
    注释颜色:
    !   红色(!)
    ?   蓝色(?)
    *   绿色(*)
    ^   黄色(^)
    &   粉色(&)
    ~   紫色(~)
    todo 深黄色(todo)
    // 灰色(//)

'''
import sys,string,os,time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy
from sto.items import StoItem
from sto.pipelines import StoPipeline
import  sto.settings



test = True     # 用来控制Remove_Temp_File()的执行,相当于c语言中的if define


def Remov_Temp_File(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("删除成功!")
    else:
        print("没有这个{0}文件".format(file_path))

if test == True:
    Remov_Temp_File("./logging.log")

else:
    pass

from web_state import *
from log import *
file_log = Log_Config('fileLogger')
console_log = Log_Config('fileAndConsole')
url = ""        #全局变量url

'''
    这是一个命令处理函数，可以通过命令来实现网站的爬取
'''
object

class Command(object):
    def __init__(self):
        self.args = sys.argv[1:]

    def Data_Command(self,command) -> string:
        return command.split("=")

    def Processing_Command(self):
        global url  # 将局部变量升级为全局变量,使用 global 关键字
        # print(1)
        # print(self.args)
        for i in self.args:
            # print(type(i))
            # print(i)
            data_temp = self.Data_Command(i)  #获取
            # print(data_temp)

            if i:
                if data_temp[0] == "--url":
                    try:    #进行异常捕获
                        url = data_temp[1]
                        # print(url)
                        '''
                            缺少处理网址的函数,去除网址头
                        '''
                        self.Web_Url_Start(url)
                        file_log.debug("访问的网址是{}".format(url))
                    except IndexError:
                        file_log.critical("超出索引范围.")    #致命错误

                elif data_temp[0] == "--help":
                    print("eg: main.py [-u=\"网址\"]/[--url=\"网址\"]")
                    print("这个暂时只有一个参数是 --url/-u")
                elif data_temp[0] == "-h":
                    print("eg: main.py [-u=\"网址\"]/[--url=\"网址\"]")
                    print("这个暂时只有一个参数是 --url/-u")
            else:
                print("eg: main.py [-u=\"网址\"]/[--url=\"网址\"]")
                print("这个暂时只有一个参数是 --url/-u")
    '''
        逻辑：输入url后检测是否带有http://(https://)后输出
    '''
    def  Web_Url_Start(self,temp_url):
        global url  # 将局部变量升级为全局变量,使用 global 关键字
        url = temp_url.split("://")
        if len(url) == 2:
            url = "http://"+url[1]
        else:
            url = "http://"+url[0]
        # print(url)



'''
 创建爬取列表文件，
 思考：在文件级别的处理是否过于缓慢
        中的处理有增，删，改，查，
'''
class Requests_List():
    def __init__(self):
        pass



def main():
    # process = CrawlerProcess(get_project_settings())
    # settings = get_project_settings()
    # print(settings)
    # print(settings.get(settings.get('BOT_NAME')))
    com = Command()
    com.Processing_Command()
    # print(url)
    web = Web(url)
    print("在此之前提取配置文件")
    # # time.sleep(100)
    try:
        if web.Web_state():
            # web.Web_Config_Parsing()    #这个是获取web的配置文件
            # a,b=web.Web_Create_List()
            # print(a)
            # print(b)
            # file_log.warning()
            pass
    except requests.exceptions.MissingSchema:
        file_log.critical("requests.exceptions.MissingSchema 没有url")

if __name__ == "__main__":
    main()
