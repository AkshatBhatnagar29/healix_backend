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
# from api.middleware import TokenAuthMiddlewareStack 

# # 3. Define the router for HTTP and all 3 WebSockets
# application = ProtocolTypeRouter({
#     "http": http_application,
#     "websocket": AllowedHostsOriginValidator(
#         TokenAuthMiddlewareStack(
#             URLRouter([
#                 path("ws/sos_alerts/", api.consumers.SOSConsumer.as_asgi()),
#                 path("ws/caretaker_alerts/", api.consumers.CaretakerConsumer.as_asgi()),
#                 path("ws/call/", api.consumers.CallConsumer.as_asgi()), # For WebRTC
#             ])
#         )
#     ),
# })
# In healix_core/asgi.py

import os
from django.core.asgi import get_asgi_application

# 1. Set default settings and initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healix_core.settings')
http_application = get_asgi_application()

# 2. Now import Channels and your other modules
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
import api.consumers 
from api.middleware import TokenAuthMiddleware  # <-- 1. Import the class directly

# 3. Define the router for HTTP and all 3 WebSockets
application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(  # <-- 2. Use the class directly here
            URLRouter([
                path("ws/sos_alerts/", api.consumers.SOSConsumer.as_asgi()),
                path("ws/caretaker_alerts/", api.consumers.CaretakerConsumer.as_asgi()),
                path("ws/call/", api.consumers.CallConsumer.as_asgi()), # For WebRTC
            ])
        )
    ),
})