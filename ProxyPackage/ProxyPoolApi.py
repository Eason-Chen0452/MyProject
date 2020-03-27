# -*- coding: utf-8 -*-

"""
    ProxyPoolApi: 用来返回可用IP, 所有外部调用, 只是用这个接口


"""

import os
from Logger.log import get_logger

_logger = get_logger(__name__)


class ProxyPool(object):

    def _get_txt_usable(self):
        file_name = os.path.abspath("usable_proxy_pool.txt")
        with open(file_name, "r") as file:
            proxy = file.readline()
            file.close()
        lines = (x for x in open(file_name, "r") if x != proxy)
        with open('text.txt', "w+") as file:
            file.writelines(lines)
            file.close()
        proxy = proxy.replace("\n", "")
        os.remove('usable_proxy_pool.txt')
        os.rename('text.txt', file_name)
        _logger.info("Text form came up with a proxy")
        return proxy

    def Get(self, txt=False, db=False):
        proxy = None
        if txt:
            proxy = self._get_txt_usable()
        elif db:
            pass
        return proxy

    def Delete(self, proxy, db=False):
        pass




