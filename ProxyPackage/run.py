# -*- coding: utf-8 -*-

"""
    启动文件 同时启动 SortOutProxy 和 VerificationProxy
"""
import sys
sys.path.append('..')

from time import sleep
from multiprocessing import Process

from ProxyPackage.VerificationProxy import main as verification_proxy
from ProxyPackage.SortOutProxy import main as crawl_agent_proxy
from Logger.log import get_logger

_logger = get_logger(__name__)


def main():
    crawl_agent = Process(target=crawl_agent_proxy, name='Crawl Agent Proxy')
    verification = Process(target=verification_proxy, name='Verification Proxy')
    crawl_agent.start()
    _logger.info('Crawl Agent Proxy Start')
    sleep(10)
    verification.start()
    _logger.info('Verification Proxy Start')
    crawl_agent.join()
    _logger.info('Crawl Agent Proxy Out')
    verification.join()
    _logger.info("Verification Proxy Out")


if __name__ == "__main__":
    main()
