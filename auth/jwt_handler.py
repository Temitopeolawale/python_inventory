# auth/jwt_handler.py
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union
import os
from dotenv import load_dotenv
import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create HTTP Bearer security scheme
security = HTTPBearer()

class JWTHandler:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        
        # Validate SECRET_KEY exists
        if not self.secret_key:
            logger.error("SECRET_KEY not found in environment variables!")
            raise ValueError("SECRET_KEY must be set in environment variables")
        
        logger.info(f"JWT Handler initialized with secret key length: {len(self.secret_key)}")
        
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7

    def _encode(self, data: Dict, expire: datetime) -> str:
        try:
            payload = data.copy()
            payload.update({
                "exp": expire,
                "iat": datetime.now(timezone.utc),
            })
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            logger.error(f"Token encoding failed: {str(e)}")
            raise

    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        try:
            expire = datetime.now(timezone.utc) + (
                expires_delta or timedelta(minutes=self.access_token_expire_minutes)
            )
            return self._encode({**data, "type": "access"}, expire)
        except Exception as e:
            logger.error(f"Access token creation failed: {str(e)}")
            raise

    def create_refresh_token(self, data: Dict) -> str:
        try:
            expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
            return self._encode({**data, "type": "refresh"}, expire)
        except Exception as e:
            logger.error(f"Refresh token creation failed: {str(e)}")
            raise

    def decode_token(self, token: str) -> Dict:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return {"error": "Invalid token"}
        except Exception as e:
            logger.error(f"Token processing failed: {str(e)}")
            return {"error": "Token processing failed"}

# Initialize with error handling
try:
    jwt_handler = JWTHandler()
except ValueError as e:
    logger.error(f"Failed to initialize JWT handler: {str(e)}")
    jwt_handler = None

def generate_tokens(user_id: Union[str, int], username: str, **extra_data) -> Dict[str, str]:
    if jwt_handler is None:
        raise RuntimeError("JWT handler not properly initialized")
    
    try:
        if not user_id or not username:
            raise ValueError("user_id and username are required")
        
        data = {"user_id": str(user_id), "username": username, **extra_data}
        tokens = {
            "access_token": jwt_handler.create_access_token(data),
            "refresh_token": jwt_handler.create_refresh_token(data),
            "token_type": "bearer",
        }
        return tokens
        
    except Exception as e:
        logger.error(f"Failed to generate tokens for user {username}: {str(e)}")
        raise

def verify_token(token: str) -> Dict:
    if jwt_handler is None:
        return {"error": "JWT handler not available"}
    
    if not token:
        return {"error": "No token provided"}
    
    return jwt_handler.decode_token(token)

# FastAPI Dependency Functions
def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract and validate JWT token from Authorization header, return user ID
    """
    try:
        # Get token from Authorization header
        token = credentials.credentials
        
        # Verify and decode token
        decoded_token = verify_token(token)
        
        # Check for errors in token verification
        if "error" in decoded_token:
            logger.error(f"Token verification failed: {decoded_token['error']}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication: {decoded_token['error']}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check token type (should be access token)
        if decoded_token.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract user ID
        user_id = decoded_token.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Extract and validate JWT token, return full decoded token data
    """
    try:
        # Get token from Authorization header
        token = credentials.credentials
        
        # Verify and decode token
        decoded_token = verify_token(token)
        
        # Check for errors in token verification
        if "error" in decoded_token:
            logger.error(f"Token verification failed: {decoded_token['error']}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication: {decoded_token['error']}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check token type (should be access token)
        if decoded_token.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return decoded_token
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )