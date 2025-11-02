# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# # --- 1. For Doctors (Global Alerts) ---
# class SOSConsumer(AsyncWebsocketConsumer):
#     """
#     This consumer handles the WebSocket connection for doctors
#     to receive real-time SOS alerts.
#     """
    
#     async def connect(self):
#         user = self.scope["user"]
        
#         # --- Debugging Logs ---
#         print(f"--- [SOSConsumer] Connection Attempt ---")
#         print(f"User: {user}")
#         print(f"Is Authenticated: {user.is_authenticated}")
#         if hasattr(user, 'role'):
#             print(f"User Role: {user.role}")
#         else:
#             print("User has no 'role' attribute.")
#         print(f"----------------------------------------")
        
#         # Only allow authenticated doctors to connect
#         if not user.is_authenticated or user.role != 'doctor':
#             print("!!! [SOSConsumer] REJECTING: Not a doctor.")
#             await self.close()
#             return

#         self.group_name = "doctors_sos_group"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print(f"✅ [SOSConsumer] Connected for Doctor: {user.username}")

#     async def disconnect(self, close_code):
#         # This check prevents crashes if the connection was rejected
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )
        
#         username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
#         print(f"[SOSConsumer] Disconnected for: {username}")

#     async def sos_notification(self, event):
#         message_data = event['message']
#         # Send the sos_event_id to the doctor's app
#         await self.send(text_data=json.dumps({
#             'type': 'sos_notification',
#             'sos_event_id': message_data.get('sos_event_id')
#         }))


# # --- 2. For Caretakers (Private Alerts) ---
# class CaretakerConsumer(AsyncWebsocketConsumer):
#     """
#     Handles WebSocket connections for individual caretakers
#     to receive alerts specific to their hostel.
#     """
    
#     async def connect(self):
#         user = self.scope["user"]
        
#         print(f"--- [CaretakerConsumer] Connection Attempt ---")
#         print(f"User: {user}")
#         print(f"Is Authenticated: {user.is_authenticated}")
#         if hasattr(user, 'role'):
#             print(f"User Role: {user.role}")
        
#         # Only allow authenticated staff to connect
#         if not user.is_authenticated or user.role not in ['staff','caretaker']  :
#             print("!!! [CaretakerConsumer] REJECTING: Not staff.")
#             await self.close()
#             return
            
#         # Create a unique, private group name for this user
#         self.group_name = f"caretaker_{user.id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print(f"✅ [CaretakerConsumer] Connected for: {user.username} in group {self.group_name}")

#     async def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )
#         username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
#         print(f"[CaretakerConsumer] Disconnected for: {username}")

#     # This function is called from SOSCreateView
#     async def sos_notification(self, event):
#         message_data = event['message']
#         # Send the full message (including who to call) to the caretaker
#         await self.send(text_data=json.dumps({
#             'type': 'sos_notification',
#             'message': message_data
#         }))


# # --- 3. For WebRTC (Private Signaling) ---
# class CallConsumer(AsyncWebsocketConsumer):
#     """
#     Handles the WebRTC signaling between two specific peers.
#     This connects to your *other* signaling server (port 8765)
#     but your Django one (port 8000).
#     """
    
#     async def connect(self):
#         user = self.scope["user"]
        
#         print(f"--- [CallConsumer] Connection Attempt ---")
#         print(f"User: {user}")

#         if not user.is_authenticated:
#             print("!!! [CallConsumer] REJECTING: Not authenticated.")
#             await self.close()
#             return

#         # Each user joins their OWN personal group based on their username
#         self.user_id = user.username
#         self.group_name = f"call_{self.user_id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print(f"✅ [CallConsumer] Connected for user: {self.user_id}")

#     async def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )
#         username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
#         print(f"[CallConsumer] Disconnected for: {username}")

#     # This is the main signaling logic
#     async def receive(self, text_data):
#         """
#         Receives a message from one peer and relays it to the target peer.
#         """
#         data = json.loads(text_data)
#         target_user_id = data.get('target') # The username of the person to call

#         if not target_user_id:
#             print("!!! [CallConsumer] Received message without a target.")
#             return

#         target_group = f"call_{target_user_id}"
#         data['from'] = self.user_id # Add the sender's ID

