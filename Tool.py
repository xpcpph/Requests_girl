import os

import chardet
import gzip

from log import *


# import time


class Tool_MiXin(Record_Log):
    #     检查文件是否可以使用
    def Information_Config_File(self,web_path):
        # 检查文件是否还存在
        file_log = self.File_Log()
        if os.path.isfile(web_path):
            if os.access(web_path, os.F_OK):
                file_log.info("{0} 存在文件路径.".format(web_path))
            else:
                file_log.info("{0} 不存在文件路径.".format(web_path))
                return False

            if os.access(web_path, os.R_OK):
                file_log.info("{0} 文件可访问".format(web_path))
            else:
                file_log.info("{0} 不存在文件路径.".format(web_path))
                return False

            if os.access(web_path, os.W_OK):
                file_log.info("{0} 文件可以写入".format(web_path))
            else:
                file_log.info("{0} 不存在文件路径.".format(web_path))
                return False

            if os.access(web_path, os.X_OK):
                file_log.info("{0} 执行文件可访问".format(web_path))
            else:
                file_log.info("{0} 不存在文件路径.".format(web_path))
                return False
            return True
        else:
            file_log.warning("配置文件不存在")

    # 解压gzip压缩的网页
    def GzdeCode(self, data) -> object:
        charset = chardet.detect(data)['encoding']
        if charset == None:
            charset = 'utf-8'
        if charset.lower() == 'gb2312':
            charset = 'gb18030'
        try:
            html = gzip.decompress(data).decode(charset)
        except OSError:
            html = data.decode(charset)
        return html

    # 通过值来获取键
    def GetDictKey(self, mydict, value):
        keyList = []
        for k, v in mydict.items():
            if v == value:
                keyList.append(k)
        return keyList

#装饰类  获取运行时间
class Get_Run_Time():
    def __init__(self,function) -> None:
        self.function = function

    def __call__(self, *args, **kwds):
        import time
        start = time.time()
        self.function( *args, **kwds)
        end = time.time()
        print(f"本函数执行时间一共用时:{end - start}s")


# 测试单元
def unittest_main(cls):
    import unittest
    unittest.main()
    return cls


if __name__ == '__main__':
    a = Tool_MiXin()
    # a.Information_Config_File("./aa")

    print(a)
