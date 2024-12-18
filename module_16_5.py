from fastapi import FastAPI, status, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def use(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post('/user/{username}/{age}')
async def new_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
               age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')], user: User) -> User:
    if users:
        users_id = len(users)+1
    else:
        users_id = 1
    user.id = users_id
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:

    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')



@app.delete('/user/{user_id}')
async def user_del(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')], user: User) -> User:

    for index, user in enumerate(users):
        if user.id == user_id:
            del_user = users.pop(index)
            return del_user
    raise HTTPException(status_code=404, detail="The User was not found")