from typing import List
from datetime import timedelta

import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends, status

from models import User, Password, DB_User
from db_connect import get_db_connection
from jwt_utils import get_current_client_by_jwt, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


app = FastAPI()


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 user_db=Depends(get_db_connection)):
    password_check = False
    pg_user_data = user_db.query(DB_User).filter(DB_User.login == form_data.username).first()
    if pg_user_data:
        password = pg_user_data.password
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


@app.post("/users", response_model=str)
async def create_user(user: User, current_user: str = Depends(get_current_client_by_jwt),
                      user_db=Depends(get_db_connection)):
    pg_user_data = user_db.query(DB_User).filter(DB_User.login == user.login).first()
    if pg_user_data:
        raise HTTPException(status_code=404, detail="User already exist")
    user.password = Password.hash_password(user.password)
    new_user = DB_User(**user.model_dump())
    user_db.add(new_user)
    user_db.commit()
    return f'User {user.login} created!'


@app.get("/users", response_model=List[User])
async def get_users_logins_list(current_user: str = Depends(get_current_client_by_jwt),
                                user_db=Depends(get_db_connection)):
    return list(user_db.query(DB_User).all())


@app.get("/users/{user_login}", response_model=User)      
async def get_user_by_login(user_login: str, current_user: str = Depends(get_current_client_by_jwt),
                            user_db=Depends(get_db_connection)):
    pg_user_data = user_db.query(DB_User).filter(DB_User.login == user_login).first()
    if pg_user_data:
        return pg_user_data
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_login}", response_model=User)
async def update_user(user_login: str, updated_user: User, current_user: str = Depends(get_current_client_by_jwt),
                      user_db=Depends(get_db_connection)):
    pg_user_data = user_db.query(DB_User).filter(DB_User.login == user_login).first()
    if pg_user_data:
        setattr(pg_user_data, 'name', updated_user.name)
        setattr(pg_user_data, 'password', updated_user.password)
        user_db.commit()
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_login}", response_model=str)
async def delete_user(user_login: str, current_user: str = Depends(get_current_client_by_jwt),
                      user_db=Depends(get_db_connection)):
    if user_login == 'admin':
        raise HTTPException(status_code=404, detail="admin can't be deleted")    
    pg_user_data = user_db.query(DB_User).filter(DB_User.login == user_login).first()
    if pg_user_data:
        user_db.delete(pg_user_data)
        user_db.commit()
        return f'User {user_login} deleted!'
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")