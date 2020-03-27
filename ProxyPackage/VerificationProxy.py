# -*- coding: utf-8 -*-

"""
    Verification: 验证爬来下的ip是否可用, 取出文本/SSDB/Redis 中的ip进行分布验证, 为1个进程, 6个进行验证的线程, 1个进行取出的线程
        _check_proxy: 将传入的proxy值进行验证, 通过bool值返回
        verify_ip: 验证方法, 同时启动四个线程来使用, 加快验证的时间
        get_txt_ip: 将ip从文本中一个一个拿出来
        main: 为该class的主控函数
    UsableIP:
"""

import requests, threading, time
from multiprocessing import Queue, Process
from Logger.log import get_logger

_logger = get_logger(__name__)


class Verification(object):

    def __init__(self, queue_a, queue_b):
        self.queue_a = queue_a
        self.queue_b = queue_b
        self.check = False
        self.main()

    # 调用 检查ip可不可用
    def _check_proxy(self, proxy):
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        proxies = {"http": "http://%s" % proxy}
        try:
            request = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
            if request.status_code == 200:
                _logger.info('%s is ok' % proxy)
                return True
        except Exception as e:
            _logger.warning(e)
            return False

    # 将文本的ip拿出来
    def get_txt_ip(self, queue_a):
        file_name = "proxy_pool.txt"
        with open(file_name, 'r') as file:
            while True:
                _proxy = file.readline()
                if not _proxy:
                    break
                _proxy = _proxy.replace("\n", "")
                if queue_a.full():
                    time.sleep(10)  # 验证是很漫长 应对请求的10s中
                queue_a.put(_proxy)
            file.close()
        _logger.info("%s file read finished" % file_name)

    # 验证IP 通用接口 文本/SSDB/Redis
    def verify_ip(self, queue_a, queue_b):
        while True:
            _proxy = queue_a.get(True)
            if self._check_proxy(_proxy):
                queue_b.put(_proxy)
            if self.check:
                break

    def main(self):
        verify_list = []
        for x in range(6):
            _verify = threading.Thread(target=self.verify_ip, args=(self.queue_a, self.queue_b), name="Verify %s" % x)
            verify_list.append(_verify)
        for x in verify_list:
            x.start()
        _logger.info("All Verification Thread Started")
        get_ip = threading.Thread(target=self.get_txt_ip, args=(self.queue_a, ), name='Get Txt IP')
        get_ip.start()
        _logger.info("Get IP Thread Started")
        get_ip.join()
        _logger.info("Get IP Thread Out")
        while True:
            if self.queue_a.empty():
                self.check = True
                break
        for x in verify_list:
            x.join()
        _logger.info("All Verification Thread Out")


class UsableIP(object):

    def __init__(self, queue):
        self.queue = queue
        self.main()

    # 取出队列值
    def _get_queue(self, queue):
        _proxy = queue.get(True)
        if _proxy == 'sort':
            _proxy = False
        return _proxy

    # 将队列的值放进指定文本/库中
    def save_usable_IP(self, queue):
        file_name = "usable_proxy_pool.txt"
        with open(file_name, "a+") as file:
            while True:
                _proxy = self._get_queue(queue)
                if not _proxy:
                    break
                file.write(str(_proxy) + "\n")
            file.close()
        _logger.info("usable_proxy_pool.txt close")

    def main(self):
        save_ip = threading.Thread(target=self.save_usable_IP, args=(self.queue, ), name="Save Usable IP")
        save_ip.start()
        _logger.info("Usable IP Thread Started")
        save_ip.join()
        _logger.info("Usable IP Thread Out")


def main():
    queue_a = Queue()
    queue_b = Queue()
    verify = Process(target=Verification, args=(queue_a, queue_b), name='Verification Proxy')
    usable = Process(target=UsableIP, args=(queue_b, ), name='Usable IP')
    verify.start()
    usable.start()
    _logger.info('Verification Proxy and Usable IP Start')

    verify.join()
    queue_b.put("sort")
    usable.join()
    _logger.info('Verification Proxy and Usable IP Out')


if __name__ == '__main__':
    main()

