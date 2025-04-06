from typing import List
from datetime import timedelta

import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends, status

from models import User, Password
from jwt_utils import get_current_client_by_jwt, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


app = FastAPI()

user_db = {
    "admin":  User(login='admin', password=Password.hash_password('secret'))
}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = False
    
    if form_data.username in user_db:
        password = user_db[form_data.username].password
        if Password.verify_password(form_data.password, password):
            password_check = True

    if password_check:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/users", response_model=User)
async def create_user(user: User, current_user: str = Depends(get_current_client_by_jwt)):
    for u in user_db.keys():
        if u == user.login:
            raise HTTPException(status_code=404, detail="User already exist")
    user.password = Password.hash_password(user.password)
    user_db[user.login] = user
    return user


@app.get("/users", response_model=List[str])
async def get_users_logins_list(current_user: str = Depends(get_current_client_by_jwt)):
    return user_db.keys()


@app.get("/users/{user_login}", response_model=User)      
async def get_user_by_login(user_login: str, current_user: str = Depends(get_current_client_by_jwt)):
    for _, login in enumerate(user_db):
        if user_db[login].login == user_login:
            return user_db[login]
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_login}", response_model=User)
async def update_user(user_login: str, updated_user: User, current_user: str = Depends(get_current_client_by_jwt)):
    for _, login in enumerate(user_db):
        if user_db[login].login == user_login:
            user_db[login] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_login}", response_model=User)
async def delete_user(user_login: str, current_user: str = Depends(get_current_client_by_jwt)):
    for _, login in enumerate(user_db):
        if user_db[login].login == user_login:
            deleted_user = user_db.pop(login)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")