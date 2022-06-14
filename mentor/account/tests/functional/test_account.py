# def test_get_account_by_id(client):
#     pass


# def test_get_accounts(client):
#     pass


def test_signup(test_client):
    response = test_client.post("/api/account/signup")
    assert response.status_code == 201
    assert response.message == "johndoe@gmail.com created successfully"


# def test_verify_email(client):
#     pass


# def test_complete_profile(client):
#     pass


# def test_create_role(client):
#     pass


# def test_get_all_roles(client):
#     pass


# def test_login(client):
#     pass


# def test_get_google_provider_cfg(client):
#     pass


# def test_google_login(client):
#     pass


# def test_google_callback(client):
#     pass


# def test_github_login(client):
#     pass


# def test_githublogout(client):
#     pass
