# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class StoPipeline:
#     def process_item(self, item, spider):
#         return item

import scrapy
# ImagesPipeline 为系统中下载图片的管道
from scrapy.pipelines.images import ImagesPipeline
#
# class ZhanzhangPipeline(object):
#     def process_item(self, item, spider):
#         return item

# 这个类的意思是，继承里系统中下载图片的功能
class StoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['secondary_url'][0],meta={'item':item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 设置图片的路径为  类型名称/url地址
        # 这是一个图片的url: http://pics.sc.chinaz.com/Files/pic/icons128/7065/z1.png
        # 这句代码的意思是先取出图片的url，[0]表示从列表转成字符串
        # split分割再取最后一个值，这样写是让图片名字看起来更好看一点
        image_name = item['secondary_url'][0].split('/')[-1]
        print(image_name)
        # 这样写是保存在一个文件夹里面，注意最后是以'.jpg' 结尾
        # path = item['title'] + image_name
        # 这样写是保存在不同的文件夹中，根据title来为文件夹命名，路径下是图片的名字，还是以.jpg结尾的
        path = '%s' % (image_name)
        return path
