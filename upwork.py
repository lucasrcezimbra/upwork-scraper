import json
import logging
from uuid import uuid4

import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        finally:
            # TODO: keep open when debuging
            self.driver.quit()

    return wrapper


BASE_URL = 'https://www.upwork.com/'


class Page:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get(self):
        self.driver.get(self.url)


class Input:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def fill(self, value):
        element = self.wait.until(EC.presence_of_element_located(self.selector))
        element.send_keys(value)
        element.send_keys(Keys.RETURN)


class UsernameInput(Input):
    selector = (By.NAME, 'login[username]')


class PasswordInput(Input):
    selector = (By.NAME, 'login[password]')


class LoginPage(Page):
    url = BASE_URL + 'ab/account-security/login'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_input = UsernameInput(self.driver, self.wait)
        self.password_input = PasswordInput(self.driver, self.wait)

    def login(self, username, password, secret_answer=None):
        self.get()
        self.username_input.fill(username)
        self.password_input.fill(password)


class HomePage(Page):
    def data(self):
        self.wait.until(EC.title_contains('My Job Feed'))
        return self.driver.execute_script(
            'return window.__INITIAL_STATE__.organizations.activeItem;'
        )

    def userdata(self):
        # TODO: verify if is logged in
        # TODO: verify if is in homepage
        data = self.data()
        return {
            'name': data['label'],
            'title': data['type_title'],
        }


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


@click.command()
@click.argument('username')
@click.argument('password')
@click.argument('secret_answer')
def cli(username, password, secret_answer):
    # TODO: adds headless option
    upwork = Upwork(username)
    upwork.login(password, secret_answer)
    upwork.dump_userdata()


if __name__ == '__main__':
    cli()
