import json

from selenium.webdriver.common.keys import Keys

from upwork import Upwork
from upwork.pages import HomePage, LoginPage, PasswordInput, UsernameInput


def test_init(mocker):
    driver_mock = mocker.MagicMock()
    wait_mock = mocker.MagicMock()

    upwork = Upwork('username', driver=driver_mock, wait=wait_mock)

    assert upwork.driver == driver_mock
    assert upwork.wait == wait_mock
    assert isinstance(upwork.login_page, LoginPage)
    assert isinstance(upwork.home_page, HomePage)


def test_login(mocker):
    username, password = 'username', 'passwd'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    username_element, password_element = mocker.MagicMock(), mocker.MagicMock()
    wait_mock.until.side_effect = [username_element, password_element]
    EC_mock = mocker.patch('upwork.pages.EC')

    upwork = Upwork(username, driver_mock, wait_mock)
    upwork.login(password)

    driver_mock.get.assert_called_once_with(LoginPage.url)
    assert wait_mock.until.call_count == 2
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

    upwork = Upwork('username', driver_mock, wait_mock)

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
    upwork = Upwork('username', driver_mock, wait_mock)
    upwork.dump_userdata(filepath)

    with open(filepath) as f:
        assert json.load(f) == {
            'name': name,
            'title': title,
        }
