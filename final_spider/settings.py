# -*- coding: utf-8 -*-

# Scrapy settings for final_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'final_spider'

SPIDER_MODULES = ['final_spider.spiders']
NEWSPIDER_MODULE = 'final_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'final_spider (+http://www.yourdomain.com)'
USER_AGENT_CHOICES = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'final_spider.middlewares.FinalSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'final_spider.middlewares.FinalSpiderSpiderMiddleware': 1,
   # 'final_spider.middlewares.JsPageMiddleware': 2,
   # 'final_spider.middlewares.ProxyMiddleware': 100,
}

PROXIES = [
    {'ip_port': '122.114.31.177:808', 'user_pass': ''},
    {'ip_port': '61.135.217.7:80', 'user_pass': ''},
    {'ip_port': '116.231.63.104:8118', 'user_pass': ''},
    {'ip_port': '112.114.95.236:8118', 'user_pass': ''},
    {'ip_port': '223.241.78.23:808', 'user_pass': ''},
    {'ip_port': '114.252.165.173:8118', 'user_pass': ''},
    {'ip_port': '121.31.148.35:8123', 'user_pass': ''},
    {'ip_port': '116.54.78.3:8118', 'user_pass': ''},
    {'ip_port': '27.10.232.26:8118', 'user_pass': ''},
    {'ip_port': '123.55.3.156:808', 'user_pass': ''},
    {'ip_port': '49.85.5.176:46489', 'user_pass': ''},
    {'ip_port': '121.206.86.91:21317', 'user_pass': ''},
]

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'final_spider.pipelines.FinalSpiderPipeline': 300,
   'final_spider.pipelines.TeamPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = '192.168.1.170'
MYSQL_DBNAME = 'qsr_18118'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'qsr1225'
MYSQL_PORT = 3306

# 输出文件编码格式
FEED_EXPORT_ENCODING = 'utf-8'

# 图片下载路径
IMAGES_STORE = 'F:\\image'
