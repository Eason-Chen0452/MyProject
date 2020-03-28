# -*- coding: utf-8 -*-

"""
    ProxyFinishing: 只进行爬取网站的ip, 将ip放进队列中, 只放ip的操作 , 为一个进程, 两线程分别爬取
        GetFreeProxy: 调用外部封装的class进行方法的获取 - 可用外部调用
        _pool_x: 两个爬取方法, 用两个线程同时启动爬取, 将得到的ip存放在队列中
        main: 该class的主控函数
    ProxySave: 来用存储爬下来的ip, 将放在队列中的ip取出, 以文本/SSDB/Redis方式存储, 为一个进程
        record_proxy_text: 用txt文件形式存储
        record_proxy_ssdb: 将ip存储在SSDB中
        main: 该class的主控函数
    main: 为控制ProxyFinishing/ProxySave类的主控函数 可独立执行
"""
import sys
sys.path.append('..')

import time
import threading
from multiprocessing import Process, Queue

from ProxyPackage.FreeProxy import CrawlProxy
from ProxyPackage.FreeProxy import ProxyReadyWork as C
from Logger.log import get_logger, get_folder

_logger = get_logger(__name__)
_file_path = get_folder()


class ProxyFinishing(object):

    def __init__(self, queue=False):
        self.queue = queue
        self.main()

    def GetFreeProxy(self):
        request = CrawlProxy()
        c = C()
        return request, c

    def _pool_1(self, queue):
        request, c = self.GetFreeProxy()
        for x in range(1, 5):
            _proxy = eval('request.proxy_%s()' % x)
            _logger.info("Start proxy_%s" % x)
            for proxy in _proxy:
                proxy = proxy.strip()
                if proxy and c.CheckProxy(proxy):
                    if queue.full():  # 队列可能会溢出
                        time.sleep(2)
                    queue.put(proxy)
            _logger.info("Out proxy_%s" % x)

    def _pool_2(self, queue):
        request, c = self.GetFreeProxy()
        for x in range(5, 9):
            _proxy = eval('request.proxy_%s()' % x)
            _logger.info("Start proxy_%s" % x)
            for proxy in _proxy:
                proxy = proxy.strip()
                if proxy and c.CheckProxy(proxy):
                    if queue.full():
                        time.sleep(2)
                    queue.put(proxy)
            _logger.info("Out proxy_%s" % x)

    def main(self):
        _pool_1 = threading.Thread(target=self._pool_1, args=(self.queue, ), name='Pool 1')
        _pool_2 = threading.Thread(target=self._pool_2, args=(self.queue, ), name='Pool 2')
        _pool_1.start()
        _pool_2.start()
        _logger.info("Start _pool_1 and _pool_2")
        _pool_1.join()
        _pool_2.join()
        _logger.info('Out _pool_1 and _pool_2')


class ProxySave(object):

    def __init__(self, queue=False):
        self.queue = queue
        self.main()

    # 写入文本的
    def record_proxy_text(self, queue):
        path = _file_path + "/proxy_pool.txt"
        with open(path, "w+") as file:
            while True:
                value = queue.get(True)
                if value == 'sort':
                    break
                file.write(value + "\n")
            file.close()
        _logger.info('proxy_pool, Text Recorded')

    # 写入SSDB
    def record_proxy_ssdb(self, queue):
        pass

    # 写入Rides
    def record_proxy_redis(self, queue):
        pass

    def main(self):
        _record = threading.Thread(target=self.record_proxy_text, args=(self.queue, ), name='Record Proxy Text')
        # _record = threading.Thread(target=self.record_proxy_ssdb, args=(self.queue, ), name='Record Proxy SSDB')
        # _record = threading.Thread(target=self.record_proxy_redis, args=(self.queue, ), name='Record Proxy SSDB')
        _record.start()
        _logger.info('_record start')
        _record.join()
        _logger.info('_record out')


def main():
    queue = Queue()
    proxy_finishing = Process(target=ProxyFinishing, args=(queue, ), name="Proxy Finishing")
    proxy_save = Process(target=ProxySave, args=(queue, ), name="Proxy Save File or DB")

    proxy_finishing.start()
    _logger.info('proxy_finishing start')
    proxy_save.start()
    _logger.info('proxy_save start')

    proxy_finishing.join()
    _logger.info('proxy_finishing out')
    time.sleep(3)
    queue.put('sort')
    proxy_save.join()
    _logger.info('proxy_save out')


if __name__ == "__main__":
    main()

