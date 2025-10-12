# Создаем .env.example
env_example = """# Telegram API конфигурация
# Получить можно на https://my.telegram.org/apps
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here

# Telegram канал для мониторинга (например: @channel_name или https://t.me/channel_name)
TELEGRAM_CHANNEL=@your_channel_name

# VK API конфигурация
# Токен для работы с группой ВКонтакте
VK_ACCESS_TOKEN=your_vk_access_token_here

# ID группы ВКонтакте (только цифры, без знака минус)
VK_GROUP_ID=123456789

# Интервал проверки новых сообщений в секундах (по умолчанию 300 = 5 минут)
CHECK_INTERVAL=300

# Подпись к каждому посту (необязательно)
POST_SIGNATURE=#автопост

# Уровень логирования (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Имя файла сессии Telegram (по умолчанию telegram_to_vk_session)
SESSION_NAME=telegram_to_vk_session
"""

with open(".env.example", "w", encoding="utf-8") as f:
    f.write(env_example)

print("✅ Создан файл .env.example")