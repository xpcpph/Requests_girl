# Requests_girl
## 目前完成的模块有:
+ log.py
+ web.py

## myrequests.py 其实可以正常使用但是有一些没有完成的功能,例如视频下载,已下载的文件的防止再次爬取拉低性能等
## 后续还有一些功能:
+ 图形界面
+ 数据库操作
+ 多线程的使用/多协成使用等
+ 
## web.conf内容讲解:
```
; 主要的一些配置
[root]
;	mysql的账户名
mysql_name=root	
;	mysql的密码			
mysql_passwd=123456

;网址,网址的规则为http://www.taobao.com
[https://www.meinvheisi.cn/ ]
;	是否保存网址,默认为False(不保存)
save_url = False
;	是否保存图片,默认为True(保存)
save_picture = True
;	是否保存视屏,默认为False(不保存)
save_video = False
;	保存路径,包括保存图片/和保存网址的路径
save_path = "./"
;	False不需要遵循,True为循序必要的爬取规则
rule_crawl = False
; 图片 Url 的爬取通配符
wildcard_url_xpath = /html/body/div[3]/div/div/div[3]/div/p
; 图片名字的爬取通配符
wildcard_title_xpath = ""
; 用户名
user_name = ""
; 用户密码
user_passwd = ""
; 主网页下一页的爬取通配符
main_page_xpath = /html/body/div[4]/div/nav/div/a[*]
; 主页面列表图片的爬取通配符,包含名字与下级页面Url
main_title_xpath = /html/body/div[4]/div/ul/li[*]/a
;主页面的链接通配符
main_href_xpath = ""
```

##loguser.conf讲解
```
;	logger提供了应用程序可以直接使用的接口，logger里面的每一个keys在下面还要写一个块，
;	用来单独的配置；
;	这里设置的是这一类的名字
[loggers]
;	配置logger信息。必须包含一个名字叫做root的logger，当使用无参函数logging.getLogger()
;	时，默认返回root这个logger，其他自定义logger可以通过
;	logging.getLogger("fileAndConsole") 方式进行调用
;	level可以是DEBUG, INFO, WARNING, ERROR, CRITICAL 或 NOTSET其中之一。
;	NOTSET表示所有的消息都要记录，这只对根logger有效
	keys=root,file,fileAndConsole       ;可以没有其他但是必须有root

;	handler将(logger创建的)日志记录发送到合适的目的输出，
;	    handler里面的每一个keys也是要在下面还要写一个块，用来单独的配置；
;	    (用来控制将日志输出到控制台/文件/
;	    将日志输出保存到文件中，并设置单个日志文件的大小和日志文件个数)
;	这里设置的是这一类的名字
[handlers]
;	定义声明handlers信息,其中包含两个handlers
keys=fileHandler,consoleHandler

;	这里设置的是这一类的名字
[formatters]
;	设置日志格式
keys=simpleFormatter

[logger_root]
;	对loggers中声明的logger进行逐个配置，且要一一对应,在所有的logger中，
;	必须制定lebel和handlers这两个选项，对于非roothandler，还需要添加一些额外的option，
;	其中qualname表示它在logger层级中的名字，在应用代码中通过这个名字制定所使用的handler，
;	即 logging.getLogger("fileAndConsole")，handlers可以指定多个，中间用逗号隔开，
;	比如handlers=fileHandler,consoleHandler，同时制定使用控制台和文件输出日志

level=DEBUG
handlers=consoleHandler

[logger_file]
level=DEBUG
handlers=fileHandler
qualname=file
;	progarate:是否将日志传给上游（多级上游，顶级为root,以foo.A.B类似表示，
;    	foo就是A,B的顶级，A就是B的父级）
propagate=1

[logger_fileAndConsole]
level=DEBUG
handlers=fileHandler,consoleHandler
qualname=fileAndConsole
propagate=0

[handler_consoleHandler]
;	 在handler中，必须指定class和args这两个option，常用的class包括
;	StreamHandler（仅将日志输出到控制台）、
;	FileHandler（将日志信息输出保存到文件）、
;	RotaRotatingFileHandler（将日志输出保存到文件中，
;	    并设置单个日志文件的大小和日志文件个数），
;	args表示传递给class所指定的handler类初始化方法参数，它必须是一个元组（tuple）的形式，
;	即便只有一个参数值也需要是一个元组的形式；里面指定输出路径，比如输出的文件名称等。
;	level与logger中的level一样，而formatter指定的是该处理器所使用的格式器，
;	这里指定的格式器名称必须出现在formatters这个section(日志的输出流)中，
;	且在配置文件中必须要有这个formatter的section定义；
;	如果不指定formatter则该handler将会以消息本身作为日志消息进行记录，
;	而不添加额外的时间、日志器名称等信息；

;	sys.stdin      默认的情况下，它将结果打印到屏幕上;
;	sys.stdout     stdout用于print和状态表达式的结果输出，及input（）的瞬时输出(为了保存记录，可以修改sys__stdin__的输出结果为某个文件;)
;	sys.stdeer     .在2的基础上，进行print()时，print等价于write，结果直接写入文件。

class=StreamHandler
args=(sys.stdout,)
level=DEBUG
formatter=simpleFormatter

[handler_fileHandler]
class=FileHandler
;	元组中包含文件名和权限
args=('dialog-analysis.log', 'a')
level=DEBUG
;	这个设置成True时,只有写入内容时才创建文件
delay=True
;when=S/M/H/D/W/
;	S           以年切割
;	M           以分钟切割
;	H           以小时切割
;	D           以天切割
;	midnight    以每天午夜切割
;	W           以周切割(在某一天切割,0是星期天)
;设置格式化方式
formatter=simpleFormatter

[formatter_simpleFormatter]
format=%(asctime)s - %(module)s - %(thread)d - %(levelname)s : %(message)s
;	%(asctime)s   易读的时间格式： 默认情况下是’2003-07-08 16：49：45,896’的形式
;	                （逗号之后的数字是毫秒部分的时间）
;	%(module)s      所在的模块名(如test6.py模块则记录test6)
;	%(thread)d      线程ID
;	%(levelname)s   消息的级别名称
;	                (‘DEBUG’, ‘INFO’, ‘WARNING’, ‘ERROR’, ‘CRITICAL’).
;	%(message)s     记录的信息
;	日期格式化
datefmt=%Y-%m-%d %H:%M:%S     ;时间格式
```
