# -*- coding: utf-8 -*-

"""
    将Execl表格 或 数据库 中的数据进行抽取清洗 分析 进行可视化
"""

import sys
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt
import jieba
import statsmodels.api as sm
from scipy.misc import imread
from wordcloud import WordCloud
from imageio import imread
from pylab import mpl

from Logger.log import get_logger, get_folder

_logger = get_logger(__name__)
_path = get_folder()


class Visualization(object):

    def _get_path(self):
        path = _path + '/data.csv'
        return path

    # 表格时调用
    def _read_data(self, path):
        file_data = pd.read_csv(path, encoding='utf-8')
        return file_data

    # 数据库时调用
    def _read_db_data(self):
        pass

    # 整理数据
    def sort_data(self, data):
        data = self._filter_data(data)
        return True

    # 过滤一些 不要的数据
    def _filter_data(self, data):
        data.drop(data[data['工作经验'].str.contaions('5-10年')].index, inplace=True)
        return data

    def a(self, data):
        re = self._regular_expression()
        data['工作年限'] = data['工作经验'].str.findall(re)

        pass

    def _regular_expression(self):
        re = ""
        return re

    # 主控函数
    def main(self):
        path = self._get_path()
        data = self._read_data(path)
        data = self.sort_data(data)
        pass


Visualization().main()
