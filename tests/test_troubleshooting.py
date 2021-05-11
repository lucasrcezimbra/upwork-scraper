import pytest

from upwork import troubleshooting
from upwork.troubleshooting import handle_exception, screenshot


def test_screeshot(mocker):
    driver_mock = mocker.MagicMock()

    filepath = 'test.png'
    screenshot(driver_mock, filepath=filepath)

    driver_mock.save_screenshot.assert_called_once_with(filepath)


def test_screeshot_without_filepath(mocker):
    driver_mock = mocker.MagicMock()
    uuid = 'random_uuid4'
    mocker.patch('upwork.troubleshooting.uuid4', return_value=uuid)

    screenshot(driver_mock)

    driver_mock.save_screenshot.assert_called_once_with(f'{uuid}.png')


def test_handle_exception_debug_false(mocker):
    mocker.patch('upwork.settings.DEBUG', False)
    screenshot_spy = mocker.spy(troubleshooting, 'screenshot')
    driver_mock = mocker.MagicMock()

    exception = Exception()
    with pytest.raises(Exception):
        handle_exception(exception, driver_mock)

    screenshot_spy.assert_called_once_with(driver_mock)
    driver_mock.quit.assert_called_once()


def test_handle_exception_debug_true(mocker):
    pdb_mock = mocker.patch('upwork.troubleshooting.pdb')
    mocker.patch('upwork.settings.DEBUG', True)
    screenshot_spy = mocker.spy(troubleshooting, 'screenshot')
    driver_mock = mocker.MagicMock()

    handle_exception(Exception(), driver_mock)

    screenshot_spy.assert_called_once_with(driver_mock)
    driver_mock.quit.assert_not_called()
    pdb_mock.set_trace.assert_called_once()
