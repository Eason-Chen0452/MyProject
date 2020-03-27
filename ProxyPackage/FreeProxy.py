# -*- coding: utf-8 -*-

"""
    ProxyReadyWork: 是爬取网页代理的准备工作
        CheckProxy: 是用来检查爬取下来的格式是否有问题 - 可用外部调用
        GetHtmlTree: 是获取请求回来的结果, 并通过etree返回html树 - 可用外部调用
        _get_web_request: 是在内部进行使用, 相对应的URL发起请求返回请求结果

    CrawlProxy: 用于爬取各个免费代理网站
"""
import sys
sys.path.append('..')

import re
import time
import requests
from requests.models import Response
from lxml import etree

from ProxyPackage.RequestHeader import Header
from Logger.log import get_logger

_logger = get_logger(__name__)


# 代理前期准备工作
class ProxyReadyWork(object):

    # 检查代理格式
    def CheckProxy(self, proxy):
        regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        _proxy = re.findall(regex, proxy)
        return True if len(_proxy) == 1 and _proxy[0] else False

    # 获取html树
    def GetHtmlTree(self, url, header=False):
        if not header:
            header = Header().Get()
            header.update({
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
            })
        time.sleep(1)
        html = self._get_web_request(url, header)
        # _element = etree.HTML(html.text)
        return html

    # 发起请求
    def _get_web_request(self, url, header, retry_time=5, timeout=30, retry_flag=list(), retry_interval=5, *args, **kwargs):
        """
        :param url:
        :param header:
        :param retry_time: 网络出错 重试时间
        :param timeout: 超时
        :param retry_flag: 如果请求内容有 retry_flag 重新来
        :param retry_interval: 重试间隔
        :param args:
        :param kwargs:
        :return: html
        """
        while True:
            try:
                html = requests.get(url, headers=header, timeout=timeout)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html
            except Exception as e:
                _logger.warning(e)
                retry_time -= 1
                if retry_time <= 0:
                    # 多次请求失败
                    resp = Response()
                    resp.status_code = 200
                    return resp
                time.sleep(retry_interval)


# 爬取各个网站免费的代理
class CrawlProxy(object):

    @staticmethod
    def proxy_1():
        urls = [
            'http://www.data5u.com/',
        ]
        request = ProxyReadyWork()
        for url in urls:
            try:
                tree = request.GetHtmlTree(url)
                tree = etree.HTML(tree.text)
                uls = tree.xpath('//ul[@class="l2"]')
                for ul in uls:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
            except Exception as e:
                _logger.warning("proxy_1: %s" % e)

    @staticmethod
    def proxy_2(area=30, page=1):
        """
        代理66 http://www.66ip.cn/
        """
        request = ProxyReadyWork()
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                try:
                    url = "http://www.66ip.cn/areaindex_%s/%s.html" % (area_index, i)
                    tree = request.GetHtmlTree(url)
                    tree = etree.HTML(tree.text)
                    tr_list = tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                    if len(tr_list) == 0:
                        continue
                    for tr in tr_list:
                        yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                except Exception as e:
                    _logger.warning("proxy_2: %s" % e)

    @staticmethod
    def proxy_3(page_count=30):
        """
        西刺代理 http://www.xicidaili.com
        """
        urls = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        request = ProxyReadyWork()
        for url in urls:
            for i in range(1, page_count + 1):
                try:
                    page_url = url + str(i)
                    tree = request.GetHtmlTree(page_url)
                    tree = etree.HTML(tree.text)
                    proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                    for proxy in proxy_list:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                except Exception as e:
                    _logger.warning("proxy_3: %s" % e)

    @staticmethod
    def proxy_4():
        """
        guobanjia http://www.goubanjia.com/
        """
        url = "http://www.goubanjia.com/"
        tree = ProxyReadyWork().GetHtmlTree(url)
        try:
            tree = etree.HTML(tree.text)
            proxy_list = tree.xpath('//td[@class="ip"]')
            # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
            # 需要过滤掉<p style="display:none;">的内容
            xpath_str = """
            .//*[not(contains(@style, 'display: none')) 
            and not(contains(@style, 'display:none'))
            and not(contains(@class, 'port'))]/text()
            """
            for each_proxy in proxy_list:
                _ip = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '%s:%s' % (_ip, port)
        except Exception as e:
            _logger.warning("proxy_4: %s" % e)

    @staticmethod
    def proxy_5():
        """
        快代理 https://www.kuaidaili.com
        """
        urls = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in urls:
            for page in range(1, 30):
                try:
                    page_url = url.format(page=page)
                    tree = ProxyReadyWork().GetHtmlTree(page_url)
                    tree = etree.HTML(tree.text)
                    proxy_list = tree.xpath('.//table//tr')
                    for tr in proxy_list[1:]:
                        yield ':'.join(tr.xpath('./td/text()')[0:2])
                except Exception as e:
                    _logger.warning("proxy_5: %s" % e)

    @staticmethod
    def proxy_6():
        """
        云代理 http://www.ip3366.net/free/
        """
        request = ProxyReadyWork()
        urls = [
            'http://www.ip3366.net/?stype=1&page=%s',
            'http://www.ip3366.net/?stype=2&page=%s'
        ]
        for url in urls:
            for x in range(1, 11):
                try:
                    # url = 'http://www.ip3366.net/?stype=1&page=%s' % x
                    tree = request.GetHtmlTree(url % x)
                    proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', tree.text)
                    for proxy in proxies:
                        yield ":".join(proxy)
                except Exception as e:
                    _logger.warning("proxy_6: %s" % e)

    @staticmethod
    def proxy_7(page_count=10):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        """
        request = ProxyReadyWork()
        for i in range(1, page_count + 1):
            try:
                url = 'http://ip.jiangxianli.com/?page=%s' % i
                tree = request.GetHtmlTree(url)
                tree = etree.HTML(tree.text)
                tr_list = tree.xpath(".//table/tbody/tr")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
            except Exception as e:
                _logger.warning("proxy_7: %s" % e)

    @staticmethod
    def proxy_8():
        request = ProxyReadyWork()
        for x in range(1, 7):
            try:
                url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % x
                tree = request.GetHtmlTree(url)
                proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', tree.text)
                for proxy in proxies:
                    yield ':'.join(proxy)
            except Exception as e:
                _logger.warning("proxy_8: %s" % e)

    # # 暂时不可用
    # @staticmethod
    # def proxy_7():
    #     """
    #     IP海 http://www.iphai.com/free/ng
    #     """
    #     urls = [
    #         'http://www.iphai.com/free/ng',
    #         'http://www.iphai.com/free/np',
    #         'http://www.iphai.com/free/wg',
    #         'http://www.iphai.com/free/wp'
    #     ]
    #     request = ProxyReadyWork()
    #     for url in urls:
    #         tree = request.GetHtmlTree(url)
    #         proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
    #                              tree.text)
    #         for proxy in proxies:
    #             yield ":".join(proxy)
    #
    # # 暂时不可用 翻墙使用
    # @staticmethod
    # def proxy_9():
    #     """
    #     墙外网站 cn-proxy
    #     """
    #     urls = ['https://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = ProxyReadyWork()
    #     for url in urls:
    #         tree = request.GetHtmlTree(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', tree.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)
    #
    # # 暂时不可用 翻墙使用
    # @staticmethod
    # def proxy_10():
    #     import base64
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = ProxyReadyWork()
    #     for url in urls:
    #         r = request.GetHtmlTree(url)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()
