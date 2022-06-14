import pytest
from mentor.app import create_app
from mentor.extensions import db
from mentor.settings import ProdConfig, TestConfig
from mentor.account.models import Account, Role, Accountprofile, UserRoles


@pytest.fixture(scope="module")
def new_account():
    account = Account("johndoe@gmail.com")
    return account


@pytest.fixture(scope="module")
def test_client():
    CONFIG = TestConfig
    app = create_app(CONFIG)

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = Account(email="johndoe1@gmail.com")
    user2 = Account(email="johndoe2@gmail.com")
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="function")
def new_account_signup(test_client):
    test_client.post(
        "/api/account/signup",
        data=dict(email="johndoe@gmail.com"),
        follow_redirects=True,
    )
    yield  # this is where the testing happens!
