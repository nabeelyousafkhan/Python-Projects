from fastapi import FastAPI
from sqlmodel import SQLModel,Field,create_engine,Session
from first_class import settings
from contextlib import asynccontextmanager

class TODO(SQLModel,table=True):
    Id: int | None = Field(default=None,primary_key=True)
    title: str

constr: str = str(settings.DB_URL).replace("postgresql","postgresql+psycopg")
engine = create_engine(constr)

def create_db_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan_fun(app:FastAPI):
    create_db_table()
    yield

app = FastAPI(title="FAST API Example", lifespan=lifespan_fun)

@app.get("/")
def read_root():
    return {"Hello": "Pakistan's"}


@app.post("/todo")
def create_todo(todo_data: TODO):
    with Session(engine) as session:
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return todo_data
