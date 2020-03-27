# -*- coding: utf-8 -*-


from ReptilePackage.ProxyPackage.VerificationProxy import Verification
from ReptilePackage.ProxyPackage import SortOutProxy
from multiprocessing import Process


def main():
    sort_out = Process(target='', name='Sort Out Proxy')
    # sort_out = Process(target='', name='Sort Out Proxy')

    sort_out.start()
    sort_out.join()



