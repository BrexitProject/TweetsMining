import os
import tkinter.messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from TestSuite import MyTestSuite

leap_year_date = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
non_leap_year_date = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def next_month(month):
    if month[-2:] == '12':
        return str(int(month[:4]) + 1).zfill(4) + '01'
    else:
        return month[:4] + str(int(month[-2:]) + 1).zfill(2)


def make_url(tag, month):
    url = 'https://twitter.com/search?l=en&q=' + tag.replace('#', '%23') + '%20'
    yy = int(month[:4])  # 年
    mm = int(month[-2:])  # 月
    date = 'since%3A' + str(yy).zfill(4) + '-' + str(mm).zfill(2) + '-01' + '%20' + 'until%3A' + str(yy).zfill(
        4) + '-' + str(mm).zfill(2) + '-'
    if is_leap_year(yy):
        date += str(leap_year_date[mm]).zfill(2)
    else:
        date += str(non_leap_year_date[mm]).zfill(2)
    url = url + date + '&src=typd'
    print(url)
    return url


def load_hashtag(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip().split()


class View(MyTestSuite):
    hashtag = []
    # 存储文件夹
    folder = 'crawl'
    # 起始月份 与 结束月份，6 位字符串形式
    start = '201901'
    stop = '201905'

    def test_view(self):
        # 读 hashtag
        self.hashtag = load_hashtag('tag')
        # 创建存储文件夹
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # 设置浏览器驱动
        driver = self.driver

        for e in self.hashtag:
            if not os.path.exists(os.path.join(self.folder, e)):
                os.makedirs(os.path.join(self.folder, e))
            cur_month = self.start
            while True:
                driver.get(make_url(e, cur_month))
                # 滚动到最底下
                if self.is_element_present(By.CLASS_NAME, 'stream-footer'):
                    target = driver.find_element_by_class_name('stream-footer')
                    location_y = 0
                    same_cnt = 0
                    while True:
                        driver.execute_script('arguments[0].scrollIntoView();', target)
                        if same_cnt > 800:
                            break
                        if target.location['y'] == location_y:
                            same_cnt += 1
                        else:
                            location_y = target.location['y']
                            same_cnt = 0
                # 对话库，点击确认后才会保存 html
                tkinter.messagebox.showinfo('提示', '确认网页加载完成？')
                # 写文件
                with open(os.path.join(self.folder, e, cur_month), 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                # 下个月
                cur_month = next_month(cur_month)
                if cur_month > self.stop:
                    break


if __name__ == '__main__':
    unittest.main()
