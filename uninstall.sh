#!/bin/bash
# Скрипт удаления Telegram to VK Poster

set -e

echo "🗑️ Удаление Telegram to VK Poster..."

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен с правами суперпользователя (sudo)" 
   exit 1
fi

# Определение переменных
INSTALL_DIR="/opt/telegram-to-vk-poster"
SERVICE_FILE="/etc/systemd/system/telegram-to-vk-poster.service"
LOG_DIR="/var/log/telegram-to-vk-poster"
DATA_DIR="/var/lib/telegram-to-vk-poster"

# Остановка и отключение сервиса
echo "⏹️ Остановка сервиса..."
systemctl stop telegram-to-vk-poster 2>/dev/null || true
systemctl disable telegram-to-vk-poster 2>/dev/null || true

# Удаление systemd service файла
echo "🗂️ Удаление service файла..."
rm -f $SERVICE_FILE

# Перезагрузка systemd
systemctl daemon-reload

# Удаление пользователя и директорий
echo "👤 Удаление пользователя и файлов..."
userdel telegram-vk-poster 2>/dev/null || true

# Удаление директорий (с подтверждением для данных)
read -p "❓ Удалить директорию с логами ($LOG_DIR)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf $LOG_DIR
    echo "✅ Логи удалены"
fi

read -p "❓ Удалить директорию с данными ($DATA_DIR)? [y/N]: " -n 1 -r  
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf $DATA_DIR
    echo "✅ Данные удалены"
fi

read -p "❓ Удалить директорию установки ($INSTALL_DIR)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf $INSTALL_DIR
    echo "✅ Файлы приложения удалены"
fi

# Очистка временных файлов
rm -rf /tmp/telegram-to-vk-media 2>/dev/null || true

echo "✅ Удаление завершено!"
echo "ℹ️ Если вы планируете переустановку, сохраните резервную копию .env файла"
