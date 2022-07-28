import asyncio
import threading

from fastapi.testclient import TestClient

from main import app

chat_room_id = None
user_id = None
client = TestClient(app)


def threaded_listeners(ch_id):
    """Thread listener function"""
    with client.websocket_connect(f"/get_messages/{ch_id}") as websocket:
        while True:
            received = websocket.receive_json()
            messages = received.get("messages", [])
            if len(messages):
                print(received)
            else:
                body = received.get("message", None)
                if body:
                    body = received["message"]["body"]
                    print(f"Thread :{threading.get_ident()} Reporting Live = ", body)
                    if "e=mc2" in body:
                        break


async def main():
    """Main client testing code"""
    with client.websocket_connect("/sign_up") as websocket:
        message = {"name": "Gaurav Panta"}
        print(dir(websocket))
        websocket.send_json(message)
        received = websocket.receive_json()
        print(received)
        chat_room_id = received["chat_room"]["chat_room_id"]
        user_id = received["user"]["user_id"]

    t1 = threading.Thread(target=threaded_listeners, args=(chat_room_id,))
    t2 = threading.Thread(target=threaded_listeners, args=(chat_room_id,))
    t1.start()
    t2.start()

    with client.websocket_connect(f"/send_message/{chat_room_id}") as websocket:
        for test_bodies in ["Hey It's a me, Mario!", "Broken! It is!", "e=mc2"]:
            if test_bodies == "e=mc2":
                user_id = "big-papers-alcoholic"
            message = {"body": test_bodies, "user_id": user_id}
            websocket.send_json(message)

    t1.join()
    t2.join()


if __name__ == "__main__":
    asyncio.run(main())
