from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from upwork import PasswordInput


def test_init(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    input = PasswordInput(driver_mock, wait_mock)

    assert input.driver == driver_mock
    assert input.wait == wait_mock


def test_selector(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    input = PasswordInput(driver_mock, wait_mock)

    assert input.selector == (By.NAME, 'login[password]')


def test_fill(mocker):
    password = 'password'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    element_mock = mocker.MagicMock()
    wait_mock.until.return_value = element_mock
    EC_mock = mocker.patch('upwork.EC')

    input = PasswordInput(driver_mock, wait_mock)
    input.fill(password)

    wait_mock.until.assert_called_once()
    EC_mock.presence_of_element_located.assert_called_once_with(input.selector)
    assert element_mock.send_keys.call_args_list == [
        mocker.call(password),
        mocker.call(Keys.RETURN)
    ]
