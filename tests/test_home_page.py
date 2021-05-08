
from upwork import HomePage


def test_init(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = HomePage(driver_mock, wait_mock)

    assert page.driver == driver_mock
    assert page.wait == wait_mock


def test_data(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()
    EC_mock = mocker.patch('upwork.EC')

    page = HomePage(driver_mock, wait_mock)
    page.data()

    EC_mock.title_contains.assert_called_once_with('My Job Feed')
    wait_mock.until.assert_called_once_with(EC_mock.title_contains.return_value)
    driver_mock.execute_script.assert_called_once_with(
        'return window.__INITIAL_STATE__.organizations.activeItem;')


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

    page = HomePage(driver_mock, wait_mock)

    assert page.userdata() == {
        'name': name,
        'title': title,
    }
