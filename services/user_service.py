from database.db import create_user, get_user_by_username
from utils.response import error_response,success_response
from werkzeug.security import generate_password_hash,check_password_hash
from utils.logger import logger
from config import SECRET_KEY
import jwt
import datetime


#---------------REGISTER-------------

def register_user(username,password):
  
  existing_user= get_user_by_username(username)
  
  if existing_user:
    return error_response('Username already exist', status_code=409)
  
  hashed_password=generate_password_hash(password)
  
  user_id= create_user(username,hashed_password)
  
  return success_response('User registered successfully',
                          {'user_id': user_id})
  
#-------------------LOG IN------------------------

def login_user(username,password):
  
  user= get_user_by_username(username)
  
  if not user:
    return error_response("Invalid username or password", status_code=401)
  
  if not check_password_hash(user["password"],password):
    logger.warning(f"Failed login attempt for username: {username}")
    return error_response('Invalid username or password', status_code=401)
  
  token=jwt.encode({
    'user_id': user['id'],
    'username': user['username'],
    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
  },
                   SECRET_KEY,
                   algorithm="HS256"
                   )
  
  
  return success_response(
    f"Successful login, Hello {user['username']}",
    {
        'token':token,
        "id": user["id"],
        "username": user["username"]
    }
)

  


