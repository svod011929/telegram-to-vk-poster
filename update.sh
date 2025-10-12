#!/bin/bash
# Скрипт обновления Telegram to VK Poster

set -e

echo "🔄 Обновление Telegram to VK Poster..."

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен с правами суперпользователя (sudo)" 
   exit 1
fi

INSTALL_DIR="/opt/telegram-to-vk-poster"
BACKUP_DIR="/tmp/telegram-to-vk-poster-backup-$(date +%Y%m%d-%H%M%S)"

# Проверка существования установки
if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ Telegram to VK Poster не установлен"
    exit 1
fi

# Остановка сервиса
echo "⏹️ Остановка сервиса..."
systemctl stop telegram-to-vk-poster

# Создание резервной копии конфигурации
echo "💾 Создание резервной копии..."
mkdir -p $BACKUP_DIR
cp $INSTALL_DIR/.env $BACKUP_DIR/ 2>/dev/null || true
cp $INSTALL_DIR/*.session $BACKUP_DIR/ 2>/dev/null || true

# Обновление кода
echo "📥 Загрузка обновлений..."
cd $INSTALL_DIR
git pull origin main || {
    echo "❌ Ошибка загрузки обновлений"
    exit 1
}

# Обновление зависимостей
echo "📦 Обновление зависимостей..."
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Восстановление конфигурации
echo "⚙️ Восстановление конфигурации..."
cp $BACKUP_DIR/.env $INSTALL_DIR/ 2>/dev/null || true
cp $BACKUP_DIR/*.session $INSTALL_DIR/ 2>/dev/null || true

# Настройка прав доступа
chown -R telegram-vk-poster:telegram-vk-poster $INSTALL_DIR

# Перезагрузка systemd (на случай изменений в service файле)
systemctl daemon-reload

# Запуск сервиса
echo "▶️ Запуск сервиса..."
systemctl start telegram-to-vk-poster

# Проверка статуса
sleep 3
if systemctl is-active --quiet telegram-to-vk-poster; then
    echo "✅ Обновление завершено успешно!"
    echo "📊 Статус сервиса:"
    systemctl status telegram-to-vk-poster --no-pager -l
else
    echo "❌ Ошибка запуска сервиса после обновления"
    echo "🔍 Проверьте логи: sudo journalctl -u telegram-to-vk-poster --lines=20"
    exit 1
fi

echo "🗂️ Резервная копия сохранена в: $BACKUP_DIR"
