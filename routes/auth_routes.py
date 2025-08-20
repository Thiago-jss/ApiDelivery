from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from scheme import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm




auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(id_user, token_lifetime=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration = datetime.now(timezone.utc) + token_lifetime
    desc_info = {"sub": str(id_user), "exp": expiration}
    encoded_token = jwt.encode(desc_info, SECRET_KEY, ALGORITHM)
    return encoded_token



def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user
    





@auth_router.get("/")
async def home():
    """
    this is a placeholder for authentication logic.
    
    """


    return {"message": "Authentication endpoint", "authentication": False}


@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="email already exists; please use a different email")
    else:
        password_hash = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.email, user_schema.username, password_hash, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"message": f"User {user_schema.email} created successfully", "status": "success"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="user not found, please check your credentials")
    
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_lifetime=timedelta(days=7))
        return {
            
            "access_token": access_token,
            "refresh_token": refresh_token, 

            "token_type": "bearer",


        }
    
@auth_router.post("/login-form")
async def acess_form(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(data_form.username, data_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="user not found, please check your credentials")
    
    else:
        access_token = create_token(user.id)
        return {
            
            "access_token": access_token,
            "token_type": "bearer",


        }
        

@auth_router.get("/refresh")

async def toke_refresh(user: User = Depends(verify_token)):
    acess_token = create_token(user.id)
    return {
        "access_token": acess_token,
        "token_type": "bearer"
    }
