# import threading
# from concurrent.futures import ThreadPoolExecutor
# import concurrent.futures
# import time,requests,os

# # urls = [
# #    str(i) for i in range(100)
# # ]
# urls = [
#         'https://www.baidu.com',
#         'https://www.sina.com.cn',
#         'https://www.tmall.com',
#         'https://www.jd.com',
#         'https://www.python.org',
#         'https://www.openstack.org',
#         'https://www.baidu.com',
#         'https://www.baidu.com',
#         'https://www.baidu.com',

#     ]

# def craw(url):
#     print(f"urls:{url}")
#     time.sleep(10)

# def get(url):
#     print('%s GET %s' % (os.getpid(),url))
#     time.sleep(3)
#     response = requests.get(url)
#     if response.status_code == 200:
#         res = response.text
#     else:
#         res = "下载失败"
#     str(res)
#     return res

# def parse(res):
#     time.sleep(1)
#     print("%s 解析结果为" %(os.getpid()))


# def a():
#     # print(urls)
#     start = time.time()
#     with ThreadPoolExecutor(9) as pool:
#         futurs = [
#             pool.submit(get,url) for url in urls
#         ]
#         pool.shutdown(wait=True)
#     for futur in futurs:
#         parse(futur.result)
#     end = time.time()
#     print("a的耗时:", end - start, "s")
# #进程池的同步调用方式
# def b():
#     start = time.time()
#     with ThreadPoolExecutor(9) as pool:
#         futurs = [
#             pool.submit(get, url) for url in urls
#         ]
#         pool.shutdown(wait=True)
#     for futur in concurrent.futures.as_completed(futurs):
#         parse(futur.result)
#     end = time.time()
#     print("b的耗时:", end - start, "s")
# def c():
#     start = time.time()
#     for url in urls:
#         parse(get(url))
#     end = time.time()
#     print("c的耗时:", end - start, "s")

# a()
# b()
# c()

import asyncio,time,Tool


# async def testa(): 
#     print('testa sleep start')
#     print(f"this is the testa")
#     await asyncio.sleep(1)

#     print('sleep end')

# async def testb(): 
#     print('testb sleep start')
#     print(f"this is the testb")
#     await asyncio.sleep(1)

#     print('sleep end')


# async def Run():
#     # resulta = await testa()
#     # resultb = await testb()
#     resulta,resultb = await asyncio.gather(testa(),testb())

# def test():
#     print("generator start")
#     n = 1
#     while True:
#         yield_expression_value = yield n
#         print("yield_expression_value = %d" % yield_expression_value)
#         n += 1
 
 
# # ①创建generator对象
# generator = test()
# print(type(generator))
 
# print("\n---------------\n")
 
# # ②启动generator
# next_result = generator.__next__()
# print("next_result = %d" % next_result)
 
# print("\n---------------\n")
 
# # ③发送值给yield表达式
# send_result = generator.send(666)
# print("send_result = %d" % send_result)


# @Tool.Get_Run_Time
# def main():
#     print("start")
#     # c = test() # 调用异步函数,得到协程对象-->c
#     loop = asyncio.get_event_loop() # 创建事件循环 
#     loop.run_until_complete(Run()) # 把协程对象丢给循环,并执行异步函数内部代码
#     print("end")
#     # b = Tool.logging
#     # print(b)
#     # a = dir(Tool)
#     # for i in range(0,len(a)):
#     #     print(i,a[i])

# if __name__ == "__main__":
#     main()

# def consumer():
#     print("[消费者] 开始")
#     r = '开始'
#     while True:
#         n = yield r
#         if not n:
#             print("n 是空的")
#             continue
#         print("[消费者] 消费者在消费 %s" % n)
#         r = "消费完了,请生产."
 
 
# def producer(c):
#     # 启动generator
#     start_value = c.send(None)
#     print(start_value)
#     n = 0
#     while n < 3:
#         n += 1
#         print("[生产者] 生产者在生产 %d" % n)
#         r = c.send(n)
#         print('[生产者] 消费者返回: %s' % r)
#     # 关闭generator
#     c.close()
 
 
# # 创建生成器
# c = consumer()
# # 传入generator
# producer(c)

