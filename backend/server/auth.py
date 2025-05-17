from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
from backend.server.hasura import HasuraAuth
from backend.settings import settings

# Your Hasura JWT config
jwt_secret_config = {
    "type": "HS256",
    "key": settings.JWT_SECRET,
    "claims_namespace": "https://hasura.io/jwt/claims",
}

auth = HasuraAuth(jwt_secret_config)
security = HTTPBearer()


async def hasura_jwt_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    claims = auth.validate_token(token)

    if not claims:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired JWT token"
        )

    return claims
