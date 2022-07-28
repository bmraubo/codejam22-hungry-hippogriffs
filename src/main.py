import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from sockets.connection_handler import ConnectionHandler
from sockets.response_factory import ResponseFactory
from src.db.db import DatabaseService
from src.sockets.connection_manager import ConnectionManager
from src.utils import (
    RandomIdGenerator,
    create_and_get_chatroom,
    create_and_get_message,
    create_and_get_user,
)

app = FastAPI()
random_generator = RandomIdGenerator()
# Instantiate DatabaseClient
db_service = DatabaseService()

response_fact_obj = ResponseFactory()

# Instantiate ConnectionManager # TODO: Fix this to set connection manager per chatroom
manager = ConnectionManager()


@app.websocket("/sign_up")
async def sign_up(websocket: WebSocket):
    """Signs Up New Users"""
    connection = ConnectionHandler(websocket)
    await connection.accept_socket_connection()
    request = await connection.get_request()
    # Create User Object
    user_obj = create_and_get_user(
        user_id=random_generator(), username=request.get("name")
    )
    chat_room_obj = create_and_get_chatroom(
        chat_room_id=random_generator(), user_id=user_obj.user_id
    )
    # Save User To DB
    user_obj = db_service.save_user(user_obj)
    # Save Chatroom to DB
    chat_room_obj = db_service.save_chat_room(chat_room_obj)
    response = response_fact_obj.generate_sign_up_response(
        True, user_obj, chat_room_obj
    )  # uses ResponseFactory to generate Response JSON from User Object
    await connection.send_response(response)


@app.websocket("/send_message/{chat_room_id}")
async def send_message(websocket: WebSocket, chat_room_id: str):
    """Sends Message to Given Chatroom"""
    connection = ConnectionHandler(websocket)
    await connection.accept_socket_connection()
    try:
        while True:
            request = await connection.get_request()
            body = request["body"]
            user_id = request["user_id"]
            # fetch chat room
            chat_room_obj = db_service.get_chat_room_by_id(chat_room_id=chat_room_id)
            # save user two when user two is empty
            if chat_room_obj.user_one != user_id and chat_room_obj.user_two is None:
                chat_room_obj.user_two = user_id
                chat_room_obj = db_service.save_chat_room(chat_room_obj)
            message_obj = create_and_get_message(
                chat_room_id=chat_room_id, user_id=user_id, body=body
            )
            message_obj = db_service.save_messaage(chat_room_obj, message_obj)
            response = ResponseFactory.generate_send_message_response(True, message_obj)
            await manager.broadcast(response)
    except WebSocketDisconnect:
        print("Websocket disconnect!")
        await manager.disconnect(connection)


@app.websocket("/get_messages/{chat_room_id}")
async def get_message(websocket: WebSocket, chat_room_id: str):
    """Gets All Messages Of Given Chatroom"""
    connection = ConnectionHandler(websocket)
    await connection.accept_socket_connection()
    manager.add_connection(connection)
    chat_room_obj = db_service.get_chat_room_by_id(chat_room_id=chat_room_id)
    messages = db_service.get_chat_room_messages(chat_room_obj)
    print()
    response = ResponseFactory.generate_get_messages_response(chat_room_obj, messages)
    await connection.send_response(response)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=4444, debug=True)
