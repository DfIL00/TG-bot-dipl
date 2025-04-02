from django.test import TestCase
from .models import CustomUser, ChatSession

class ModelTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')

    def test_create_chat_session(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass123')
        session = ChatSession.objects.create(user=user)
        self.assertTrue(session.is_active)

# Create your tests here.
