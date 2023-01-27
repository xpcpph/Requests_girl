# -*- coding: utf-8 -*-

'''
这是一个日志记录模块中包含,错误日志,运行日志,本程序运行配置日志
'''
__all__ = [
    "Record_Log",
]

import logging
import os
import stat
import time


class Record_Log(object):
    def __init__(self):
        self.file_path = "./logging.log"

    def File_State(self):       #检测文件是否存在/可用,不可用就创建或更改权限
        if os.path.isfile(self.file_path):
            if os.access(self.file_path, os.F_OK):   #判断路径是否存在
                # print("Given file path is exist.")

                os.chmod(self.file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            if os.access(self.file_path, os.R_OK):    #判断文件是否可读
                # print("File is accessible to read")
                os.chmod(self.file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            if os.access(self.file_path, os.W_OK):    #判断文件是否可写
                # print("File is accessible to write")
                os.chmod(self.file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            # if os.access("/file/path/foo.txt", os.X_OK):    #
            #     print("File is accessible to execute")
            #     return
        else:
            print("文件正在创建,请稍后...")
            file_temp = open(self.file_path,"a+")
            file_temp.close()
            time.sleep(2.5)
            print("创建成功!")
            print("正在更改文件权限,请稍后...")
            os.chmod(self.file_path,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)       #更改文件权限为777
            time.sleep(2.5)
            print("文件更改成功!")
            self.File_State()

    def Remov_File(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
            print("删除成功!")
        else:
            print("没有这个{0}文件".format(self.file_path))

    def Log_Config(self, logname: str) -> logging:
        import logging.config
        # '读取日志配置文件'
        path = r'./loguser.conf'
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                logging.config.fileConfig(f)
        #logging.getLogger中的name与配置文件中的qualname名字保持一致即可调用配置文件中的配置进行控制
        file_logger = logging.getLogger(name=logname)
        # 日志等级: notset > debug > info > warning > error > critical

        # logger.debug('debug级别，一般用来打印一些调试信息，级别最低')
        # logger.info('info级别，一般用来打印一些正常的操作信息')
        # logger.warning('waring级别，一般用来打印警告信息')
        # logger.error('error级别，一般用来打印一些错误信息')
        # logger.critical('critical级别，一般用来打印一些致命的错误信息，等级最高')

        return file_logger
    
    @property       #添加这个后可以直接使用属性名来使用,不需要加()来使用
    def File_Log(self):
        file_log = self.Log_Config('fileLogger')
        return file_log

    @property
    def Console_Log(self):
        console_log = self.Log_Config('fileAndConsole')
        return console_log

def main():
    cass = Record_Log()
    cass.File_State()
    file_log = cass.Log_Config('fileLogger')
    console_log = cass.Log_Config('fileAndConsole')
    file_log.debug("test")
    console_log.warning("test")
    # file_log = cass.File_Log()
    file_log.debug("test")

if __name__ == "__main__":
    main()