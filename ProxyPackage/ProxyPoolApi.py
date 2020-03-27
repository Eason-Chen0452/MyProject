# -*- coding: utf-8 -*-

"""
    ProxyPoolApi: 用来返回可用IP, 所有外部调用, 只是用这个接口
"""

import os
from Logger.log import get_logger, get_create_folder

_logger = get_logger(__name__)
_file_path = get_create_folder()


class ProxyPool(object):

    def _get_txt_usable(self):
        path = _file_path + "/usable_proxy_pool.txt"
        new_path = _file_path + "/text.txt"
        with open(path, "r") as file:
            proxy = file.readline()
            file.close()
        lines = (x for x in open(path, "r") if x != proxy)
        with open(new_path, "w+") as file:
            file.writelines(lines)
            file.close()
        proxy = proxy.replace("\n", "")
        os.remove(path)
        os.rename(new_path, path)
        _logger.info("Text form came up with a proxy")
        return proxy

    def Get(self, txt=False, db=False):
        proxy = None
        if txt:
            proxy = self._get_txt_usable()
        elif db:
            pass
        return proxy if proxy else None

    def Delete(self, proxy, db=False):
        pass




