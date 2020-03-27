# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ReptilePackage.ReptileReady import ReptileBrowser


def get_request(url, browser):
    browser.get(url)
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'glow-toaster-title')))
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'asMSIF')))
    except Exception as e:
        time.sleep(5)
    return browser


def close_window(browser):
    try:
        browser.find_element_by_xpath('//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div/div[1]/table/tbody/tr/td[2]/div[3]/div[3]/div[2]/div/a').click()
    except Exception as e:
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div/div[1]/table/tbody/tr/td[2]/div[3]/div[3]/div[2]/div/a').click()
    return browser


def first_click(browser, no_first=False, g_check=False):
    if no_first is False:
        xpath = '//*[@id="ddVehicle"]/div[2]/table/tbody/tr[2]/td[2]/div/div/div'
    else:
        xpath = '//*[@id="ddVehicle"]/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/div[1]'
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'ddVehicle')))
        WebDriverWait(browser, 5).until(EC.visibility_of_any_elements_located((By.XPATH, xpath)))
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'ddYearStripe')))
    except Exception as e:
        time.sleep(2)
    if g_check is False:
        browser.find_element_by_xpath('//*[@id="ddVehicle"]').click()
        browser.find_element_by_xpath(xpath).click()
    else:
        browser.find_element_by_xpath('//*[@id="ddYearStripe"]').click()
    return browser


def reptile_amazon(url, browser):
    browser = get_request(url, browser)
    browser = close_window(browser)
    browser = first_click(browser)
    year_ul, year_li, make_ul, make_li, model_ul, model_li = 1, 2, 2, 4, 1, 1
    check, s_check, t_check, g_check = False, False, False, False
    while True:
        print(year_ul, year_li, make_ul, make_li, model_ul, model_li)
        year_ul, year_li, f_check = first(browser, year_ul, year_li, check, s_check, g_check)
        if f_check:
            break
        if g_check:
            g_check = False
        make_ul, make_li, s_check = second(browser, make_ul, make_li, t_check)
        if s_check:
            continue
        model_ul, model_li, t_check = third(browser, model_ul, model_li)
        if t_check:
            g_check = True
            continue
        browser = fourth(browser)
        if not check:
            check = True
        text = browser.find_element_by_xpath('//*[@id="asTitle"]').text
        if text != "This fits your:":
            print('on')
            continue
        text = browser.find_element_by_xpath('//*[@id="asAdditionalFitmentInfoEntry"]/div/div').text
        with open('Amazon.txt', 'a+') as file:
            file.write(text + "\n\n\n")
        print('ok')


def first_check(browser, year_ul, year_li):
    xpath = '//*[@id="ddYearStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/ul[%s]/li[%s]' % (year_ul, year_li)
    try:
        WebDriverWait(browser, 5).until(EC.visibility_of_any_elements_located((By.XPATH, xpath)))
    except Exception as e:
        time.sleep(2)
    browser.find_element_by_xpath(xpath)


def first(browser, year_ul, year_li, check, s_check, g_check):
    f_check, again = False, False
    if check and not g_check:
        first_click(browser, no_first=True)
    if s_check:
        year_li += 1
    try:
        first_check(browser, year_ul, year_li)
    except Exception as e:
        year_ul += 1
        year_li = 2
        again = True
    if again:
        try:
            first_check(browser, year_ul, year_li)
        except Exception as e:  # 到这里还报错 说明 遍历结束 ul 已经超出了
            f_check = True
    if not f_check:
        if g_check:
            first_click(browser, no_first=True, g_check=g_check)
        xpath = '//*[@id="ddYearStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/ul[%s]/li[%s]' % (year_ul, year_li)
        browser.find_element_by_xpath(xpath).click()
    return year_ul, year_li, f_check


def second_check(browser, make_ul, make_li):
    xpath = '//*[@id="ddMakeStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/ul[%s]/li[%s]' % (make_ul, make_li)
    try:
        WebDriverWait(browser, 5).until(EC.visibility_of_any_elements_located((By.XPATH, xpath)))
    except Exception as e:
        time.sleep(2)
    browser.find_element_by_xpath(xpath)


def second(browser, make_ul, make_li, t_check):
    check, again = False, False
    if t_check:
        make_li += 1
    try:
        second_check(browser, make_ul, make_li)
    except Exception as e:
        make_ul += 1
        make_li = 1
        again = True
    if again:
        try:
            second_check(browser, make_ul, make_li)
        except Exception as e:
            make_ul = 1
            make_li = 1
            check = True
    if not check:
        xpath = '//*[@id="ddMakeStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/ul[%s]/li[%s]' % (make_ul, make_li)
        browser.find_element_by_xpath(xpath).click()
    return make_ul, make_li, check


def third_check(browser, model_ul, model_li):
    xpath = '//*[@id="ddModelStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/ul[%s]/li[%s]' % (model_ul, model_li)
    try:
        WebDriverWait(browser, 5).until(EC.visibility_of_any_elements_located((By.XPATH, xpath)))
    except Exception as e:
        time.sleep(2)
    value = browser.find_element_by_xpath(xpath).text
    return True if not value else False


def third(browser, model_ul, model_li):
    check, again, value = False, False, False
    try:
        value = third_check(browser, model_ul, model_li)
        if value:
            model_ul += 1
            model_li = 1
    except Exception as e:
        model_ul += 1
        model_li = 1
        again = True
    if again:
        try:
            third_check(browser, model_ul, model_li)
        except Exception as e:
            model_ul = 1
            model_li = 1
            check = True
    if not check and not value:
        xpath = '//*[@id="ddModelStripe"]/div[2]/table/tbody/tr[2]/td[2]/div/ul[%s]/li[%s]' % (model_ul, model_li)
        browser.find_element_by_xpath(xpath).click()
        # browser.execute_script('arguments[0].click();', click)
        model_li += 1
    return model_ul, model_li, check


def fourth(browser):
    browser.find_element_by_xpath('//*[@id="ddSubmit"]').click()
    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="ddVehicle"]/div[1]/div[2]/div')))
    except Exception as e:
        time.sleep(5)
    return browser


def get_url_path():
    # 爬取的链接
    url = "https://www.amazon.com/Denso-234-4621-Oxygen-Sensor/dp/B000C5YCUM/ref=au_as_r?_encoding=UTF8&Make=Honda%7C59&Model=Accord%7C751&Year=1998%7C1998&ie=UTF8&n=15684181&newVehicle=1&s=automotive&vehicleId=95&vehicleType=automotive"
    # 模拟浏览器行为的路径
    path = r'C:\Users\Administrator\Desktop\chromedriver_win32\chromedriver.exe'
    return url, path


def main():
    url, path = get_url_path()
    browser = ReptileBrowser(path).chrome()
    browser.maximize_window()  # 将浏览器最大化显示
    # browser.set_window_size(480, 800)  # 设置浏览器窗口大小
    reptile_amazon(url, browser)
    browser.close()


if __name__ == "__main__":
    main()

