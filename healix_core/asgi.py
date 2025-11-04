# # import os
# # from django.core.asgi import get_asgi_application

# # # 1. Set default settings and initialize Django
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix_core.settings')
# # http_application = get_asgi_application()

# # # 2. Now import Channels and your other modules
# # from channels.routing import ProtocolTypeRouter, URLRouter
# # from channels.security.websocket import AllowedHostsOriginValidator
# # from django.urls import path
# # import api.consumers 
# # from api.middleware import TokenAuthMiddlewareStack 

# # # 3. Define the router for HTTP and all 3 WebSockets
# # application = ProtocolTypeRouter({
# #     "http": http_application,
# #     "websocket": AllowedHostsOriginValidator(
# #         TokenAuthMiddlewareStack(
# #             URLRouter([
# #                 path("ws/sos_alerts/", api.consumers.SOSConsumer.as_asgi()),
# #                 path("ws/caretaker_alerts/", api.consumers.CaretakerConsumer.as_asgi()),
# #                 path("ws/call/", api.consumers.CallConsumer.as_asgi()), # For WebRTC
# #             ])
# #         )
# #     ),
# # })
# # In healix_core/asgi.py

# import os
# from django.core.asgi import get_asgi_application

# # 1. Set default settings and initialize Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix_core.settings')
# http_application = get_asgi_application()

# # 2. Now import Channels and your other modules
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.urls import path
# import api.consumers 
# from api.middleware import TokenAuthMiddleware  # <-- 1. Import the class directly

# # 3. Define the router for HTTP and all 3 WebSockets
# application = ProtocolTypeRouter({
#     "http": http_application,
#     "websocket": AllowedHostsOriginValidator(
#         TokenAuthMiddleware(  # <-- 2. Use the class directly here
#             URLRouter([
#                 path("ws/sos_alerts/", api.consumers.SOSConsumer.as_asgi()),
#                 path("ws/caretaker_alerts/", api.consumers.CaretakerConsumer.as_asgi()),
#                 path("ws/call/", api.consumers.CallConsumer.as_asgi()), # For WebRTC
#             ])
#         )
#     ),
# })
# import os
# import logging
# from urllib.parse import parse_qs

# # Non-Django imports first
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from channels.db import database_sync_to_async
# from django.urls import re_path

# # Set default settings FIRST
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix_core.settings')

# # Configure Django settings NOW
# from django.core.asgi import get_asgi_application
# http_application = get_asgi_application()

# # NOW import Django models and other Django-specific things
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# # Import your consumers (after Django init)
# import api.consumers

# User = get_user_model()

# logger = logging.getLogger(__name__)

# @database_sync_to_async
# def get_user_from_token(token_key):
#     """
#     Asynchronously gets the user associated with a given access token.
#     """
#     logger.info(f"Attempting to validate token: {token_key[:20]}...")
#     try:
#         # Validate the token and get its payload
#         access_token = AccessToken(token_key)
#         # Get the user ID from the payload
#         user_id = access_token['user_id']
#         # Fetch the user from the database
#         user = User.objects.get(id=user_id)
#         logger.info(f"Token VALID. User: {user.username}")
#         return user
#     except (InvalidToken, TokenError):
#         logger.warning("!!! TOKEN ERROR: Token is invalid or expired.")
#         return AnonymousUser()
#     except User.DoesNotExist:
#         logger.warning("!!! TOKEN ERROR: User in token does not exist.")
#         return AnonymousUser()
#     except Exception as e:
#         logger.error(f"!!! TOKEN ERROR: An unexpected error occurred: {e}")
#         return AnonymousUser()


# class TokenAuthMiddleware:
#     """
#     Custom middleware that takes a token from the query string and
#     authenticates the user.
#     """

#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         query_string = scope.get("query_string", b"").decode("utf-8")
#         query_params = parse_qs(query_string)
        
#         token = query_params.get("token", [None])[0]

#         if token:
#             scope["user"] = await get_user_from_token(token)
#         else:
#             logger.warning("!!! NO TOKEN: No token found in query string.")
#             scope["user"] = AnonymousUser()

#         # Reject anonymous users early (security)
#         if scope["user"].is_anonymous:
#             logger.warning("Anonymous user rejected.")
#             scope["type"] = "disconnected"
#             await send({"type": "websocket.close", "code": 4001})
#             return

#         return await self.inner(scope, receive, send)


# # Define the router
# application = ProtocolTypeRouter({
#     "http": http_application,
#     "websocket": AllowedHostsOriginValidator(
#         TokenAuthMiddleware(
#             URLRouter([
#                 re_path(r"ws/sos_alerts/$", api.consumers.SOSConsumer.as_asgi()),
#                 re_path(r"ws/caretaker_alerts/$", api.consumers.CaretakerConsumer.as_asgi()),
#                 re_path(r"ws/call/$", api.consumers.CallConsumer.as_asgi()),
#             ])
#         )
#     ),
# })
import os
import logging
from urllib.parse import parse_qs

# Non-Django imports first
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.db import database_sync_to_async
from django.urls import re_path

# Set default settings FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix_core.settings')

# Configure Django settings NOW
from django.core.asgi import get_asgi_application
http_application = get_asgi_application()

# NOW import Django models and other Django-specific things
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Import your consumers (after Django init)
import api.consumers

User = get_user_model()

logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user_from_token(token_key):
    """
    Asynchronously gets the user associated with a given access token.
    """
    logger.info(f"Attempting to validate token: {token_key[:20]}...")
    try:
        access_token = AccessToken(token_key)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        logger.info(f"Token VALID. User: {user.username}")
        return user
    except (InvalidToken, TokenError):
        logger.warning("!!! TOKEN ERROR: Token is invalid or expired.")
        return AnonymousUser()
    except User.DoesNotExist:
        logger.warning("!!! TOKEN ERROR: User in token does not exist.")
        return AnonymousUser()
    except Exception as e:
        logger.error(f"!!! TOKEN ERROR: An unexpected error occurred: {e}")
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            logger.warning("!!! NO TOKEN: No token found in query string.")
            scope["user"] = AnonymousUser()

        if scope["user"].is_anonymous:
            logger.warning("Anonymous user rejected.")
            scope["type"] = "disconnected"
            await send({"type": "websocket.close", "code": 4001})
            return

        return await self.inner(scope, receive, send)

# Define the router - WEBSOCKET BEFORE HTTP (critical for Render proxy)
application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                re_path(r"ws/sos_alerts/$", api.consumers.SOSConsumer.as_asgi()),
                re_path(r"ws/caretaker_alerts/$", api.consumers.CaretakerConsumer.as_asgi()),
                re_path(r"ws/call/$", api.consumers.CallConsumer.as_asgi()),
            ])
        )
    ),
    "http": http_application,  # Fallback last
})