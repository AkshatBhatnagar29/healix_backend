import asyncio
import websockets
import json

# A dictionary to keep track of connected users and their WebSocket connections
connected_users = {}

async def handler(websocket, path):
    """
    Handles WebSocket connections and signaling messages.
    """
    user_id = None
    try:
        # The first message from the client should be an authentication message
        # with their user ID.
        auth_message = await websocket.recv()
        auth_data = json.loads(auth_message)
        user_id = auth_data['user_id']
        connected_users[user_id] = websocket
        print(f"User '{user_id}' connected.")

        # Listen for messages from this user
        async for message in websocket:
            data = json.loads(message)
            target_user_id = data.get('target')

            if target_user_id and target_user_id in connected_users:
                # This is a signaling message intended for another user.
                # We add the sender's ID and forward it.
                data['from'] = user_id
                target_websocket = connected_users[target_user_id]
                await target_websocket.send(json.dumps(data))
            else:
                print(f"Target user '{target_user_id}' not found or not specified.")

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection with user '{user_id}' closed.")
    finally:
        # When a user disconnects, remove them from our list
        if user_id and user_id in connected_users:
            del connected_users[user_id]
            print(f"User '{user_id}' disconnected.")

async def main():
    # Start the WebSocket server on port 8765
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Signaling server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
