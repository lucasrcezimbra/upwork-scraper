from upwork.models import Address, Profile


def test_profile():
    address = Address(
        line1='Street 1',
        line2='Number 2',
        city='New York',
        state='NY',
        postal_code='0123456',
        country='United States',
    )
    assert Profile(
        full_name='John Snow',
        first_name='John',
        last_name='Snow',
        email='john@got.com',
        phone_number='+55510987654321',
        picture_url='https://example.com/john.jpg',
        address=address,
    )
