import jwt
from config import SECRET_KEY
from functools import wraps
from flask import request
from utils.response import error_response, success_response
from flask import g




def decode_token(token):
  payload= jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
  return payload

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token=None
    
    if 'Authorization' in request.headers:
      auth_header=request.headers['Authorization']
      
      if auth_header.startswith('Bearer'):
        token= auth_header.split(' ')[1]
        
        
    if not token:
      return error_response ('Token is missing', status_code=401)
    
    try:
      data= decode_token(token)
      g.user=data
      
    except:
      return error_response('Invalid token', status_code=401)
      
    
    return f(*args, **kwargs)
  return decorated
