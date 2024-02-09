import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from starlette import status

from pz_setup import app_config

# Clé secrète pour signer les tokens JWT
SECRET_KEY = app_config["auth"]["secret"]
ALGORITHM = "HS256"

security = HTTPBearer()


# Méthode pour vérifier et décoder le JWT
def decode_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
