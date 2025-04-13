from website.models import Customer

def test_new_user():
    """
    GIVEN a User model
    When a new user is created
    Then check email,hashed password and role fields are defined correctly
    """

    customer = Customer(
        customer_id=1,
        first_name='John',
        last_name='Cena',
        email='johncena123@gmail.com',
        phone='07909756744',
        location='Chicago'
    )
    assert customer.customer_id == '1'
    assert customer.first_name == 'John'
    assert customer.last_name == 'Cena'
    assert customer.email == 'johncena123@gmail.com'
    assert customer.phone == '07909756744'
    assert customer.location == 'Chicago'

