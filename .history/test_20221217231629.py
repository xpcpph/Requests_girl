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

def consumer():
    print("[CONSUMER] start")
    r = 'start'
    while True:
        n = yield r
        if not n:
            print("n is empty")
            continue
        print("[CONSUMER] Consumer is consuming %s" % n)
        r = "200 ok"
 
 
def producer(c):
    # 启动generator
    start_value = c.send(None)
    print(start_value)
    n = 0
    while n < 3:
        n += 1
        print("[PRODUCER] Producer is producing %d" % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    # 关闭generator
    c.close()
 
 
# 创建生成器
c = consumer()
# 传入generator
producer(c)