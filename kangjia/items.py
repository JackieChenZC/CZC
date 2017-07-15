# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import hashlib
import logging

import time
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Compose


def extract_word(field):
    if field:
        if isinstance(field, list):
            field = ','.join(field)  # 补丁
        try:
            field_list = field.split('：')
            new_field = field_list[1]
        except:
            logging.info('该字段未知错误：{0}'.format(field))
            new_field = ''
    else:
        new_field = field
    # logging.info('+++++++++++++{0}++++++++++'.format(new_field))
    return new_field


def create_record_id(name):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    m = hashlib.md5()
    m.update(name + current_time)
    record_id = m.hexdigest()
    return record_id


class ShafaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_name = Field()  # APP名字
    cat = Field()  # APP分类
    comments = Field()  # 评论
    control_type = Field()  # 操作方式
    download_link = Field()  # 下载链接
    downloads = Field()  # 下载次数
    introduction = Field()  # app简介
    language = Field()  # 语言
    package_name = Field()  # 包名
    resolution = Field()  # 分辨率
    score = Field()  # 评分
    system = Field()  # 系统版本
    tag = Field()  # 分类标签
    type = Field()  # 类型
    update = Field()  # 更新
    version = Field()  # 版本
    picture = Field()  # App图片
    package_size = Field()  # 包大小
    mark_distribution = Field()  # 评分分布
    mark_count = Field()  # 评分人数

    _in_time = Field()
    _utime = Field()
    _record_id = Field()


class TuDouItem(Item):
    program = Field()  # 节目名称
    program_alias = Field(input_processor=Compose(extract_word))  # 节目别名
    area = Field()  # 地区
    image = Field()  # 封面地址
    presenter = Field()  # 主讲人
    episodes = Field()  # 总集数或更新至
    # episodes_update = Field()  # 更新至
    tag = Field()  # 类型
    year = Field()  # 年代
    play_cnt = Field(input_processor=MapCompose(extract_word))  # 总播放量
    comment_cnt = Field(input_processor=MapCompose(extract_word))  # 评论
    voteup_cnt = Field(input_processor=MapCompose(extract_word))  # 顶
    introduction = Field(input_processor=MapCompose(extract_word))  # 简介
    applicable_age = Field(input_processor=MapCompose(extract_word))  # 适用年龄
    first_broadcast = Field()  # 开播时间
    director = Field()  # 编导
    cast = Field()  # 声优
    producer = Field()  # 电视台

    _in_time = Field()
    _utime = Field()
    _record_id = Field(input_processor=MapCompose(create_record_id))
