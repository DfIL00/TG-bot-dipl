from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    create_chat_session,
    send_message,
    get_chat_history
)

urlpatterns = [

    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('create-session/', create_chat_session, name='create_session'),
    path('send-message/<int:session_id>/', send_message, name='send_message'),
    path('history/<int:session_id>/', get_chat_history, name='history'),
]