#         print(f"[CallConsumer] Relaying '{data.get('type')}' from {self.user_id} to {target_user_id}")

#         # Relay the message to the target's group
#         await self.channel_layer.group_send(
#             target_group,
#             {
#                 'type': 'call_message', # This will call the 'call_message' function
#                 'message': data
#             }
#         )

#     async def call_message(self, event):
#         """
#         Sends the relayed message down to the client's WebSocket.
#         """
#         await self.send(text_data=json.dumps(event['message']))

import json
from channels.generic.websocket import AsyncWebsocketConsumer


# --- 1. For Doctors (Global Alerts) ---
class SOSConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles the WebSocket connection for doctors
    to receive real-time SOS alerts.
    """
    
    async def connect(self):
        user = self.scope["user"]
        
        print(f"--- [SOSConsumer] Connection Attempt ---")
        print(f"User: {user}")
        print(f"Is Authenticated: {user.is_authenticated}")
        if hasattr(user, 'role'):
            print(f"User Role: {user.role}")
        else:
            print("User has no 'role' attribute.")
        print(f"----------------------------------------")
        
        if not user.is_authenticated or user.role != 'doctor':
            print("!!! [SOSConsumer] REJECTING: Not a doctor.")
            await self.close()
            return

        self.group_name = "doctors_sos_group"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ [SOSConsumer] Connected for Doctor: {user.username}")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        print(f"[SOSConsumer] Disconnected for: {username}")

    async def sos_notification(self, event):
        message_data = event['message']
        await self.send(text_data=json.dumps({
            'type': 'sos_notification',
            'sos_event_id': message_data.get('sos_event_id')
        }))


# --- 2. For Caretakers (Private Alerts) ---
class CaretakerConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket connections for individual caretakers
    to receive alerts specific to their hostel.
    """
    
    async def connect(self):
        user = self.scope["user"]
        
        print(f"--- [CaretakerConsumer] Connection Attempt ---")
        print(f"User: {user}")
        print(f"Is Authenticated: {user.is_authenticated}")
        if hasattr(user, 'role'):
            print(f"User Role: {user.role}")
        
        # This now correctly checks for 'caretaker'
        if not user.is_authenticated or user.role != 'caretaker':
            print(f"!!! [CaretakerConsumer] REJECTING: Not a caretaker. Role: {user.role}")
            await self.close()
            return
            
        self.group_name = f"caretaker_{user.id}" # Private group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ [CaretakerConsumer] Connected for: {user.username} in group {self.group_name}")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        print(f"[CaretakerConsumer] Disconnected for: {username}")

    async def sos_notification(self, event):
        message_data = event['message']
        await self.send(text_data=json.dumps({
            'type': 'sos_notification',
            'message': message_data
        }))


# --- 3. For WebRTC (Private Signaling) ---
class CallConsumer(AsyncWebsocketConsumer):
    """
    This replaces your standalone signaling_server.py
    It handles the WebRTC signaling between two specific peers.
    """
    
    async def connect(self):
        user = self.scope["user"]
        
        print(f"--- [CallConsumer] Connection Attempt ---")
        print(f"User: {user}")

        if not user.is_authenticated:
            print("!!! [CallConsumer] REJECTING: Not authenticated.")
            await self.close()
            return

        self.user_id = user.username # Use username as the WebRTC ID
        self.group_name = f"call_{self.user_id}" # Private group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ [CallConsumer] Connected for user: {self.user_id}")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        print(f"[CallConsumer] Disconnected for: {username}")

    async def receive(self, text_data):
        """
        Receives a message from one peer and relays it to the target peer.
        """
        data = json.loads(text_data)
        target_user_id = data.get('target') # Username of the person to call

        if not target_user_id:
            print("!!! [CallConsumer] Received message without a target.")
            return

        target_group = f"call_{target_user_id}"
        data['from'] = self.user_id # Add the sender's ID

        print(f"[CallConsumer] Relaying '{data.get('type')}' from {self.user_id} to {target_user_id}")

        await self.channel_layer.group_send(
            target_group,
            {
                'type': 'call_message', # This will call the 'call_message' function
                'message': data
            }
        )

    async def call_message(self, event):
        """
        Sends the relayed message down to the client's WebSocket.
        """
        await self.send(text_data=json.dumps(event['message']))

