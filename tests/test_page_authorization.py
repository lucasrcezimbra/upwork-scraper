from selenium.webdriver.common.keys import Keys

from upwork.pages import AuthorizationPage, SecretAnswerInput


def test_init(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = AuthorizationPage(driver_mock, wait_mock)

    assert page.driver == driver_mock
    assert page.wait == wait_mock
    assert isinstance(page.secret_answer_input, SecretAnswerInput)


def test_needs_authorization(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = AuthorizationPage(driver_mock, wait_mock)

    driver_mock.title = 'Device authorization'
    assert page.needs_authorization() is True

    driver_mock.title = 'Not authorization'
    assert page.needs_authorization() is False


def test_ensure_authorization_when_dont_needs(mocker):
    secret_answer = 's3cr3t_4nsw3r'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    secret_answer_input = mocker.MagicMock()
    wait_mock.until.side_effect = [secret_answer_input]
    driver_mock.title = 'Not Device authorization'
    EC_mock = mocker.patch('upwork.pages.EC')

    page = AuthorizationPage(driver_mock, wait_mock)
    page.ensure_authorization(secret_answer)

    assert page.needs_authorization() is False

    assert wait_mock.until.call_count == 0
    EC_mock.presence_of_element_located.assert_not_called()
    secret_answer_input.send_keys.assert_not_called()
    EC_mock.presence_of_element_located.assert_not_called()


def test_ensure_authorization_when_needs(mocker):
    secret_answer = 's3cr3t_4nsw3r'
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    secret_answer_input = mocker.MagicMock()
    wait_mock.until.side_effect = [secret_answer_input]
    driver_mock.title = 'Device authorization'
    EC_mock = mocker.patch('upwork.pages.EC')

    page = AuthorizationPage(driver_mock, wait_mock)
    page.ensure_authorization(secret_answer)

    assert page.needs_authorization() is True

    assert wait_mock.until.call_count == 1
    EC_mock.presence_of_element_located.call_args_list == [
        mocker.call(SecretAnswerInput.selector),
    ]
    assert secret_answer_input.send_keys.call_args_list == [
        mocker.call(secret_answer),
        mocker.call(Keys.RETURN)
    ]
    EC_mock.presence_of_element_located.call_args_list == [
        mocker.call(SecretAnswerInput.selector),
    ]
