# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BifenSpider(scrapy.Spider):
    name = 'ip_filefab'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com']

    def parse(self, response):
        browser = webdriver.Chrome()
        try:
            browser.get('https://www.baidu.com')
            kw = browser.find_element_by_id('kw')
            kw.send_keys('python3')
            kw.send_keys(Keys.ENTER)
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
            print(kw)
        finally:
            browser.close()

