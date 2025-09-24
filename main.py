import vk_api
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
import logging
import json
import os
import time
from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_CHANNEL_USERNAME,
    VK_API_TOKEN,
    VK_GROUP_ID,
    CHECK_INTERVAL_SECONDS
)

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Названия файлов ---
STATE_FILE = 'state.json'
SESSION_NAME = 'telegram_session'

def load_last_message_id() -> int:
    # (Код этой функции остается без изменений)
    if not os.path.exists(STATE_FILE):
        logging.info("Файл состояния не найден. Начинаем с самых новых постов.")
        return 0
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return int(state.get('last_message_id', 0))
    except (json.JSONDecodeError, ValueError, FileNotFoundError):
        logging.warning("Ошибка чтения файла состояния. Начинаем с 0.")
        return 0

def save_last_message_id(message_id: int):
    # (Код этой функции остается без изменений)
    with open(STATE_FILE, 'w') as f:
        json.dump({'last_message_id': message_id}, f)
    logging.info(f"Состояние обновлено. Последний ID сообщения: {message_id}")

def process_new_messages(client, vk):
    """Основной цикл обработки и публикации сообщений."""
    last_known_id = load_last_message_id()
    logging.info(f"Проверка новых сообщений с ID > {last_known_id}...")

    new_messages = []
    try:
        channel = client.get_entity(TELEGRAM_CHANNEL_USERNAME)
        for message in client.iter_messages(channel, min_id=last_known_id):
            if message.text:
                new_messages.append(message)
    except Exception as e:
        logging.error(f"Ошибка при получении сообщений из Telegram: {e}", exc_info=False)
        return # Пропускаем этот цикл, попробуем в следующий раз

    if not new_messages:
        logging.info("Новых сообщений не найдено.")
        return

    new_messages.reverse()
    logging.info(f"Найдено {len(new_messages)} новых сообщений для публикации.")

    channel_title = channel.title

    for message in new_messages:
        try:
            post_text = message.text
            post_text += f"\n\n—\nОпубликовано из Telegram-канала «{channel_title}»"
            vk.wall.post(owner_id=-VK_GROUP_ID, from_group=1, message=post_text)
            logging.info(f"Сообщение {message.id} успешно опубликовано в VK.")
            save_last_message_id(message.id)
            time.sleep(2) # Небольшая задержка между постами, чтобы не превышать лимиты VK API
        except Exception as e:
            logging.error(f"Не удалось опубликовать сообщение {message.id} в VK: {e}", exc_info=False)
            logging.error("Прекращение цикла публикации, чтобы избежать рассинхронизации. Попробуем снова через интервал.")
            return

def main():
    """Главная функция-демон."""
    logging.info("--- Запуск сервиса Telegram to VK Poster ---")

    # Инициализация клиентов вне цикла
    try:
        vk_session = vk_api.VkApi(token=VK_API_TOKEN)
        vk = vk_session.get_api()
        logging.info("VK API успешно инициализирован.")

        client = TelegramClient(SESSION_NAME, int(TELEGRAM_API_ID), TELEGRAM_API_HASH)
        logging.info("Клиент Telegram инициализирован.")
    except Exception as e:
        logging.critical(f"Критическая ошибка при инициализации клиентов: {e}", exc_info=True)
        return

    while True:
        try:
            if not client.is_connected():
                client.connect()

            if not client.is_user_authorized():
                logging.critical("Пользователь не авторизован! Запустите скрипт один раз вручную для входа.")
                break

            process_new_messages(client, vk)

        except Exception as e:
            logging.error(f"Произошла необработанная ошибка в главном цикле: {e}", exc_info=True)

        logging.info(f"Пауза на {CHECK_INTERVAL_SECONDS} секунд...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
