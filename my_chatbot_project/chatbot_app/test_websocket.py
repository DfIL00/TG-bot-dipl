# test_websocket.py

from channels.testing import WebsocketCommunicator
from chatbot_project.routing import application


async def test_chat_consumer():
    communicator = WebsocketCommunicator(application, f"/ws/chat/123/")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({"message": "Привет"})
    response = await communicator.receive_json_from()
    assert "Бот: Получил ваше сообщение" in response['message']