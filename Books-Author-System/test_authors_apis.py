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


def test_read_author(clientX):
    response = clientX.get("/authors/4")
    assert response.status_code == 200
    assert response.json() == {
        "name": "string",
        "id": 4,
        "books": []
    }


def test_read_authors(clientX):
    response = clientX.get("/authors/")
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


def test_read_inexistent_author(clientX):
    response = clientX.get("/authors/970")
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}

# ###############################################################################################
# # Create Tests


def test_create_author(clientX):
    response = clientX.post(
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


def test_create_author_blank_request(clientX):
    response = clientX.post(
        "/authors/",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'name'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}


def test_create_author_wrong_type(clientX):
    response = clientX.post(
        "/authors/",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_author_wrong_string(clientX):
    response = clientX.post(
        "/authors/",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_create_author_blank_name(clientX):
    response = clientX.post(
        "/authors/",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}

# #########################################################################################################
# # Update Tests


def test_update_author(clientX):
    response = clientX.patch(
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


def test_update_author_blank_request(clientX):
    response = clientX.patch(
        "/authors/9",
        json={
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


def test_update_author_wrong_type(clientX):
    response = clientX.patch(
        "/authors/9",
        json={
            "name": 4
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_author_wrong_string(clientX):
    response = clientX.patch(
        "/authors/9",
        json={
            "name": "45@"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Author's name cant be blank and should contain atleast one alphabet from A to Z"}


def test_update_author_blank_name(clientX):
    response = clientX.patch(
        "/authors/9",
        json={
            "name": ""
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': "Empty Json"}


# #########################################################################################################
# # Delete Tests


def test_delete_author(clientX):
    response = clientX.delete(
        "/authors/9"
    )
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_delete__inexistent_author(clientX):
    response = clientX.delete(
        "/authors/99"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


def test_delete__bad_format_author(clientX):
    response = clientX.delete(
        "/authors/99r"
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'author_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_delete__blank_format_author(clientX):
    response = clientX.delete(
        "/authors/"
    )
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}
