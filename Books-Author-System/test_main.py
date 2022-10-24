from fastapi.testclient import TestClient

from main import auth_book_app

client = TestClient(auth_book_app)

###############################################################################################
# Create Tests


def test_read_book():
    response = client.get("/books/4")
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 4,
        "books": []
    }


def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "f5 test",
            "id": 2,
            "books": [
                {
                    "name": "hello",
                    "id": 3,
                    "book_id": 2
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
                    "book_id": 5
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
                    "book_id": 6
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


def test_read_inexistent_book():
    response = client.get("/books/970")
    assert response.status_code == 404
    assert response.json() == {"detail": "book not found"}

###############################################################################################
# Create Tests


# def test_create_book():
#     response = client.post(
#         "/books/",
#         json={
#             "name": "string"
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "name": "string",
#         "id": 9,
#         "books": []
#     }


# def test_create_book_blank_request():
#     response = client.post(
#         "/books/",
#         json={
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {'detail': [{'loc': ['body', 'name'],
#                                            'msg': 'field required',
#                                            'type': 'value_error.missing'}]}


# def test_create_book_wrong_type():
#     response = client.post(
#         "/books/",
#         json={
#             "name": 4
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "book's name cant be blank and should contain atleast one alphabet from A to Z"}


# def test_create_book_wrong_string():
#     response = client.post(
#         "/books/",
#         json={
#             "name": "45@"
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "book's name cant be blank and should contain atleast one alphabet from A to Z"}


# def test_create_book_blank_name():
#     response = client.post(
#         "/books/",
#         json={
#             "name": ""
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "book's name cant be blank and should contain atleast one alphabet from A to Z"}

#########################################################################################################
# Update Tests


# def test_update_book():
#     response = client.patch(
#         "/books/9",
#         json={
#             "name": "Newstring"
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "name": "Newstring",
#         "id": 9,
#         "books": []
#     }


# def test_update_book_blank_request():
#     response = client.patch(
#         "/books/9",
#         json={
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "Empty Json"}


# def test_update_book_wrong_type():
#     response = client.patch(
#         "/books/9",
#         json={
#             "name": 4
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "book's name cant be blank and should contain atleast one alphabet from A to Z"}


# def test_update_book_wrong_string():
#     response = client.patch(
#         "/books/9",
#         json={
#             "name": "45@"
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "book's name cant be blank and should contain atleast one alphabet from A to Z"}


# def test_update_book_blank_name():
#     response = client.patch(
#         "/books/9",
#         json={
#             "name": ""
#         },
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': "Empty Json"}


#########################################################################################################
# Delete Tests


# def test_delete_book():
#     response = client.delete(
#         "/books/9"
#     )
#     assert response.status_code == 200
#     assert response.json() == {"deleted": True}


# def test_delete__inexistent_book():
#     response = client.delete(
#         "/books/99"
#     )
#     assert response.status_code == 404
#     assert response.json() == {"detail": "book not found"}


# def test_delete__bad_format_book():
#     response = client.delete(
#         "/books/99r"
#     )
#     assert response.status_code == 422
#     assert response.json() == {'detail': [{'loc': [
#         'path', 'book_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


# def test_delete__blank_format_book():
#     response = client.delete(
#         "/books/"
#     )
#     assert response.status_code == 405
#     assert response.json() == {'detail': 'Method Not Allowed'}
