import json

from selenium.webdriver.common.keys import Keys

from upwork import Upwork
from upwork.pages import (AuthorizationPage, ContactJsonPage, HomePage,
                          LoginPage, PasswordInput, UsernameInput)


def test_init(mocker):
    driver_mock = mocker.MagicMock()
    wait_mock = mocker.MagicMock()

    upwork = Upwork('username', 'password', 'secret_answer', driver=driver_mock, wait=wait_mock)

    assert upwork.username == 'username'
    assert upwork.password == 'password'
    assert upwork.secret_answer == 'secret_answer'
    assert upwork.driver == driver_mock
    assert upwork.wait == wait_mock
    assert isinstance(upwork.login_page, LoginPage)
    assert isinstance(upwork.home_page, HomePage)
    assert isinstance(upwork.contact_json_page, ContactJsonPage)
    assert isinstance(upwork.authorization_page, AuthorizationPage)


def test_headless_by_default(mocker):
    chrome_mock = mocker.patch('upwork.upwork.Chrome')
    options_mock = mocker.patch('upwork.upwork.ChromeOptions').return_value

    Upwork('username', 'password', 'secret_answer')

    options_mock.add_argument.assert_called_with('--headless')
    chrome_mock.assert_called_once_with(options=options_mock)


def test_headless_by_false(mocker):
    mocker.patch('upwork.settings.HEADLESS', False)
    chrome_mock = mocker.patch('upwork.upwork.Chrome')
    options_mock = mocker.patch('upwork.upwork.ChromeOptions').return_value

    Upwork('username', 'password', 'secret_answer')

    options_mock.add_argument.assert_not_called()
    chrome_mock.assert_called_once_with(options=options_mock)


def test_login(mocker):
    username, password = 'username', 'passwd'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    username_element, password_element = mocker.MagicMock(), mocker.MagicMock()
    wait_mock.until.side_effect = [username_element, password_element, None]
    EC_mock = mocker.patch('upwork.pages.EC')

    upwork = Upwork(username, password, 'secret_answer', driver_mock, wait_mock)
    upwork.login()

    driver_mock.get.assert_called_once_with(LoginPage.url)
    assert wait_mock.until.call_count == 3
    EC_mock.presence_of_element_located.call_args_list == [
        mocker.call(UsernameInput.selector),
        mocker.call(PasswordInput.selector),
    ]
    assert username_element.send_keys.call_args_list == [
        mocker.call(username),
        mocker.call(Keys.RETURN)
    ]
    assert password_element.send_keys.call_args_list == [
        mocker.call(password),
        mocker.call(Keys.RETURN)
    ]
    EC_mock.title_contains.assert_called_once_with('My Job Feed')


def test_userdata(mocker):
    name, title = 'Walter White', 'Cooker'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    driver_mock.execute_script.return_value = {
        'id': 'd1000228459',
        'is_active': True,
        'label': name,
        'link': '/signup/home?companyReference=d1000228459',
        'photo_url': 'https://www.upwork.com/profile-portraits/ABC123',
        'type_title': title,
        'uid': '1361618152857010177'
    }

    upwork = Upwork('username', 'password', 'secret_answer', driver_mock, wait_mock)

    assert upwork.userdata() == {
        'name': name,
        'title': title,
    }


def test_dump_userdata(mocker, tmpdir):
    name, title = 'Walter White', 'Cooker'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    driver_mock.execute_script.return_value = {
        'id': 'd1000228459',
        'is_active': True,
        'label': name,
        'link': '/signup/home?companyReference=d1000228459',
        'photo_url': 'https://www.upwork.com/profile-portraits/ABC123',
        'type_title': title,
        'uid': '1361618152857010177'
    }

    filepath = tmpdir.join('username.json')
    upwork = Upwork('username', 'password', 'secret_answer', driver_mock, wait_mock)
    upwork.dump_userdata(filepath)

    with open(filepath) as f:
        assert json.load(f) == {
            'name': name,
            'title': title,
        }


def test_profile(mocker, contact_info_fake):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    upwork = Upwork('username', 'password', 'secret_answer', driver_mock, wait_mock)
    upwork.contact_json_page.rawdata = lambda: json.dumps(contact_info_fake)
    profile = upwork.profile()

    freelancer = contact_info_fake['freelancer']
    address = freelancer['address']
    assert profile.full_name == ' '.join((
        freelancer['firstName'],
        freelancer['lastName'],
    ))
    assert profile.first_name == freelancer['firstName']
    assert profile.last_name == freelancer['lastName']
    assert profile.email == freelancer['email']['address']
    assert profile.phone_number == freelancer['phone']
    assert profile.picture_url == freelancer['portrait']['bigPortrait']
    assert profile.address.line1 == address['street']
    assert profile.address.line2 == address['additionalInfo']
    assert profile.address.city == address['city']
    assert profile.address.state == address['state']
    assert profile.address.postal_code == address['zip']
    assert profile.address.country == address['country']


def test_dump_profile(mocker, tmpdir, contact_info_fake):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    filepath = tmpdir.join('username.json')

    upwork = Upwork('username', 'password', 'secret_answer', driver_mock, wait_mock)
    upwork.contact_json_page.rawdata = lambda: json.dumps(contact_info_fake)
    upwork.dump_profile(filepath)

    with open(filepath) as f:
        assert json.load(f) == upwork.profile().dict()
