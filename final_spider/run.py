# -*- coding: utf-8 -*-
# @Author : dio
"""
爬虫执行顺序（初始执行顺序）
league_country
league
season_type
season_sub_type
team
sportsman
sportsman_relation
# relation
season
score
yazhi
ouzhi
zhenx
jishu
event

（实时爬虫顺序）
team_real
sportsman_real
sportsman_relation_real
season_real
score_real
yazhi_real
ouzhi_real
zhenx_real
jishu_real
bifen

竞彩网彩票信息
lottery
"""
from scrapy import cmdline
name = 'zhenx_real'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())