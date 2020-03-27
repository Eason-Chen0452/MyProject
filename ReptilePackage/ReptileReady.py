# -*- utf-8: coding -*-

"""
    ReptileReady 作用引入自己自定义的包, 其他文件去引用
        如 引用代理池, 请求头等
        ReptileBrowser: 模拟浏览器爬虫行为
        ReptileConventional: 常规爬虫行为
"""

import sys
sys.path.append('..')

from selenium import webdriver

from ProxyPackage.ProxyPoolApi import ProxyPool
from ProxyPackage.RequestHeader import Header


class Ready(object):

    def __init__(self, path=False):
        self.path = path

    # 返回随机浏览器请求头
    def get_header(self):
        return Header().Get()

    # 返回一个代理
    def get_proxy(self, txt=False, db=False):
        pool = ProxyPool()
        proxy = pool.Get(txt=txt, db=db)
        return proxy

    # 模拟浏览器行为 Google
    def browser_chrome(self, headless=False, user_dir=False):
        opt = None
        if headless:
            opt = webdriver.ChromeOptions()
            opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
            opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
            opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
            opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
            # 设置成用户自己的数据目录
            if user_dir:
                opt.add_argument(r'--user-data-dir=%s' % user_dir)
        chrome_browser = webdriver.Chrome(executable_path=self.path, options=opt)
        return chrome_browser

    # 模拟浏览器行为 火狐
    def browser_firefox(self):
        pass







