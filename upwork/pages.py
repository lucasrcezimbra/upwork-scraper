import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from upwork import settings
from upwork.logging import get_logger
from upwork.models import Profile

logger = get_logger(__name__)


class Page:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get(self):
        logger.debug(f'Get page {self.url}')
        self.driver.get(self.url)


class Input:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def fill(self, value):
        logger.debug(f'Waiting presence of {self.selector}')
        element = self.wait.until(EC.presence_of_element_located(self.selector))
        logger.debug(f'Filling in input {self.selector}')
        element.send_keys(value)
        element.send_keys(Keys.RETURN)


class UsernameInput(Input):
    selector = (By.NAME, 'login[username]')


class PasswordInput(Input):
    selector = (By.NAME, 'login[password]')


class SecretAnswerInput(Input):
    selector = (By.NAME, 'deviceAuth[answer]')


class LoginPage(Page):
    url = settings.BASE_URL + 'ab/account-security/login'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_input = UsernameInput(self.driver, self.wait)
        self.password_input = PasswordInput(self.driver, self.wait)

    def login(self, username, password):
        logger.debug('Login: Get login page')
        self.get()
        logger.debug('Login: Filling in username input')
        self.username_input.fill(username)
        logger.debug('Login: Filling in password input')
        self.password_input.fill(password)


class HomePage(Page):
    def wait_loading(self):
        logger.debug('Waiting for home page')
        self.wait.until(EC.title_contains('My Job Feed'))

    def data(self):
        # TODO: verify if is in homepage
        self.wait_loading()
        logger.debug('Get data from homepage')
        return self.driver.execute_script(
            'return window.__INITIAL_STATE__.organizations.activeItem;'
        )

    def userdata(self):
        logger.debug('Get userdata from homepage')
        data = self.data()
        return {
            'name': data['label'],
            'title': data['type_title'],
        }


class ContactJsonPage(Page):
    url = settings.BASE_URL + 'freelancers/settings/api/v1/contactInfo'

    def rawdata(self):
        self.get()
        logger.debug('rawdata from contact info json page')
        return self.driver.find_element_by_xpath('//pre').get_attribute('innerHTML')

    def data(self):
        logger.debug('data from contact info json page')
        return json.loads(self.rawdata())

    def userdata(self):
        data = self.data()
        person = data['freelancer']
        address = person['address']
        logger.debug('userdata from contact info json page')
        return {
            'full_name': ' '.join((person['firstName'], person['lastName'])),
            'first_name': person['firstName'],
            'last_name': person['lastName'],
            'email': person['email']['address'],
            'phone_number': person['phone'],
            'picture_url': person['portrait']['bigPortrait'],
            'address': {
                'line1': address['street'],
                'line2': address['additionalInfo'],
                'city': address['city'],
                'state': address['state'],
                'postal_code': address['zip'],
                'country': address['country'],
            }
        }

    def profile(self):
        logger.debug('profile from contact info json page')
        return Profile(**self.userdata())


class AuthorizationPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_answer_input = SecretAnswerInput(self.driver, self.wait)

    def needs_authorization(self):
        logger.debug(f'Needs secret answer? Page title {self.driver.title}')
        return self.driver.title == 'Device authorization'

    def ensure_authorization(self, secret_answer):
        if self.needs_authorization():
            logger.debug('Needs secret answer authorization. Filling in input')
            self.secret_answer_input.fill(secret_answer)
