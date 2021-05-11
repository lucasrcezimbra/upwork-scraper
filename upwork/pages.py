from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# TODO: moves to settings
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
    def wait_loading(self):
        self.wait.until(EC.title_contains('My Job Feed'))

    def data(self):
        self.wait_loading()
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
