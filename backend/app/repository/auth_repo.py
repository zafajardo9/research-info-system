
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError

from app.config import SECRET_KEY, ALGORITHM


class JWTRepo:

    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)  # token expires

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt


    def decode_token(self):
        try:
            decoded_token = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token if decoded_token.get("exp") >= datetime.datetime().timestamp() else None
        except ExpiredSignatureError:
            return None  # Explicitly return None if the token is expired
        except JWTError:
            return None

    @staticmethod
    def extract_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})


    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except ExpiredSignatureError:
            return False
        except JWTError:
            return False
        
        
    # @staticmethod
    # def verify_jwt(jwt_token: str):
    #     return True if jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM]) is not None else False
