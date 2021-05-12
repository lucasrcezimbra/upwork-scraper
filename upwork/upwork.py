import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from upwork.pages import (AuthorizationPage, ContactJsonPage, HomePage,
                          LoginPage)
from upwork.troubleshooting import driver_except


class Upwork:
    def __init__(self, username, password, secret_answer, driver=None, wait=None):
        self.username = username
        self.password = password
        self.secret_answer = secret_answer
        self.driver = driver or webdriver.Chrome('./chromedriver')
        self.wait = wait or WebDriverWait(self.driver, 10)
        self.login_page = LoginPage(self.driver, self.wait)
        self.home_page = HomePage(self.driver, self.wait)
        self.contact_json_page = ContactJsonPage(self.driver, self.wait)
        self.authorization_page = AuthorizationPage(self.driver, self.wait)

    @driver_except
    def login(self):
        self.login_page.login(self.username, self.password)
        self.authorization_page.ensure_authorization(self.secret_answer)
        self.home_page.wait_loading()

    @driver_except
    def userdata(self):
        self.authorization_page.ensure_authorization(self.secret_answer)
        return self.home_page.userdata()

    @driver_except
    def dump_userdata(self, path=None, indent=4):
        path = path or f'{self.username}.json'
        with open(path, 'w') as f:
            json.dump(self.userdata(), f, indent=indent)

    @driver_except
    def profile(self):
        self.authorization_page.ensure_authorization(self.secret_answer)
        return self.contact_json_page.profile()

    @driver_except
    def dump_profile(self, path=None, indent=4):
        path = path or f'{self.username}_profile.json'
        with open(path, 'w') as f:
            json.dump(self.profile().dict(), f, indent=indent)
