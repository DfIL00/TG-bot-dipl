# chatbot_project/settings/base.py
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Для трехуровневой структуры проекта

STATICFILES_DIRS = [
    BASE_DIR / "frontend/public",  # Правильный формат пути
]

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'}
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    }
}

ASGI_APPLICATION = "chatbot_project.asgi.application"