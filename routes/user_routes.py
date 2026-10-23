from flask import request,Blueprint
from services.user_service import register_user,login_user
from utils.validation import validate_register_data, validate_login_data
from utils.response import error_response

user_bp=Blueprint('user_bp',__name__)

@user_bp.route('/register',methods=['POST'])
def register():
  data= request.get_json()
  
  username=data.get("username")
  password=data.get('password')
  
  error = validate_register_data(username, password)

  if error:
      return error_response(error, status_code=400)
  
  results= register_user(username,password)
  return results

@user_bp.route('/login',methods=['POST'])
def login():
  data=request.get_json()
  
  username=data.get('username')
  password=data.get('password')
  
  error= validate_login_data(username,password)
  if error:
    return error_response(error,status_code=400)
  
  results=login_user(username,password)
  return results