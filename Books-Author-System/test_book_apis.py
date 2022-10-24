from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import auth_book_app as app
from database import Base
from main import get_db


##########################################################################
# Create the new database session

SQLALCHEMY_DATABASE_URL = "sqlite:///./fakedb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():

    # Create the database

    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def clientX(session):

    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

# ###############################################################################################
# # Read Tests


def test_read_book_by_book_id(clientX):
    response = clientX.get("/books/4")
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 4,
        "author_id": 444
    }


def test_read_book_by_author_id(clientX):
    response = clientX.get("/books/?authorid=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "string",
            "id": 1,
            "author_id": 1
        },
        {
            "name": "string",
            "id": 2,
            "author_id": 1
        }
    ]


def test_read_book_by_wrong_author_id(clientX):
    response = clientX.get("/books/?authorid=1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Books not found"}


def test_read_books(clientX):
    response = clientX.get("/books/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "string",
            "id": 1,
            "author_id": 1
        },
        {
            "name": "string",
            "id": 2,
            "author_id": 1
        },
        {
            "name": "hello",
            "id": 3,
            "author_id": 2
        },
        {
            "name": "string",
            "id": 4,
            "author_id": 444
        },
        {
            "name": "string",
            "id": 5,
            "author_id": 444
        },
        {
            "name": "string",
            "id": 6,
            "author_id": 555
        },
        {
            "name": "string",
            "id": 7,
            "author_id": 6
        },
        {
            "name": "aweet",
            "id": 8,
            "author_id": 5
        }
    ]


def test_read_inexistent_book(clientX):
    response = clientX.get("/books/970")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

# ###############################################################################################
# # Create Tests


def test_create_book(clientX):
    response = clientX.post(
        "/books/2",
        json={
            "name": "string"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 9,
        "author_id": 2
    }


def test_create_book_blank_request(clientX):
    response = clientX.post(
        "/books/2",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'name'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}


def test_create_book_wrong_type(clientX):
    response = clientX.post(
        "/books/2",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Book's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_book_wrong_string(clientX):
    response = clientX.post(
        "/books/2",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Book's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_book_blank_name(clientX):
    response = clientX.post(
        "/books/2",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Book's name cant be blank and should contain atleast one alphabet from A to Z"}

# #########################################################################################################
# # Update Tests


def test_update_book(clientX):
    response = clientX.patch(
        "/books/9",
        json={
            "name": "Newstring"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Newstring",
        "id": 9,
        "author_id": 2
    }


def test_update_book_blank_request(clientX):
    response = clientX.patch(
        "/books/9",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


def test_update_book_wrong_type(clientX):
    response = clientX.patch(
        "/books/9",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Book's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_book_wrong_string(clientX):
    response = clientX.patch(
        "/books/9",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Book's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_book_blank_name(clientX):
    response = clientX.patch(
        "/books/9",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


# #########################################################################################################
# # Delete Tests


def test_delete_book(clientX):
    response = clientX.delete(
        "/books/9"
    )
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_delete__inexistent_book(clientX):
    response = clientX.delete(
        "/books/99"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_delete__bad_format_book(clientX):
    response = clientX.delete(
        "/books/99r"
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'book_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_delete__blank_format_book(clientX):
    response = clientX.delete(
        "/books/"
    )
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}
