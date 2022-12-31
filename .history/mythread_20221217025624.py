# -*- coding: utf-8 -*-
#处理多线程任务


import threading
import _thread
import queue
import myrequests
import time
from os import getgid  as pid
import asyncio

exitFlag = 0
#互斥锁，用于线程对互斥资源的访问
queueLock = threading.Lock()
workqueue = queue.Queue(10)     #参数列表

class Web_Threading(threading.Thread,myrequests.My_Requests):
    def __init__(self, thread_id, thread_name,delay):
        threading.Thread.__init__(self)
        super().__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.delay = delay
        self.work_list = []

    #~生产者用   于产生数据
    #~对应的是提取网址放入待爬取列表

    #^消费者 用于处理数据
    #^对应的是重爬取列表中取出数据进行爬取


    #向workqueue中添加数据
    def Return_Num_Data(self):
        queueLock.acquire()
        num = 20
        # self.download_urls
        if num >= 20:
            pass
        else:
            if len(self.work_list) < num:
                with open("./download.cvs","a") as f:
                    for i in range(1,num):
                        self.work_list.append(f.readline())
            else:
                for i in self.work_list:
                    if True is not workqueue.full():
                        workqueue.put(i)
                        self.work_list.remove(i)
                        if workqueue.full():
                            return

    def run(self):
        print("开始线程：" + self.thread_name)
        process_data(self.thread_name, self.delay)
        print("退出线程：" + self.thread_name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workqueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
listqueue =[]



print("主进程开始")
threadID = 1
# 创建新线程
for tName in threadList:
    thread = Web_Threading(threadID, tName, workqueue)
    thread.start()
    listqueue.append(thread)
    threadID += 1

queueLock.acquire()
for i in nameList:
    # print(type(i))
    # i.join()
    workqueue.put(i)
queueLock.release()
# 等待队列清空
while not workqueue.empty():
    pass
# 通知线程是时候退出
exitFlag = 1

for t in listqueue:
    t.join()

print("主进程结束")

# if __name__ == "__main__":
#     main()

