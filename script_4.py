# Создаем скрипт установки
install_script = """#!/bin/bash
# Скрипт установки Telegram to VK Poster

set -e

echo "🚀 Установка Telegram to VK Poster..."

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен с правами суперпользователя (sudo)" 
   exit 1
fi

# Определение директорий
INSTALL_DIR="/opt/telegram-to-vk-poster"
SERVICE_FILE="/etc/systemd/system/telegram-to-vk-poster.service"
LOG_DIR="/var/log/telegram-to-vk-poster"
DATA_DIR="/var/lib/telegram-to-vk-poster"

# Обновление системы
echo "📦 Обновление пакетов системы..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv git

# Создание пользователя для сервиса
echo "👤 Создание пользователя сервиса..."
if ! id "telegram-vk-poster" &>/dev/null; then
    useradd --system --shell /bin/false --home-dir $INSTALL_DIR --create-home telegram-vk-poster
fi

# Создание директорий
echo "📁 Создание директорий..."
mkdir -p $INSTALL_DIR
mkdir -p $LOG_DIR
mkdir -p $DATA_DIR
mkdir -p /tmp/telegram-to-vk-media

# Копирование файлов
echo "📋 Копирование файлов проекта..."
cp telegram-to-vk-poster.py $INSTALL_DIR/
cp requirements.txt $INSTALL_DIR/
cp .env.example $INSTALL_DIR/

# Создание виртуального окружения
echo "🐍 Создание виртуального окружения Python..."
cd $INSTALL_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Установка systemd service
echo "⚙️ Установка systemd service..."
cp telegram-to-vk-poster.service $SERVICE_FILE

# Настройка прав доступа
echo "🔐 Настройка прав доступа..."
chown -R telegram-vk-poster:telegram-vk-poster $INSTALL_DIR
chown -R telegram-vk-poster:telegram-vk-poster $LOG_DIR
chown -R telegram-vk-poster:telegram-vk-poster $DATA_DIR
chown -R telegram-vk-poster:telegram-vk-poster /tmp/telegram-to-vk-media

chmod 755 $INSTALL_DIR
chmod 644 $INSTALL_DIR/*.py
chmod 600 $INSTALL_DIR/.env.example
chmod 755 $LOG_DIR
chmod 755 $DATA_DIR

# Перезагрузка systemd
echo "🔄 Перезагрузка systemd daemon..."
systemctl daemon-reload

echo "✅ Установка завершена успешно!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Скопируйте .env.example в .env и настройте конфигурацию:"
echo "   sudo cp $INSTALL_DIR/.env.example $INSTALL_DIR/.env"
echo "   sudo nano $INSTALL_DIR/.env"
echo ""
echo "2. Запустите сервис:"
echo "   sudo systemctl enable telegram-to-vk-poster"
echo "   sudo systemctl start telegram-to-vk-poster"
echo ""
echo "3. Проверьте статус сервиса:"
echo "   sudo systemctl status telegram-to-vk-poster"
echo ""
echo "4. Просмотр логов:"
echo "   sudo journalctl -u telegram-to-vk-poster -f"
echo ""
echo "🎉 Готово! Сервис установлен в $INSTALL_DIR"
"""

with open("install.sh", "w", encoding="utf-8") as f:
    f.write(install_script)

print("✅ Создан скрипт установки: install.sh")