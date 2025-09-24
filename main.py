import vk_api
from telethon.sync import TelegramClient
import logging
import json
import os
from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_CHANNEL_USERNAME,
    VK_API_TOKEN,
    VK_GROUP_ID,
)

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Названия файлов ---
STATE_FILE = 'state.json'
SESSION_NAME = 'telegram_session'

# --- Функции для управления состоянием ---
def load_last_message_id() -> int:
    """Загружает ID последнего обработанного сообщения из файла state.json."""
    if not os.path.exists(STATE_FILE):
        logging.info("Файл состояния не найден. Будет создан новый. Начинаем с самых новых постов.")
        return 0
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return int(state.get('last_message_id', 0))
    except (json.JSONDecodeError, ValueError, FileNotFoundError):
        logging.warning("Ошибка чтения файла состояния. Начинаем с самых новых постов.", exc_info=True)
        return 0

def save_last_message_id(message_id: int):
    """Сохраняет ID последнего обработанного сообщения в state.json."""
    with open(STATE_FILE, 'w') as f:
        json.dump({'last_message_id': message_id}, f)
    logging.info(f"Состояние обновлено. Последний ID сообщения: {message_id}")

# --- Основная логика ---
def main():
    """Главная функция для выполнения переноса постов."""
    logging.info("--- Запуск скрипта ---")

    # Загружаем ID последнего обработанного поста
    last_known_id = load_last_message_id()
    logging.info(f"ID последнего известного сообщения: {last_known_id}")

    new_messages = []
    channel_title = TELEGRAM_CHANNEL_USERNAME # Значение по умолчанию
    try:
        # --- Подключение к Telegram ---
        logging.info("Подключение к Telegram...")
        with TelegramClient(SESSION_NAME, int(TELEGRAM_API_ID), TELEGRAM_API_HASH) as client:
            channel = client.get_entity(TELEGRAM_CHANNEL_USERNAME)
            channel_title = channel.title
            logging.info(f"Получение сообщений из канала: {channel.title}")

            # Получаем новые сообщения, начиная с последнего известного ID
            for message in client.iter_messages(channel, min_id=last_known_id):
                if message.text: # Обрабатываем только текстовые сообщения
                    new_messages.append(message)

        # Разворачиваем список, чтобы публиковать в хронологическом порядке
        if new_messages:
            new_messages.reverse()
            logging.info(f"Найдено {len(new_messages)} новых сообщений для публикации.")
        else:
            logging.info("Новых сообщений не найдено.")
            logging.info("--- Работа скрипта завершена ---")
            return

    except Exception as e:
        logging.error("Произошла ошибка при работе с Telegram.", exc_info=e)
        return

    # --- Подключение к ВКонтакте ---
    try:
        logging.info("Подключение к ВКонтакте...")
        vk_session = vk_api.VkApi(token=VK_API_TOKEN)
        vk = vk_session.get_api()
    except Exception as e:
        logging.error("Произошла ошибка при аутентификации в VK.", exc_info=e)
        return

    # --- Публикация в ВКонтакте ---
    for message in new_messages:
        try:
            # Формируем текст для поста
            post_text = message.text
            post_text += f"\n\n—\nОпубликовано из Telegram-канала «{channel_title}»"

            # Публикуем на стене группы (ID группы должен быть с минусом)
            vk.wall.post(owner_id=-VK_GROUP_ID, from_group=1, message=post_text)

            logging.info(f"Сообщение с ID {message.id} успешно опубликовано в VK.")

            # Сразу после успешной публикации обновляем состояние
            save_last_message_id(message.id)

        except Exception as e:
            logging.error(f"Не удалось опубликовать сообщение с ID {message.id} в VK.", exc_info=e)
            logging.error("Прекращение работы, чтобы избежать рассинхронизации. Пожалуйста, исправьте ошибку и запустите скрипт заново.")
            # Прерываем выполнение, чтобы не пропустить посты
            return

    logging.info("--- Работа скрипта успешно завершена ---")


if __name__ == "__main__":
    main()
