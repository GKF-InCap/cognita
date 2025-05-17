import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from typing import Optional, Dict


class HasuraAuth:
    def __init__(self, jwt_secret: Dict):
        """
        Initialize the HasuraAuth with the JWT secret used by Hasura.
        :param jwt_secret: The secret dict, e.g. {
            "type": "HS256",
            "key": "your-secret-key"
        }
        """
        self.algorithm = jwt_secret.get("type", "HS256")
        self.secret_key = jwt_secret["key"]
        self.claim_namespace = jwt_secret.get(
            "claims_namespace", "https://hasura.io/jwt/claims"
        )

    def validate_token(self, token: str) -> Optional[Dict]:
        """
        Validates a JWT token and returns the Hasura claims if valid.
        :param token: JWT token string
        :return: Decoded token payload or None if invalid
        """
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            hasura_claims = decoded.get(self.claim_namespace)
            if not hasura_claims:
                raise ValueError("Missing Hasura claims")
            return hasura_claims
        except ExpiredSignatureError:
            print("Token has expired")
        except InvalidTokenError as e:
            print(f"Invalid token: {str(e)}")
        except Exception as e:
            print(f"Token validation error: {str(e)}")
        return None
