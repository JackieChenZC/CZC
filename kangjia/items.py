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
from w3lib.html import remove_tags


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
    # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    current_time = time.time()
    m = hashlib.md5()
    m.update('{name}{time}'.format(name=name, time=current_time))
    record_id = m.hexdigest()
    return record_id


def jiwu_update_date(date):
    if date:
        new_date = date[0].replace(u"'", u'').replace(u'-', u'年').replace(u'：', u'')
        return new_date


# 去除空格、换行符
def remove_blank(content):
    if content:
        if isinstance(content, list):
            content = ','.join(content)  # 补丁
        new_content = content.replace(u'\n', u'').replace(u' ', u'')
    else:
        new_content = content
    return new_content


def baidu_publish_time(content):
    if isinstance(content, list):
        content = ','.join(content)
    if not content:
        publish_time = content.split(' ')[-1]
        date = time.strftime("%Y-%m-%d ", time.localtime())
        new_time = date + publish_time
    else:
        new_time = content
    return new_time


def weather_date(date):
    if date:
        if isinstance(date, list):
            date = date[0]
        year = unicode(time.localtime().tm_year)
        if year not in date:
            new_date = year + date
        else:
            new_date = date
    else:
        new_date = date
    return new_date


def extract_place_name(place_name):
    if place_name:
        place_name = place_name[0].replace(u"pm2.5", u"").replace(u"明日", u"").replace(u"天气预报", u"")
    return place_name


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


class JiwuHousePriceItem(Item):
    province = Field()  # 省份
    city = Field()  # 行政市
    region = Field()  # 区（如南山、福田），该字段为空表示全市价格
    new_house_price = Field()  # 新房价格
    second_house_price = Field()  # 二手房价格
    update_date = Field(input_processor=Compose(jiwu_update_date))  # 更新时间

    _in_time = Field()
    _utime = Field()
    _record_id = Field(input_processor=MapCompose(create_record_id))


class WeatherItem(Item):
    region = Field(input_processor=Compose(extract_place_name))  # 区域
    city = Field(input_processor=Compose(extract_place_name))  # 城市
    province = Field(input_processor=Compose(extract_place_name))  # 省份
    city.items()
    date = Field(input_processor=Compose(weather_date))  # 日期
    high_temp = Field()  # 最高气温
    low_temp = Field()  # 最低气温
    weather = Field()  # 天气
    wind = Field()  # 风向风力
    aqi = Field()  # 空气质量指数
    quality = Field()  # 空气质量

    _in_time = Field()
    _utime = Field()
    _record_id = Field(input_processor=MapCompose(create_record_id))


class IqiyiTVplayItem(Item):
    title = Field()  # 名称
    score = Field(input_processor=MapCompose(remove_tags, remove_blank))  # 评分
    votetop = Field()  # 顶
    votedown = Field()  # 踩
    new_title = Field(input_processor=MapCompose(extract_word))  # 别名
    status = Field(input_processor=MapCompose(extract_word))  # 总集数或更新集情况
    update_time = Field(input_processor=MapCompose(extract_word, remove_blank))  # 更新时间
    pub_year = Field(input_processor=MapCompose(extract_word))  # 上映时间
    type = Field()  # 类型
    area = Field()  # 地区remove_blank
    director = Field()  # 导演
    actor = Field()  # 演员
    summary = Field(input_processor=Compose(remove_blank))  # 简介
    video_type = Field()  # 播放渠道
    detail_url = Field()  # 详细地址
    video_id = Field()  # 电影ID

    _in_time = Field()
    _utime = Field()
    _record_id = Field(input_processor=MapCompose(create_record_id))


class BaiduNewsItem(Item):
    title = Field()  # 新闻标题
    url = Field()  # 新闻链接
    publish_time = Field(input_processor=Compose(baidu_publish_time))  # 新闻发布时间

    _in_time = Field()
    _utime = Field()
    _record_id = Field(input_processor=MapCompose(create_record_id))
