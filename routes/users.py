from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from database.connection import Database
from auth.hash_password import HashPassword

user_router = APIRouter(
    tags=["User"],
)
users = {}
user_database = Database(User)
hash_password = HashPassword()

@user_router.post("/signup")
async def sign_new_user(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with provided exists already"
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message" : "User successfully registered!"
    }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        print(f"User not found: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    verified = hash_password.verify_hash(user.password, user_exist.password)
    print(f"Password verification result: {verified}")
    
    if verified:
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password"
    )