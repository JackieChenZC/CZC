# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import logging
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Identity


def extract_word(field):
    if field:
        try:
            new_field = field.split('：')[1]
        except:
            logging.info('该字段未知错误：{0}'.format(field))
            new_field = ''
    else:
        new_field = ''
    logging.info('+++++++++++++{0}++++++++++'.format(new_field))
    return new_field


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
    program_alias = Field(input_processor=MapCompose(extract_word))  # 节目别名
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

    _in_time = Field()
    _utime = Field()
    _record_id = Field()

