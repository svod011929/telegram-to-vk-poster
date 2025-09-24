import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# --- Конфигурация Telegram ---
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_CHANNEL_USERNAME = os.getenv("TELEGRAM_CHANNEL_USERNAME")

# --- Конфигурация ВКонтакте ---
VK_API_TOKEN = os.getenv("VK_API_TOKEN")
# ID группы VK должен быть числом
try:
    VK_GROUP_ID = int(os.getenv("VK_GROUP_ID"))
except (ValueError, TypeError):
    print("Ошибка: VK_GROUP_ID должен быть числом. Проверьте ваш .env файл.")
    exit(1)


# --- Проверка наличия всех переменных ---
def validate_config():
    """Проверяет, что все необходимые переменные окружения заданы."""
    missing_vars = []
    required_vars = {
        "TELEGRAM_API_ID": TELEGRAM_API_ID,
        "TELEGRAM_API_HASH": TELEGRAM_API_HASH,
        "TELEGRAM_CHANNEL_USERNAME": TELEGRAM_CHANNEL_USERNAME,
        "VK_API_TOKEN": VK_API_TOKEN,
        "VK_GROUP_ID": os.getenv("VK_GROUP_ID"), # Проверяем исходную строку
    }

    for var_name, value in required_vars.items():
        if not value:
            missing_vars.append(var_name)

    if missing_vars:
        print(f"Ошибка: Отсутствуют следующие переменные окружения в файле .env: {', '.join(missing_vars)}")
        print("Пожалуйста, создайте и заполните файл .env перед запуском.")
        exit(1)

# Вызываем проверку при импорте модуля
validate_config()
