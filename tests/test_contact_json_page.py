import json

from upwork.pages import ContactJsonPage


def test_init(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)

    assert page.driver == driver_mock
    assert page.wait == wait_mock


def test_url():
    page = ContactJsonPage(None, None)
    assert page.url == 'https://www.upwork.com/freelancers/settings/api/v1/contactInfo'


def test_get(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)
    page.get()

    driver_mock.get.assert_called_once_with(page.url)


def test_rawdata(mocker):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)
    page.rawdata()

    driver_mock.get.assert_called_once_with(page.url)
    find_element_by_xpath = driver_mock.find_element_by_xpath
    get_attribute = find_element_by_xpath.return_value.get_attribute
    find_element_by_xpath.assert_called_once_with('//pre')
    get_attribute.assert_called_once_with('innerHTML')


def test_data(mocker, contact_info_fake):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)
    page.rawdata = lambda: json.dumps(contact_info_fake)

    assert page.data() == json.loads(page.rawdata())


def test_userdata(mocker, contact_info_fake):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)
    page.rawdata = lambda: json.dumps(contact_info_fake)

    freelancer = contact_info_fake['freelancer']
    address = freelancer['address']
    assert page.userdata() == {
        'full_name': ' '.join((
            freelancer['firstName'],
            freelancer['lastName']
        )),
        'first_name': freelancer['firstName'],
        'last_name': freelancer['lastName'],
        'email': freelancer['email']['address'],
        'phone_number': freelancer['phone'],
        'picture_url': freelancer['portrait']['bigPortrait'],
        'address': {
            'line1': address['street'],
            'line2': address['additionalInfo'],
            'city': address['city'],
            'state': address['state'],
            'postal_code': address['zip'],
            'country': address['country'],
        }
    }


def test_profile(mocker, contact_info_fake):
    driver_mock, wait_mock = mocker.MagicMock(), mocker.MagicMock()

    page = ContactJsonPage(driver_mock, wait_mock)
    page.rawdata = lambda: json.dumps(contact_info_fake)
    profile = page.profile()

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
