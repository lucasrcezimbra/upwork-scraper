import json

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

from upwork import settings
from upwork.logging import get_logger
from upwork.pages import (AuthorizationPage, ContactJsonPage, HomePage,
                          LoginPage)
from upwork.troubleshooting import driver_except

logger = get_logger(__name__)


class Upwork:
    def __init__(self, username, password, secret_answer, driver=None, wait=None):
        self.username = username
        self.password = password
        self.secret_answer = secret_answer
        options = ChromeOptions()
        if settings.HEADLESS:
            options.add_argument("--headless")
        self.driver = driver or Chrome(options=options)
        self.wait = wait or WebDriverWait(self.driver, settings.WAIT_TIMEOUT)
        self.login_page = LoginPage(self.driver, self.wait)
        self.home_page = HomePage(self.driver, self.wait)
        self.contact_json_page = ContactJsonPage(self.driver, self.wait)
        self.authorization_page = AuthorizationPage(self.driver, self.wait)

    @driver_except
    def login(self):
        logger.info('Starting login')
        self.login_page.login(self.username, self.password)
        logger.info('Verifying if needs secret answer')
        self.authorization_page.ensure_authorization(self.secret_answer)
        logger.info('Waiting to be redirect to home')
        self.home_page.wait_loading()

    @driver_except
    def userdata(self):
        logger.info('Verifying if needs secret answer')
        self.authorization_page.ensure_authorization(self.secret_answer)
        logger.info('Getting userdata from home page')
        return self.home_page.userdata()

    @driver_except
    def dump_userdata(self, path=None, indent=4):
        path = path or f'{self.username}.json'
        with open(path, 'w') as f:
            logger.info(f'Saving userdata in {path}')
            json.dump(self.userdata(), f, indent=indent)

    @driver_except
    def profile(self):
        logger.info('Verifying if needs secret answer')
        self.authorization_page.ensure_authorization(self.secret_answer)
        logger.info('Getting profile data')
        return self.contact_json_page.profile()

    @driver_except
    def dump_profile(self, path=None, indent=4):
        path = path or f'{self.username}_profile.json'
        with open(path, 'w') as f:
            logger.info(f'Saving profile data in {path}')
            json.dump(self.profile().dict(), f, indent=indent)
