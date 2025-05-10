import pytest
from app import schemas
from jose import jwt
from app.config import settings



@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com",
                 "password": "hello123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user




# def test_root(client):

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello@gmail.com", "password": "hello123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'hello123', 401),
    ('hello@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'hello123', 422),        # Here the whole username field is not passed
    ('hello@gmail.com', None, 422)  # Here the whole password field is not passed
])
def test_incorrect_login(test_user, client, email, password, status_code):
    login_data = {}
    if email is not None:
        login_data["username"] = email
    if password is not None:
        login_data["password"] = password

    res = client.post("/login", data=login_data)
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

# or
# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'hello123', 401),
#     ('hello@gmail.com', 'wrongpassword', 401),
#     ('wrongemail@gmail.com', 'wrongpassword', 401),
#     (None, 'hello123', 401),
#     ('hello@gmail.com', None, 401)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     res = client.post(
#         "/login", data={"username": email, "password": password})

#     assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

