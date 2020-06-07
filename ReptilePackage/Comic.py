# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import requests, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from random import randint
from lxml import etree

from ReptilePackage.ReptileReady import Ready
from Logger.log import get_logger, get_folder

_logger = get_logger(__name__)
_file_path = get_folder()


class ComicImage(object):

    def _get_sleep_time(self):
        return randint(1, 3)

    def _get_header(self):
        return Ready().get_header()

    def _get_url_path(self):
        url = 'https://40ta.com/home/book/chapter_list/id/14489'
        path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        return url, path

    def _check(self, browser):
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="showcontentitem1"]/img[1]')))
        except Exception as e:
            _logger.warning(e)
            sleep(self._get_sleep_time())
        return browser

    def check(self, browser):
        path = '//*[@id="chapter_list_panel"]/ul/li[1]/div/div[2]/div'
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, path)))
        except Exception as e:
            _logger.warning(e)
            sleep(self._get_sleep_time())
        return browser

    def first(self):
        url, path = self._get_url_path()
        browser = Ready(path).browser_chrome(headless=False)
        browser.maximize_window()
        browser.get(url)
        browser = self.check(browser)
        tree = etree.HTML(browser.page_source)
        page = tree.xpath('/html/body/div/div/ul/li[3]/div/select/option')
        return len(page), browser

    def create_file(self, browser):
        x_tree = etree.HTML(browser.page_source)
        value = x_tree.xpath('//*[@id="showcontentitem1"]/img[1]')[0].attrib.get('src')
        value = value[:value.index('.jpg')-1] + '%s.jpg'
        name = x_tree.xpath('//*[@id="content_bar"]/h1')[0].text
        if "?" in name:
            name = name[:name.index('?')]
        file_path = 'D:/Comic/%s' % name
        print(name)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        return browser, value, file_path

    def second(self, page, browser):
        header = self._get_header()
        browser.find_element_by_xpath('/html/body/div/div/ul/li[4]/div').click()
        sleep(5)
        browser.find_element_by_xpath('/html/body/div/div/ul/li[4]/div').click()
        sleep(5)
        path = '//*[@id="chapter_list_panel"]/ul/li[3]/div/div[2]/div'
        browser.find_element_by_xpath(path).click()
        while True:
            browser = self._check(browser)
            browser, value, file_path = self.create_file(browser)
            number = 1
            while True:
                url = value % number
                request = requests.get(headers=header, url=url)
                if request.status_code != 200:
                    break
                img_path = file_path + '/' + str(number) + '.jpg'
                with open(img_path, "ab") as img:
                    img.write(request.content)
                img.close()
                number += 1
            browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/div').click()

    def main(self):
        page, browser = self.first()
        self.second(page, browser)


if __name__ == "__main__":
    ComicImage().main()


from PIL import Image
import os


def rea():
    path = 'D:\Comic\Integration'
    if not os.path.exists(path):
        os.mkdir(path)
    path = path[:path.index('\Integration')]
    file_path = os.listdir(path)
    file_path.remove('Integration')
    for x, y in enumerate(file_path):
        y_path = path + '/' + y
        number, new_list, image = 1, [], None
        while True:
            x_path = y_path + '/' + str(number) + '.jpg'
            if number == 1:
                image = Image.open(x_path).convert('RGB')
            elif not os.path.exists(x_path):
                break
            else:
                img = Image.open(x_path).convert('RGB')
                new_list.append(img)
            number += 1
        image.save('D:\Comic\Integration\%s.pdf' % y, "PDF", resolution=100.0, save_all=True, append_images=new_list)
        print(y)


rea()
