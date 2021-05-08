from selenium.webdriver.common.keys import Keys

from upwork import LoginPage, PasswordInput, UsernameInput


def test_init(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = LoginPage(driver_mock, wait_mock)

    assert page.driver == driver_mock
    assert page.wait == wait_mock


def test_url(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = LoginPage(driver_mock, wait_mock)

    assert page.url == 'https://www.upwork.com/ab/account-security/login'


def test_get(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = LoginPage(driver_mock, wait_mock)
    page.get()

    driver_mock.get.assert_called_once_with(page.url)


def test_login(mocker):
    username, password = 'username', 'passwd'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    username_element, password_element = mocker.MagicMock(), mocker.MagicMock()
    wait_mock.until.side_effect = [username_element, password_element]
    EC_mock = mocker.patch('upwork.EC')

    page = LoginPage(driver_mock, wait_mock)
    page.login(username, password)

    driver_mock.get.assert_called_once_with(page.url)
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
