from http import HTTPStatus

from fastapi import FastAPI

from fastapi_project.routers import auth, users
from fastapi_project.schemas import Message

app = FastAPI(title='Projeto do Curso de FastAPI')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
