# Telegram to VK Poster

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Systemd](https://img.shields.io/badge/systemd-compatible-orange.svg)](https://systemd.io/)

**Telegram to VK Poster** — это простой и надёжный скрипт на Python для автоматического репоста сообщений из общедоступного Telegram-канала в группу ВКонтакте.

Скрипт разработан для работы в качестве системного сервиса (systemd) в Linux, что обеспечивает стабильность, автоматический перезапуск и работу в фоновом режиме 24/7.

## ✨ Ключевые функции

- 🛡️ **Отказоустойчивость**: скрипт запоминает идентификатор последнего поста, что исключает повторы
- 🔄 **Постоянная работа**: работает как демон, проверяя наличие новых постов через настраиваемый интервал
- ⚙️ **Простая настройка**: вся конфигурация хранится в .env файле
- ✍️ **Настройка подписи**: легко добавляемая подпись к каждому посту
- 📝 **Логирование**: подробные логи работы сервиса для удобного отслеживания
- 📸 **Поддержка медиа**: автоматическая загрузка и публикация изображений
- 🔒 **Безопасность**: работа под отдельным пользователем с ограниченными правами

## 📋 Требования

- **Операционная система**: Linux с systemd
- **Python**: версия 3.8 или выше
- **Права**: root доступ для установки системного сервиса

## 🚀 Быстрая установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/svod011929/telegram-to-vk-poster.git
cd telegram-to-vk-poster
```

### 2. Запуск автоматической установки

```bash
chmod +x install.sh
sudo ./install.sh
```

### 3. Настройка конфигурации

```bash
# Копирование примера конфигурации
sudo cp /opt/telegram-to-vk-poster/.env.example /opt/telegram-to-vk-poster/.env

# Редактирование конфигурации
sudo nano /opt/telegram-to-vk-poster/.env
```

### 4. Настройка переменных окружения

Отредактируйте файл `.env` и укажите необходимые параметры:

```env
# Telegram API конфигурация
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_CHANNEL=@your_channel_name

# VK API конфигурация  
VK_ACCESS_TOKEN=your_vk_access_token_here
VK_GROUP_ID=123456789

# Дополнительные настройки
CHECK_INTERVAL=300
POST_SIGNATURE=#автопост
LOG_LEVEL=INFO
```

### 5. Запуск сервиса

```bash
# Включение автозапуска
sudo systemctl enable telegram-to-vk-poster

# Запуск сервиса
sudo systemctl start telegram-to-vk-poster

# Проверка статуса
sudo systemctl status telegram-to-vk-poster
```

## 🔧 Подробная настройка

### Получение Telegram API ключей

1. Перейдите на [my.telegram.org](https://my.telegram.org/apps)
2. Войдите в свой аккаунт Telegram
3. Создайте новое приложение
4. Скопируйте `api_id` и `api_hash`

### Получение VK Access Token

1. Перейдите в [настройки VK API](https://vk.com/apps?act=manage)
2. Создайте Standalone-приложение
3. Получите токен доступа с правами на публикацию в группе
4. Скопируйте ID группы (только цифры, без знака минус)

### Настройка Telegram канала

- Канал должен быть **публичным**
- Укажите username канала в формате `@channel_name`
- Или используйте прямую ссылку: `https://t.me/channel_name`

### Первый запуск

При первом запуске скрипт запросит номер телефона и код подтверждения для авторизации в Telegram API. Это необходимо только один раз.

```bash
# Запуск в интерактивном режиме для первой авторизации
sudo -u telegram-vk-poster /opt/telegram-to-vk-poster/venv/bin/python /opt/telegram-to-vk-poster/telegram-to-vk-poster.py
```

## 📊 Управление сервисом

### Основные команды

```bash
# Запуск сервиса
sudo systemctl start telegram-to-vk-poster

# Остановка сервиса  
sudo systemctl stop telegram-to-vk-poster

# Перезапуск сервиса
sudo systemctl restart telegram-to-vk-poster

# Проверка статуса
sudo systemctl status telegram-to-vk-poster

# Включение автозапуска
sudo systemctl enable telegram-to-vk-poster

# Отключение автозапуска
sudo systemctl disable telegram-to-vk-poster
```

### Просмотр логов

```bash
# Просмотр логов в реальном времени
sudo journalctl -u telegram-to-vk-poster -f

# Просмотр последних логов
sudo journalctl -u telegram-to-vk-poster --lines=100

# Просмотр логов за сегодня
sudo journalctl -u telegram-to-vk-poster --since=today
```

### Файлы логов

- **Системные логи**: `journalctl -u telegram-to-vk-poster`
- **Файловые логи**: `/var/log/telegram-to-vk-poster/service.log`
- **Файл состояния**: `/var/lib/telegram-to-vk-poster/last_post.json`

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательная | По умолчанию |
|------------|----------|--------------|--------------|
| `TELEGRAM_API_ID` | API ID от Telegram | ✅ | - |
| `TELEGRAM_API_HASH` | API Hash от Telegram | ✅ | - |
| `TELEGRAM_CHANNEL` | Имя канала для мониторинга | ✅ | - |
| `VK_ACCESS_TOKEN` | Токен доступа VK API | ✅ | - |
| `VK_GROUP_ID` | ID группы ВКонтакте | ✅ | - |
| `CHECK_INTERVAL` | Интервал проверки (секунды) | ❌ | 300 |
| `POST_SIGNATURE` | Подпись к постам | ❌ | "" |
| `LOG_LEVEL` | Уровень логирования | ❌ | INFO |
| `SESSION_NAME` | Имя файла сессии | ❌ | telegram_to_vk_session |

### Структура проекта

```
/opt/telegram-to-vk-poster/
├── telegram-to-vk-poster.py    # Основной скрипт
├── requirements.txt             # Зависимости Python
├── .env                        # Конфигурация (создается при установке)
├── venv/                       # Виртуальное окружение Python
└── telegram_to_vk_session.session # Файл сессии Telegram

/var/log/telegram-to-vk-poster/
└── service.log                 # Логи сервиса

/var/lib/telegram-to-vk-poster/
└── last_post.json             # Состояние последнего поста
```

## 🔒 Безопасность

### Права доступа

Сервис работает под отдельным пользователем `telegram-vk-poster` с минимальными правами:

- **NoNewPrivileges**: запрет на повышение привилегий
- **PrivateTmp**: изолированная временная директория
- **ProtectSystem**: защита системных файлов
- **ProtectHome**: защита домашних директорий

### Ограничения ресурсов

- **Память**: максимум 512 МБ
- **CPU**: максимум 50% одного ядра
- **Файлы**: максимум 65536 дескрипторов

### Рекомендации

1. Регулярно обновляйте зависимости: `pip install --upgrade -r requirements.txt`
2. Мониторьте логи на предмет ошибок и подозрительной активности
3. Используйте отдельные токены для каждого проекта
4. Не публикуйте конфигурационные файлы в публичных репозиториях

## 🛠️ Разработка

### Локальная разработка

```bash
# Клонирование репозитория
git clone https://github.com/svod011929/telegram-to-vk-poster.git
cd telegram-to-vk-poster

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Копирование конфигурации
cp .env.example .env
# Отредактируйте .env файл

# Запуск в режиме разработки
python telegram-to-vk-poster.py
```

### Структура кода

- `TelegramToVKPoster` - основной класс приложения
- `LastPostTracker` - класс для отслеживания состояния
- `setup_logging()` - настройка системы логирования
- `main()` - точка входа в приложение

### Тестирование

```bash
# Проверка синтаксиса
python -m py_compile telegram-to-vk-poster.py

# Запуск с отладочным уровнем логирования
LOG_LEVEL=DEBUG python telegram-to-vk-poster.py
```

## 🐛 Устранение неполадок

### Типичные проблемы

**1. Ошибка авторизации Telegram**
```
Решение: Удалите файл сессии и перезапустите сервис для повторной авторизации
sudo rm /opt/telegram-to-vk-poster/telegram_to_vk_session.session
sudo systemctl restart telegram-to-vk-poster
```

**2. Ошибка доступа к VK API**
```
Решение: Проверьте права токена и корректность ID группы
```

**3. Сервис не запускается**
```
Решение: Проверьте логи и конфигурацию
sudo journalctl -u telegram-to-vk-poster --lines=50
```

**4. Нет новых постов**
```
Решение: Проверьте доступность канала и корректность имени
```

### Полезные команды диагностики

```bash
# Проверка конфигурации
sudo cat /opt/telegram-to-vk-poster/.env

# Проверка состояния файлов
sudo ls -la /var/lib/telegram-to-vk-poster/

# Тест подключения к VK API
curl "https://api.vk.com/method/groups.getById?group_id=YOUR_GROUP_ID&access_token=YOUR_TOKEN&v=5.131"

# Проверка процессов
ps aux | grep telegram-to-vk-poster
```

## 📈 Мониторинг

### Метрики для отслеживания

- Время работы сервиса
- Количество обработанных сообщений
- Ошибки API запросов
- Использование памяти и CPU

### Интеграция с системами мониторинга

Сервис поддерживает стандартные инструменты мониторинга Linux:

- **systemd status** - базовая информация о состоянии
- **journald logs** - централизованное логирование
- **htop/top** - мониторинг ресурсов

## 🤝 Вклад в разработку

Мы приветствуем вклад в развитие проекта! 

### Как помочь проекту

1. **Форкните** репозиторий
2. **Создайте** ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. **Коммитьте** изменения (`git commit -m 'Add amazing feature'`)
4. **Отправьте** изменения в ветку (`git push origin feature/amazing-feature`)
5. **Откройте** Pull Request

### Разработческие соглашения

- Следуйте стилю кода PEP 8
- Документируйте новые функции
- Добавляйте тесты для нового функционала
- Обновляйте README при необходимости

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 🔗 Полезные ссылки

- [Telegram API Documentation](https://core.telegram.org/api)
- [VK API Documentation](https://dev.vk.com/method)
- [Systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Python Telegram Client - Telethon](https://github.com/LonamiWebs/Telethon)
- [VK API Python Library](https://github.com/python273/vk_api)

## 🙋‍♂️ Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [секцию устранения неполадок](#-устранение-неполадок)
2. Изучите [существующие issues](https://github.com/svod011929/telegram-to-vk-poster/issues)
3. Создайте [новый issue](https://github.com/svod011929/telegram-to-vk-poster/issues/new) с подробным описанием проблемы

---

⭐ Если этот проект оказался полезным, поставьте звездочку на GitHub!

**Автор**: [svod011929](https://github.com/svod011929)
