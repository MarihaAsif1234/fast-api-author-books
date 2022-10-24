from fastapi.testclient import TestClient

from main import auth_book_app

client = TestClient(auth_book_app)

###############################################################################################
# Create Tests


def test_read_author():
    response = client.get("/authors/4")
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 4,
        "books": []
    }


def test_read_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "f5 test",
            "id": 2,
            "books": [
                {
                    "name": "hello",
                    "id": 3,
                    "author_id": 2
                }
            ]
        },
        {
            "name": "string",
            "id": 4,
            "books": []
        },
        {
            "name": "54",
            "id": 5,
            "books": [
                {
                    "name": "aweet",
                    "id": 8,
                    "author_id": 5
                }
            ]
        },
        {
            "name": "44",
            "id": 6,
            "books": [
                {
                    "name": "string",
                    "id": 7,
                    "author_id": 6
                }
            ]
        },
        {
            "name": "44",
            "id": 7,
            "books": []
        },
        {
            "name": "7h",
            "id": 8,
            "books": []
        }
    ]


def test_read_inexistent_author():
    response = client.get("/authors/970")
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}

###############################################################################################
# Create Tests


def test_create_author():
    response = client.post(
        "/authors/",
        json={
            "name": "string"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 9,
        "books": []
    }


def test_create_author_blank_request():
    response = client.post(
        "/authors/",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'name'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}


def test_create_author_wrong_type():
    response = client.post(
        "/authors/",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_author_wrong_string():
    response = client.post(
        "/authors/",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_author_blank_name():
    response = client.post(
        "/authors/",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}

#########################################################################################################
# Update Tests


def test_update_author():
    response = client.patch(
        "/authors/9",
        json={
            "name": "Newstring"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Newstring",
        "id": 9,
        "books": []
    }


def test_update_author_blank_request():
    response = client.patch(
        "/authors/9",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


def test_update_author_wrong_type():
    response = client.patch(
        "/authors/9",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_author_wrong_string():
    response = client.patch(
        "/authors/9",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_author_blank_name():
    response = client.patch(
        "/authors/9",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


#########################################################################################################
# Delete Tests


def test_delete_author():
    response = client.delete(
        "/authors/9"
    )
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_delete__inexistent_author():
    response = client.delete(
        "/authors/99"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


def test_delete__bad_format_author():
    response = client.delete(
        "/authors/99r"
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'author_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_delete__blank_format_author():
    response = client.delete(
        "/authors/"
    )
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}
