#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram to VK Poster - простой и надёжный скрипт для автоматического репоста
сообщений из общедоступного Telegram-канала в группу ВКонтакте.

Разработан для работы в качестве системного сервиса (systemd) в Linux.
"""

import os
import time
import logging
import asyncio
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

# Основные библиотеки
import vk_api
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dotenv import load_dotenv

# Настройка логирования
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Настройка системы логирования"""
    log_dir = Path("/var/log/telegram-to-vk-poster")
    log_dir.mkdir(exist_ok=True)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Настройка файлового логирования
    file_handler = logging.FileHandler(log_dir / "service.log")
    file_handler.setFormatter(logging.Formatter(log_format))

    # Настройка консольного логирования  
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger("telegram-to-vk-poster")
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

class LastPostTracker:
    """Класс для отслеживания последнего обработанного поста"""

    def __init__(self, state_file: str = "/var/lib/telegram-to-vk-poster/last_post.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def get_last_post_id(self) -> Optional[int]:
        """Получить ID последнего обработанного поста"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_post_id')
        except Exception as e:
            logging.error(f"Ошибка при чтении файла состояния: {e}")
        return None

    def save_last_post_id(self, post_id: int) -> bool:
        """Сохранить ID последнего обработанного поста"""
        try:
            data = {
                'last_post_id': post_id,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении файла состояния: {e}")
            return False

class TelegramToVKPoster:
    """Основной класс для репоста из Telegram в VK"""

    def __init__(self):
        # Загрузка переменных окружения
        load_dotenv()

        # Настройка логирования
        self.logger = setup_logging(os.getenv("LOG_LEVEL", "INFO"))

        # Конфигурация
        self.config = self._load_config()

        # Инициализация компонентов
        self.post_tracker = LastPostTracker()
        self.telegram_client = None
        self.vk_session = None
        self.vk_api = None

        self.logger.info("Инициализация TelegramToVKPoster завершена")

    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из переменных окружения"""
        required_vars = [
            "TELEGRAM_API_ID", "TELEGRAM_API_HASH", "TELEGRAM_CHANNEL",
            "VK_ACCESS_TOKEN", "VK_GROUP_ID"
        ]

        config = {}
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"Переменная окружения {var} не установлена")
            config[var.lower()] = value

        # Дополнительные настройки
        config.update({
            "check_interval": int(os.getenv("CHECK_INTERVAL", "300")),  # 5 минут
            "post_signature": os.getenv("POST_SIGNATURE", ""),
            "session_name": os.getenv("SESSION_NAME", "telegram_to_vk_session")
        })

        return config

    async def init_telegram_client(self):
        """Инициализация Telegram клиента"""
        try:
            self.telegram_client = TelegramClient(
                self.config["session_name"],
                int(self.config["telegram_api_id"]),
                self.config["telegram_api_hash"]
            )

            await self.telegram_client.start()
            self.logger.info("Telegram клиент успешно инициализирован")

        except Exception as e:
            self.logger.error(f"Ошибка инициализации Telegram клиента: {e}")
            raise

    def init_vk_session(self):
        """Инициализация VK сессии"""
        try:
            self.vk_session = vk_api.VkApi(token=self.config["vk_access_token"])
            self.vk_api = self.vk_session.get_api()

            # Проверка доступа
            info = self.vk_api.groups.getById(group_id=self.config["vk_group_id"])
            self.logger.info(f"VK API успешно инициализирован для группы: {info[0]['name']}")

        except Exception as e:
            self.logger.error(f"Ошибка инициализации VK API: {e}")
            raise

    async def get_new_messages(self):
        """Получение новых сообщений из Telegram канала"""
        try:
            last_post_id = self.post_tracker.get_last_post_id()
            messages = []

            async for message in self.telegram_client.iter_messages(
                self.config["telegram_channel"],
                limit=50
            ):
                if last_post_id and message.id <= last_post_id:
                    break

                if message.text or message.media:
                    messages.append(message)

            # Сортировка по возрастанию ID (от старого к новому)
            messages.reverse()

            self.logger.info(f"Получено {len(messages)} новых сообщений")
            return messages

        except Exception as e:
            self.logger.error(f"Ошибка получения сообщений из Telegram: {e}")
            return []

    def format_message(self, message) -> str:
        """Форматирование сообщения для VK"""
        text = message.text or ""

        # Добавление подписи если настроена
        if self.config["post_signature"]:
            text += f"\n\n{self.config['post_signature']}"

        return text

    async def download_media(self, message) -> Optional[str]:
        """Скачивание медиафайлов из сообщения"""
        if not message.media:
            return None

        try:
            media_dir = Path("/tmp/telegram-to-vk-media")
            media_dir.mkdir(exist_ok=True)

            file_path = await self.telegram_client.download_media(message, media_dir)
            return str(file_path) if file_path else None

        except Exception as e:
            self.logger.error(f"Ошибка скачивания медиафайла: {e}")
            return None

    def upload_photo_to_vk(self, photo_path: str) -> Optional[str]:
        """Загрузка фотографии в VK"""
        try:
            upload = vk_api.VkUpload(self.vk_session)

            # Загрузка фото на стену группы
            photo = upload.photo_wall(
                photos=photo_path,
                group_id=int(self.config["vk_group_id"])
            )

            if photo:
                attachment = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
                self.logger.info(f"Фото успешно загружено: {attachment}")
                return attachment

        except Exception as e:
            self.logger.error(f"Ошибка загрузки фото в VK: {e}")

        return None

    def post_to_vk(self, text: str, attachments: str = "") -> bool:
        """Публикация поста в VK"""
        try:
            result = self.vk_api.wall.post(
                owner_id=f"-{self.config['vk_group_id']}",
                message=text,
                attachments=attachments,
                from_group=1
            )

            if result.get('post_id'):
                self.logger.info(f"Пост успешно опубликован в VK: {result['post_id']}")
                return True
            else:
                self.logger.error(f"Ошибка публикации поста в VK: {result}")
                return False

        except Exception as e:
            self.logger.error(f"Ошибка публикации в VK: {e}")
            return False

    async def process_message(self, message) -> bool:
        """Обработка одного сообщения"""
        try:
            self.logger.info(f"Обработка сообщения ID: {message.id}")

            # Форматирование текста
            formatted_text = self.format_message(message)

            # Обработка медиафайлов
            attachments = ""
            if message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    media_path = await self.download_media(message)
                    if media_path:
                        attachment = self.upload_photo_to_vk(media_path)
                        if attachment:
                            attachments = attachment

                        # Удаление временного файла
                        try:
                            os.unlink(media_path)
                        except:
                            pass

            # Публикация в VK
            if self.post_to_vk(formatted_text, attachments):
                # Сохранение ID последнего обработанного поста
                self.post_tracker.save_last_post_id(message.id)
                return True

            return False

        except Exception as e:
            self.logger.error(f"Ошибка обработки сообщения {message.id}: {e}")
            return False

    async def run_check_cycle(self):
        """Выполнение одного цикла проверки новых сообщений"""
        try:
            messages = await self.get_new_messages()

            for message in messages:
                success = await self.process_message(message)
                if success:
                    # Небольшая задержка между постами
                    await asyncio.sleep(2)

        except Exception as e:
            self.logger.error(f"Ошибка в цикле проверки: {e}")

    async def run(self):
        """Основной цикл работы сервиса"""
        self.logger.info("Запуск службы Telegram to VK Poster")

        try:
            # Инициализация клиентов
            await self.init_telegram_client()
            self.init_vk_session()

            self.logger.info(f"Служба запущена. Интервал проверки: {self.config['check_interval']} секунд")

            while True:
                try:
                    await self.run_check_cycle()
                except Exception as e:
                    self.logger.error(f"Ошибка в основном цикле: {e}")

                # Ожидание до следующей проверки
                await asyncio.sleep(self.config["check_interval"])

        except KeyboardInterrupt:
            self.logger.info("Получен сигнал прерывания. Завершение работы...")
        except Exception as e:
            self.logger.error(f"Критическая ошибка: {e}")
            raise
        finally:
            if self.telegram_client:
                await self.telegram_client.disconnect()
            self.logger.info("Служба остановлена")

def main():
    """Точка входа в приложение"""
    try:
        poster = TelegramToVKPoster()
        asyncio.run(poster.run())
    except Exception as e:
        logging.error(f"Критическая ошибка запуска: {e}")
        exit(1)

if __name__ == "__main__":
    main()