# # 子生成器
# def test(n):
#     i = 0
#     while i < n:
#         yield i
#         i += 1
 
# 委派生成器
# def test_yield_from(n):
#     print("test_yield_from start")
#     yield from test(n)
#     print("test_yield_from end")

# @asyncio.coroutine
# def test_yield_from(n):
#     print("test_yield_from start")
#     yield from test(n)  #第一个生成器
#     print("test_yield_from doing")  
#     yield from test(n)  #第二个 生成器
#     print("test_yield_from end")
# #  使用@asyncio.coroutine装饰的函数称为协程。不过没有从语法层面进行严格约束。

# # 是否是协程函数
# print(asyncio.iscoroutinefunction(test_yield_from))
# # 是否是协程对象
# print(asyncio.iscoroutine(test_yield_from(3)))

# for i in test_yield_from(3):
#     print(i)

# import asyncio
 
# @asyncio.coroutine
# def compute(x, y):
#     print("Compute %s + %s ..." % (x, y))
#     yield from asyncio.sleep(1.0)
#     return x + y
 
# @asyncio.coroutine
# def print_sum(x, y):
#     result = yield from compute(x, y)
#     print("%s + %s = %s" % (x, y, result))
 
# loop = asyncio.get_event_loop()
# print("start")
# # 中断调用，直到协程执行结束
# loop.run_until_complete(print_sum(1, 2))
# print("end")
# loop.close()


# import asyncio
 
# async def compute1(x, y):
#     print("Compute %s + %s ..." % (x, y))
#     await asyncio.sleep(1.0)
#     return x + y
 
# async def print_sum1(x, y):
#     result = await compute1(x, y)
#     print("%s + %s = %s" % (x, y, result))
 
# loop1 = asyncio.get_event_loop()
# print("start")
# # 中断调用，直到协程执行结束

# loop1.run_until_complete(print_sum1(1, 2))
# print("end")
# loop1.close()

# def myFunction():
#     myFunction.__name__ = "test"
#     print('变量 myFunction.__name__ 的值是 ' + myFunction.__name__)

# def main():
#     myFunction()
#     test()

# if __name__ == '__main__':
#     main()

#     asyncio.ensure_future()


"""
    !思路:
        ^利用生产者和消费者的设计模式来设计.
        ^生产者生产下载图片的url
        ^消费者消费下载图片的url
"""
def consumer(): #消费者
    print("[消费者] 开始")
    r = '开始'
    while True:
        n = yield r
        if not n:
            print("n 是空的")
            continue
        print("[消费者] 消费者在消费 %s" % n)
        r = "消费完了,请生产."

url_list = ["http://www.baidu.com"]*5

def Url_Get():
    
    
    for i in range(0,len(url_list)):
        print(f"len(url_list):{len(url_list)}")
        
        print(f"[url_list[{i}]]:",url_list[i])
        yield url_list[i]
        

def Url_Append(url):
    url_list.append(url)

def producer(c): #生产者
    temp = len(url_list)
    print(f"temp:{temp}")
    url1 = Url_Get()
    start_value = c.send(None)
    print(start_value)
    """
        这个生成器创建后不检索,只会在每次执行的时候来进行获取
    """
    Url_Append("http://www.zhihu.com")
    if not temp == len(url_list) :
        ValueError("url_list changed.")
    ValueError("url_list changed.")
    n = len(url_list)
    while ((n) > 0):
        n -= 1
        url2 = url1.send(None)
        if not url2:
            print("url2 None")
            continue
        
        print(f'[生产者] 生产了: {url2}' )
        r = c.send(url2)
        print(f'[生产者] 消费者返回: {r}')


c = consumer()
producer(c)