import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class MyTestSuite(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # 禁止图像、声音、Flash 等的加载，加快进度
        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 2,
                'images': 2,
                'flash': 2,
                'plugins': 2,
                'popups': 2,
                'sound': 2,
                'media_stream_mic': 2,
                'media_stream_camera': 2,
                'automatic_downloads': 2,
                'midi_sysex': 2,
            }
        }
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(2)
        self.base_url = 'https://twitter.com/search'
        self.verificationErrors = []
        self.accept_next_alert = True

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
