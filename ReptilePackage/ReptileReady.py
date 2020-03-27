# -*- utf-8: coding -*-

"""
    ReptileBrowser: 模拟浏览器爬虫行为
    ReptileConventional: 常规爬虫行为
"""

from selenium import webdriver


class ReptileBrowser(object):

    def __init__(self, path):
        self.path = path

    # 使用Google时
    def chrome(self, headless=False, user_dir=False):
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

    # 使用火狐时
    def firefox(self):
        pass


class ReptileConventional(object):
    b = 1
    pass


