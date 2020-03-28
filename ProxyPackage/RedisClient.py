# -*- coding: utf-8 -*-

"""
    采用Redis 哈希表 进行存储
"""

import redis


class RedisClient(object):

    def __init__(self, host, port, table=None, db=0):
        self.table = table
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.conn = redis.Redis(connection_pool=pool)
        assert self.conn.ping(), '%s: %s, Connection Failed'

    def main(self):
        a = 1
        pass


RedisClient("127.0.0.1", 6379, 'proxy_pool').main()






