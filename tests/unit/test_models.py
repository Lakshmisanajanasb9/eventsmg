from website.models import User

def test_new_user():
    """
    GIVEN a User model
    When a new user is created
    Then check email,hashed password and role fields are defined correctly
    """

    user = User('patkenny70@gmail.com','FlaskisAwesome')
    assert user.email == 'patkenny70@gmail.com'
    assert user.hashed_password != 'FlaskisAwesome'
