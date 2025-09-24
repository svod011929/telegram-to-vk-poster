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
try:
    VK_GROUP_ID = int(os.getenv("VK_GROUP_ID", 0))
except ValueError:
    print("Ошибка: VK_GROUP_ID должен быть числом. Проверьте ваш .env файл.")
    exit(1)

# --- Конфигурация работы скрипта ---
# Интервал проверки новых сообщений в секундах (по умолчанию 5 минут)
try:
    CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", 300))
except ValueError:
    print("Ошибка: CHECK_INTERVAL_SECONDS должен быть числом. Используется значение по умолчанию (300).")
    CHECK_INTERVAL_SECONDS = 300


# --- Проверка наличия всех переменных ---
def validate_config():
    """Проверяет, что все необходимые переменные окружения заданы."""
    # (Код валидации остается без изменений...)
    missing_vars = []
    required_vars = {
        "TELEGRAM_API_ID": TELEGRAM_API_ID,
        "TELEGRAM_API_HASH": TELEGRAM_API_HASH,
        "TELEGRAM_CHANNEL_USERNAME": TELEGRAM_CHANNEL_USERNAME,
        "VK_API_TOKEN": VK_API_TOKEN,
        "VK_GROUP_ID": os.getenv("VK_GROUP_ID"),
    }

    for var_name, value in required_vars.items():
        if not value:
            missing_vars.append(var_name)

    if missing_vars:
        print(f"Ошибка: Отсутствуют переменные в .env: {', '.join(missing_vars)}")
        exit(1)
    if not VK_GROUP_ID:
        print("Ошибка: VK_GROUP_ID не может быть пустым или нулем.")
        exit(1)

validate_config()
