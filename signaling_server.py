import asyncio
import websockets
import json

connected_users = {}

async def handler(websocket):
    user_id = None
    try:
        auth_message = await websocket.recv()
        auth_data = json.loads(auth_message)
        user_id = auth_data.get('user_id')

        if not user_id:
            await websocket.close(code=4000, reason="Missing user_id")
            print("[SignalingServer] Connection rejected: no user_id.")
            return

        connected_users[user_id] = websocket
        print(f"[SignalingServer] ✅ User '{user_id}' connected.")

        async for message in websocket:
            data = json.loads(message)
            target_user_id = data.get('target')
            msg_type = data.get('type')

            if not target_user_id:
                print(f"[SignalingServer] ⚠️ No target in message from {user_id}")
                continue

            target_ws = connected_users.get(target_user_id)
            if target_ws:
                data['from'] = user_id
                await target_ws.send(json.dumps(data))
                print(f"[SignalingServer] 🔁 Relayed '{msg_type}' from {user_id} → {target_user_id}")
            else:
                print(f"[SignalingServer] ⚠️ Target '{target_user_id}' not connected.")
    except Exception as e:
        print(f"[SignalingServer] ❗ Error: {e}")
    finally:
        if user_id in connected_users:
            del connected_users[user_id]
            print(f"[SignalingServer] 🧹 Cleaned up '{user_id}'.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 Signaling server started on ws://<your-ip>:8765")
        print("💡 Replace <your-ip> with your local IPv4 (e.g., ws://192.168.29.196:8765)")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
