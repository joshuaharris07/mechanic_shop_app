#File for token functions
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose

SECRET_KEY = "a super secret, secret key"

def encode_token(user_id): #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #Setting the expiration time to an hour past now
        'iat': datetime.now(timezone.utc), #Issued at
        'sub':  str(user_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token