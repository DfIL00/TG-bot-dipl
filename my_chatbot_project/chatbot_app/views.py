import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatSession, Message  # Удален неиспользуемый импорт BotResponseTemplate
import random
from bot_logic import generate_bot_response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request, session_id):
    """Получение истории чата"""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Сессия не найдена'}, status=404)

    messages = Message.objects.filter(session=session).order_by('timestamp')
    history = [
        {'text': msg.text, 'is_bot': msg.is_bot, 'timestamp': msg.timestamp}
        for msg in messages
    ]
    return Response({'history': history})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_session(request):
    session = ChatSession.objects.create(user=request.user)
    return Response({
        'session_id': session.id,
        'started_at': session.started_at
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, session_id):
    """Отправляет сообщение в чат и получает ответ от бота."""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Сессия не найдена'}, status=404)

    text = request.data.get('text')
    if not text:
        return Response({'error': 'Текст сообщения не может быть пустым'}, status=400)

    # Сохраняем сообщение пользователя (переменная не используется явно)
    Message.objects.create(
        session=session,
        text=text,
        is_bot=False
    )

    # Генерируем ответ бота
    bot_response = generate_bot_response(text)

    # Сохраняем ответ бота
    bot_message = Message.objects.create(
        session=session,
        text=bot_response,
        is_bot=True
    )

    return Response({
        'bot_response': bot_response,
        'message_id': bot_message.id
    })

def generate_bot_response(text):
    """Логика генерации ответа бота"""
    triggers = {
        'привет': ["Здравствуйте!", "Привет! Как я могу помочь?"],
        'погода': ["Погодный сервис временно недоступен."]
    }
    text_lower = text.lower()

    for key in triggers:
        if key in text_lower:
            return random.choice(triggers[key])

    return "Я пока не умею отвечать на такие вопросы."

class RegisterAPI(generics.GenericAPIView):
    """API для регистрации пользователей."""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(generics.GenericAPIView):
    """API для входа в систему."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response({"error": "Invalid credentials"}, status=401)