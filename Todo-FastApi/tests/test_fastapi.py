from fastapi.testclient import TestClient
from fastapi import FastAPI
from first_poetry import settings
from sqlmodel import SQLModel, create_engine,Session
from first_poetry.main import app, get_session
import pytest

connection_string: str = str(settings.myTestDatabase_url).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300)

#=============================================================
# Refactor with pytest fixture
# 1- Arrange, 2- Act, 3- Assert, 4- Cleanup
@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)

@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session
    app.dependency_overrides[get_session] = test_session
    with TestClient(app=app) as client:
        yield client

#=============================================================


def test_root():
    client = TestClient(app=app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Todo App'}

def test_create_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app=app)
    test_todo = {'name':'todo test'}
    response = test_app.post('/todos', json= test_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == test_todo["name"]

def test_get_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app=app)
    test_todo = {'name':'get all todo test'}
    response = test_app.post('/todos', json= test_todo)
    data = response.json()
    response = test_app.get('/todos')
    new_todo = response.json()[-1]
    assert response.status_code == 200
    assert data["name"] == test_todo["name"]

def test_get_single_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app=app)
    test_todo = {'name':'get single todo test'}
    response = test_app.post('/todos', json= test_todo)
    todo_id = response.json()["id"]
    res = test_app.get(f'/todos/{todo_id}')
    data = res.json()
    assert res.status_code == 200
    assert data["name"] == test_todo["name"]

def test_update_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app=app)
    test_todo = {'name':'edit todo test', "is_complete": False}
    response = test_app.post('/todos', json= test_todo)
    todo_id = response.json()["id"]
    edit_todo = {'name':'edit my current todo test', "is_complete": True}
    res = test_app.put(f'/todos/{todo_id}', json = edit_todo)
    data = res.json()
    print(f'print data: {res.json()} code: {res.status_code} and edit todo {edit_todo["name"]}')
    assert res.status_code == 200
    assert data["name"] == edit_todo["name"]

def test_delete_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app=app)
    test_todo = {'name':'delete todo test', "is_complete": False}
    response = test_app.post('/todos', json= test_todo)
    todo_id = response.json()["id"]
    res = test_app.delete(f'/todos/{todo_id}')
    data = res.json()
    assert res.status_code == 200
    assert data["message"] == "Record Successfully delete"
