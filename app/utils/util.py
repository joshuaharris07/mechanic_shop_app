#File for token functions
from datetime import datetime, timedelta, timezone
from jose import jwt
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "secret key for login"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=4), #timedelta is setting the expiration at 4 hours from login
        'iat': datetime.now(timezone.utc), #iat is what time the token is issued at
        'sub':  str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:

            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'missing token'}), 400
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print(data)
                customer_id = data['sub']
            except jwt.ExpiredSignatureError as err:
                return jsonify({'message': 'token expired'}), 400
            except jwt.InvalidTokenError as err:
                return jsonify({'message': 'invalid token'}), 400
            
            return f(customer_id, *args, **kwargs)
        
        else:  
            return jsonify({'message': 'Please log in to access this function'}), 400
    return decorated