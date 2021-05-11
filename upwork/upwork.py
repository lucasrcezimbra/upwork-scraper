import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from upwork.pages import ContactJsonPage, HomePage, LoginPage
from upwork.troubleshooting import driver_except


class Upwork:
    def __init__(self, username, driver=None, wait=None):
        self.username = username
        self.driver = driver or webdriver.Chrome('./chromedriver')
        self.wait = wait or WebDriverWait(self.driver, 10)
        self.login_page = LoginPage(self.driver, self.wait)
        self.home_page = HomePage(self.driver, self.wait)
        self.contact_json_page = ContactJsonPage(self.driver, self.wait)

    @driver_except
    def login(self, password, secret_answer=None):
        self.login_page.login(self.username, password)
        self.home_page.wait_loading()

    @driver_except
    def userdata(self):
        return self.home_page.userdata()

    @driver_except
    def dump_userdata(self, path=None, indent=4):
        path = path or f'{self.username}.json'
        with open(path, 'w') as f:
            json.dump(self.userdata(), f, indent=indent)

    @driver_except
    def profile(self):
        return self.contact_json_page.profile()

    @driver_except
    def dump_profile(self, path=None, indent=4):
        path = path or f'{self.username}_profile.json'
        with open(path, 'w') as f:
            json.dump(self.profile().dict(), f, indent=indent)
