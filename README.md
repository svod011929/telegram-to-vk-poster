# 🚀 Telegram to VK Poster
Автоматический постер сообщений из Telegram-канала в группу ВКонтакте на Python.

![GitHub top language](https://img.shields.io/github/languages/top/svod011929/telegram-to-vk-poster?style=for-the-badge&color=5865F2)
![GitHub Repo stars](https://img.shields.io/github/stars/svod011929/telegram-to-vk-poster?style=for-the-badge&color=f9a825)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/svod011929/telegram-to-vk-poster?style=for-the-badge&color=4caf50&label=commits)
![GitHub last commit](https://img.shields.io/github/last-commit/svod011929/telegram-to-vk-poster?style=for-the-badge&color=lightgrey)

<p align="center">
  <img src="https://media.giphy.com/media/tKxvu25nKSAeI/giphy.gif" width="400" alt="Social Media Animation">
</p>

## 🔍 Описание
**Telegram to VK Poster** — это простой и надежный Python-скрипт для автоматического перепоста сообщений из публичного Telegram-канала в группу ВКонтакте.

Скрипт разработан для работы в качестве системного сервиса (`systemd`) на Linux, что обеспечивает стабильность, автоматический перезапуск и работу в фоновом режиме 24/7.

## ✨ Ключевые функции
- **🛡️ Отказоустойчивость**: Скрипт запоминает ID последнего поста, что исключает повторы.
- **🔄 Постоянная работа**: Работает как демон, проверяя новые посты через настраиваемый интервал.
- **⚙️ Простая настройка**: Вся конфигурация хранится в `.env` файле.
- **✍️ Кастомизация**: Легко добавляемая подпись к каждому посту.
- **📝 Логирование**: Подробные логи работы сервиса для удобного отслеживания.

---

## ⚙️ Установка и настройка на сервере (Linux)

### 1. Клонирование и настройка проекта
```bash
# Клонируем репозиторий
git clone https://github.com/svod011929/telegram-to-vk-poster.git
cd telegram-to-vk-poster

# Создаем и активируем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

```

### 2. Настройка конфигурации
Создайте файл `.env` и заполните его вашими данными.
<details>
<summary><strong>📄 Нажмите, чтобы увидеть пример .env файла</strong></summary>

```ini
#============ TELEGRAM ============
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_CHANNEL_USERNAME=my_channel_name

#============ VKONTAKTE ============
VK_API_TOKEN=vk1.a.very_long_and_secret_vk_api_token
VK_GROUP_ID=123456789

#============ НАСТРОЙКИ СЕРВИСА ============
# Интервал проверки новых постов в секундах (например, 300 = 5 минут)
CHECK_INTERVAL_SECONDS=300

```
</details>

### 3. Первая авторизация в Telegram
**Это обязательный шаг!** Запустите скрипт один раз вручную, чтобы войти в Telegram и создать файл сессии.
```bash
python main.py

```
Вам нужно будет ввести номер телефона, код и, возможно, пароль. После успешного входа и первой проверки постов остановите скрипт (`Ctrl+C`). В папке появится файл `telegram_session.session`.

---

## ⚡ Запуск в качестве сервиса (systemd)

### 1. Создание service-файла
Создайте файл конфигурации для `systemd`:
```bash
sudo nano /etc/systemd/system/telegram-poster.service

```
Скопируйте в него текст ниже. **Не забудьте** заменить `your_username` и путь в `WorkingDirectory`/`ExecStart` на ваши!

```ini
[Unit]
Description=Telegram to VK Poster Service
After=network-online.target

[Service]
# Имя пользователя, от которого запускается скрипт
User=your_username
# Группа пользователя
Group=your_username

# АБСОЛЮТНЫЙ путь к папке проекта
WorkingDirectory=/home/your_username/telegram-to-vk-poster

# АБСОЛЮТНЫЙ путь к Python в виртуальном окружении
ExecStart=/home/your_username/telegram-to-vk-poster/venv/bin/python main.py

# Политика перезапуска
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target

```
> **Подсказка:** Чтобы узнать полный путь к папке, перейдите в нее и выполните команду `pwd`.

### 2. Управление сервисом
После сохранения файла выполните команды:
```bash
# Перезагрузить конфигурацию systemd
sudo systemctl daemon-reload

# Включить автозапуск сервиса при старте системы
sudo systemctl enable telegram-poster.service

# Запустить сервис немедленно
sudo systemctl start telegram-poster.service

```

### 3. Проверка статуса и логов
```bash
# Проверить, работает ли сервис
sudo systemctl status telegram-poster.service

# Смотреть логи в реальном времени (выйти через Ctrl+C)
sudo journalctl -u telegram-poster.service -f

```

---

## 🌟 Поддержка и автор

<div align="center">

### ✨ Свяжитесь со мной
Автор проекта: [svod011929](https://github.com/svod011929/)

[![Telegram Contact](https://img.shields.io/badge/Telegram-@KodoDrive-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/KodoDrive)
[![Email](https://img.shields.io/badge/Email-bussines@kododrive--devl.ru-7B68EE?style=for-the-badge&logo=gmail&logoColor=white)](mailto:bussines@kododrive-devl.ru)

</div>
