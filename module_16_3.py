from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users():
    return users

@app.post('/user/{username}/{age}')
async def new_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
               age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> str:
    current = str(int(max(users, key=int)) + 1)
    users[current] = f'Имя: {username}, возраст: {age}'
    return f'User {current} is registered'

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> str:
    users[str(user_id)]=f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'

@app.delete('/user/{user_id}')
async def user_del(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> str:
    del users[str(user_id)]
    return f'User {user_id} has been deleted'
