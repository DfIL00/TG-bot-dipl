from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken, TokenError
import json
from channels.middleware import BaseMiddleware

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        # Логика проверки токена
        return await super().__call__(scope, receive, send)



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        query_params = dict(param.split('=') for param in query_string.split('&') if '=' in param)

        token = query_params.get('token', [''])[0]
        if not token:
            await self.close()
            return

        try:
            user_id = await self.get_user_id(token)
            if not user_id:
                await self.close()
                return
        except TokenError as e:
            await self.close()
            return

        await self.accept()

    @database_sync_to_async
    def get_user_id(self, token):
        try:
            return AccessToken(token).get('user_id')
        except TokenError:
            return None

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message = data.get('message', '')

            await self.send(text_data=json.dumps({
                'message': 'Ответ от бота',
                'original_message': message
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))

    async def disconnect(self, close_code):
        pass