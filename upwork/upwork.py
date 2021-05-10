import json
import logging
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from upwork.pages import HomePage, LoginPage

# TODO: improve log format
logger = logging.getLogger(__name__)


def driver_except(f):
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            filename = f'{uuid4()}.png'
            logger.critical(f'{e}. Saving screenshot for troubleshooting in {filename}')
            self.driver.save_screenshot(filename)
            raise e
        # finally:
        #     # TODO: keep open when debuging
        #     self.driver.quit()

    return wrapper


class Upwork:
    def __init__(self, username, driver=None, wait=None):
        self.username = username
        self.driver = driver or webdriver.Chrome('./chromedriver')
        self.wait = wait or WebDriverWait(self.driver, 10)
        self.login_page = LoginPage(self.driver, self.wait)
        self.home_page = HomePage(self.driver, self.wait)

    @driver_except
    def login(self, password, secret_answer=None):
        self.login_page.login(self.username, password)

    @driver_except
    def userdata(self):
        return self.home_page.userdata()

    @driver_except
    def dump_userdata(self, path=None):
        path = path or f'{self.username}.json'
        with open(path, 'w') as f:
            json.dump(self.userdata(), f)
