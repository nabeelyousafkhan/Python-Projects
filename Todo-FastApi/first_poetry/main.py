from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from first_poetry import settings
from typing import Annotated
from contextlib import asynccontextmanager

class TODO (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=3, max_length=35)
    is_complete: bool = Field(default=False)

connection_string: str = str(settings.myDatabase_url).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo = True)

def create_tables():
    SQLModel.metadata.create_all(engine)

session = Session(engine)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('create tables')
    create_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo App", version='1.0.0')

@app.get('/')
def root():
    return {'message': 'Welcome to Todo App'}

@app.post('/todos', response_model=TODO)
def create_todo(todo: TODO, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get('/todos', response_model= list[TODO])
def get_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(TODO)).all()
    if todos:
        return todos
    else:
        raise HTTPException(status_code= 404, detail="no record found")

@app.get('/todos/{id}', response_model=TODO)
def get_single_todos(id:int , session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(TODO).where(TODO.id == id)).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code= 404, detail="no record found")

@app.put('/todos/{id}')
def get_single_todos(todo: TODO, id:int , session: Annotated[Session, Depends(get_session)]):
    existing_todo = session.exec(select(TODO).where(TODO.id == id)).first()
    if existing_todo:
        existing_todo.name = todo.name
        existing_todo.is_complete = todo.is_complete
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code= 404, detail="no record found")


@app.delete('/todos/{id}')
def get_single_todos(id:int , session: Annotated[Session, Depends(get_session)]):
    todo = session.exec(select(TODO).where(TODO.id == id)).first()
    if todo:
        session.delete(todo)
        session.commit()
        return {'message': 'Record Successfully delete'}
    else:
        raise HTTPException(status_code = 404, detail='No record found')

