# -*- coding: utf-8 -*-

"""
    通过浏览器查看登入之后的请求头; 绕过登入的验证, 确定特殊路由进行请求
    使用拉钩 boss 猎聘网站
    爬取拉钩招聘信息
"""


import requests, time, pandas as pd
from random import randint
from ReptilePackage.ReptileReady import Ready
from Logger.log import get_logger, get_create_folder

_logger = get_logger(__name__)
_file_path = get_create_folder()


class JobSite(object):

    # post 请求需要的参数
    def _get_post(self):
        data = {
            'first': 'true',
            'pn': 1,
            'kd': 'python',
        }
        return data

    # url get请求 post请求 中 url可能不同, 这看网站的情况
    def _get_url(self):
        url = {
            'get_url': 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=',
            'post_url': 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
        }
        return url

    # header 请求头的处理
    def _get_header(self):
        header = Ready().get_header()
        header.update({
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': None,
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.lagou.com',
            'Origin': "https://www.lagou.com",
            'Referer': "https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=",
        })
        return header

    # proxies 代理
    def _get_proxies(self):
        proxy = Ready().get_proxy(txt=True)
        if proxy:
            proxy = {
                "http": "http://%s" % proxy,
                "https": 'http://%s' % proxy,
            }
        return proxy

    # 存放文件的路径
    def _get_save_file(self, path):
        path = _file_path + path
        return path

    # Session Cookies 发起get请求
    def _get_cookies(self, url, header, proxy):
        url = url.get('get_url')
        request = requests.Session()
        request = request.get(url=url, headers=header, timeout=10, proxies=proxy)
        cookie = request.cookies
        return cookie

    # post 返回的数据 整合处理
    def _process_json(self, data, process=False):
        if not process:
            x_number = data['content']['positionResult']['totalCount']
            return x_number
        data = data['content']['positionResult']['result']
        return data

    # 计算爬取的页数
    def _process_page(self, number):
        page = round(number / 15)
        return 30 if page >= 30 else page

    # 随机休眠时间 - 必要的时候使用这个函数 进行休眠
    def _random_sleep(self):
        number = randint(1, 30)
        _logger.info("Sleep %s" % number)
        time.sleep(number)
        return True

    def _get_columns(self):
        field = [
            '公司全名',
            '公司简称',
            '公司规模',
            '融资阶段',
            '区域',
            '职位名称',
            '工作经验',
            '学历要求',
            '薪资',
            '职位福利',
            '经营范围',
            '职位类型',
            '公司福利',
            '第二职位类型',
            '城市'
        ]
        return field

    # post 请求
    def request_post(self, url, cookie, data, header, proxy):
        try:
            url = url.get('post_url')
            request = requests.post(url=url, cookies=cookie, headers=header, data=data, proxies=proxy)
            print(request.text)
            value = request.json()
            assert value.get('success'), 'Reptiles found!'
            return value
        except Exception as e:
            _logger.warning(e)
            return False
    
    def request_list(self, data):
        post_list = []
        for i in data:
            x = []
            x.append(i['companyFullName'])
            x.append(i['companyShortName'])
            x.append(i['companySize'])
            x.append(i['financeStage'])
            x.append(i['district'])
            x.append(i['positionName'])
            x.append(i['workYear'])
            x.append(i['education'])
            x.append(i['salary'])
            x.append(i['positionAdvantage'])
            x.append(i['industryField'])
            x.append(i['firstType'])
            x.append(i['companyLabelList'])
            x.append(i['secondType'])
            x.append(i['city'])
            post_list.append(x)
        return post_list

    def update_cookie_header_session(self, url, header):
        new_header = Ready().get_header()
        header.update(new_header)
        cookie = self._request_session_cookies(url, header)
        _logger.info('Update Cookie, SessionID, User-Agent')
        return header, cookie

    def Crawling(self):
        pass

    # 主控函数
    def main(self):
        url = self._get_url()
        data = self._get_post()
        path = self._get_save_file('/data.csv')
        header = self._get_header()
        proxy = self._get_proxies()
        cookie = self._get_cookies(url, header, proxy)
        post_json = self.request_post(url, cookie, data, header, proxy)
        number = self._process_json(post_json)
        page = self._process_page(number)
        columns = self._get_columns()
        _logger.info('Total posts %s, Total pages %s' % (number, page))
        self.Crawling()


        info = []
        for x in range(1, page+1):
            data.update({'pn': x})
            if randint(0, 1):
                header, cookie = self.update_cookie_header_session(url, header)
            post_data = self.request_post(url, cookie, data, header)
            if not post_data:
                while True:
                    _logger.info("Reptile found, Reptile found, dormant for one minute")
                    self._get_proxies(aip=True)
                    # time.sleep(30)
                    cookie = self._request_session_cookies(url, header)
                    post_data = self.request_post(url, cookie, data, header)
                    if post_data:
                        _logger.info("End the endless loop")
                        break
            post_data = self._process_json(post_data, process=True)
            post_list = self.request_list(post_data)
            info += post_list
            _logger.info('Number %s page, Accumulate posts %s' % (x, len(info)))
        df = pd.DataFrame(data=info, columns=columns)
        df.to_csv(path, index=False)
        _logger.info("Save")


JobSite().main()

