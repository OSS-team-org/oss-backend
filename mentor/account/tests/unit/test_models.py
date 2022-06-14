def test_new_account(new_account):
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that the email field is defined correctly
    """
    assert new_account.email == "johndoe@gmail.com"
