# import jwt
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from channels.db import database_sync_to_async
# from channels.middleware import BaseMiddleware
# from channels.auth import AuthMiddlewareStack
# from urllib.parse import parse_qs

# User = get_user_model()

# @database_sync_to_async
# def get_user_from_token(token_key):
#     print(f"Attempting to validate token: {token_key[:20]}...") 
        
#     try:
#         # Assumes your token is signed with SECRET_KEY and HS256
#         payload = jwt.decode(
#             token_key,
#             settings.SECRET_KEY,
#             algorithms=["HS256"]
#         )
#         user = User.objects.get(id=payload['user_id'])
        
#         print(f"Token VALID. User: {user.username}")
#         return user
        
#     except jwt.ExpiredSignatureError:
#         print("!!! TOKEN ERROR: Signature has expired.")
#         return AnonymousUser()
#     except jwt.DecodeError:
#         print("!!! TOKEN ERROR: Failed to decode. Token is invalid.")
#         return AnonymousUser()
#     except User.DoesNotExist:
#         print("!!! TOKEN ERROR: User in token does not exist.")
#         return AnonymousUser()
#     except Exception as e:
#         print(f"!!! TOKEN ERROR: An unexpected error occurred: {e}")
#         return AnonymousUser()

# class TokenAuthMiddleware(BaseMiddleware):
#     """
#     Custom middleware that takes a token from the query string and
#     authenticates the user.
#     """
#     async def __call__(self, scope, receive, send):
#         query_string = scope.get("query_string", b"").decode("utf-8")
#         query_params = parse_qs(query_string)
        
#         token = query_params.get("token", [None])[0]

#         if token:
#             scope["user"] = await get_user_from_token(token)
#         else:
#             print("!!! NO TOKEN: No token found in query string.")
#             scope["user"] = AnonymousUser()

#         return await super().__call__(scope, receive, send)

# def TokenAuthMiddlewareStack(inner):
#     """
#     Wraps the custom token middleware in the standard auth stack.
#     """
#     return TokenAuthMiddleware(AuthMiddlewareStack(inner))
# In api/middleware.py

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token_key):
    """
    Asynchronously gets the user associated with a given access token.
    """
    print(f"Attempting to validate token: {token_key[:20]}...")
    try:
        # Validate the token and get its payload
        access_token = AccessToken(token_key)
        # Get the user ID from the payload
        user_id = access_token['user_id']
        # Fetch the user from the database
        user = User.objects.get(id=user_id)
        print(f"Token VALID. User: {user.username}")
        return user
    except (InvalidToken, TokenError):
        print("!!! TOKEN ERROR: Token is invalid or expired.")
        return AnonymousUser()
    except User.DoesNotExist:
        print("!!! TOKEN ERROR: User in token does not exist.")
        return AnonymousUser()
    except Exception as e:
        print(f"!!! TOKEN ERROR: An unexpected error occurred: {e}")
        return AnonymousUser()


class TokenAuthMiddleware: # No need to inherit from BaseMiddleware
    """
    Custom middleware that takes a token from the query string and
    authenticates the user.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            print("!!! NO TOKEN: No token found in query string.")
            scope["user"] = AnonymousUser()

        # Continue to the inner application
        return await self.inner(scope, receive, send)

# --- DELETE THE TokenAuthMiddlewareStack FUNCTION ---
# It is no longer needed.