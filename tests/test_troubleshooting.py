from upwork.troubleshooting import screenshot


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
