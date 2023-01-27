### list

# -*- coding: utf-8 -*-
# Python中sys模块：该模块提供对解释器使用或维护的一些变量的访问，以及与解释器强烈交互的函数

# sys.argv #命令行参数List，第一个元素是程序本身路径
# sys.modules.keys() #返回所有已经导入的模块列表
# sys.exc_info() #获取当前正在处理的异常类,exc_type、exc_value、exc_traceback当前处理的异常详细信息
# sys.exit(n) #程序，正常退出时exit(0)
# sys.hexversion #获取Python解释程序的版本值，16进制格式如：0x020403F0
# sys.version #获取Python解释程序的版本信息
# sys.maxint #最大的Int值
# sys.maxunicode #最大的Unicode值
# sys.modules #返回系统导入的模块字段，key是模块名，value是模块
# sys.path #返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值
# sys.platform #返回操作系统平台名称
# sys.stdout #标准输出
# sys.stdin #标准输入
# sys.stderr #错误输出
# sys.exc_clear() 	#用来清除当前线程所出现的当前的或最近的错误信息
# sys.exec_prefix 	#返回平台独立的python文件安装的位置
# sys.byteorder 		#本地字节规则的指示器，big-endian平台的值是'big',little-endian平台的值是'little'
# sys.copyright 		#记录python版权相关的东西
# sys.api_version 	#解释器的C的API版本
# sys.version_info 	#获取Python解释器的版本信息
# sys.getwindowsversion #获取Windows的版本
# sys.getdefaultencoding #返回当前你所用的默认的字符编码格式
# sys.getfilesystemencoding #返回将Unicode文件名转换成系统文件名的编码的名字
# sys.setdefaultencoding(name) #用来设置当前默认的字符编码
# sys.builtin_module_names 	#Python解释器导入的模块列表
# sys.executable 					#Python解释程序路径
# sys.stdin.readline 				#从标准输入读一行，sys.stdout.write("a") 屏幕输出a
