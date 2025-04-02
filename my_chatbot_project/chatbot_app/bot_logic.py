from .models import BotResponseTemplate


def generate_bot_response(user_text):
    user_text_lower = user_text.lower()

    # Статичные ответы
    if any(word in user_text_lower for word in ['привет', 'здравствуй']):
        return "Привет! Чем могу помочь?"

    # Поиск шаблонов с точным совпадением триггерного слова
    template = BotResponseTemplate.objects.filter(
        trigger_word__iexact=user_text_lower
    ).order_by('-priority').first()

    return template.response_text if template else "Извините, я не понял ваш вопрос. Можете переформулировать?"