# Создаем дополнительные служебные скрипты

# 1. Скрипт удаления
uninstall_script = """#!/bin/bash
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
"""

with open("uninstall.sh", "w", encoding="utf-8") as f:
    f.write(uninstall_script)

# 2. Скрипт обновления
update_script = """#!/bin/bash
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
"""

with open("update.sh", "w", encoding="utf-8") as f:
    f.write(update_script)

# 3. Скрипт для настройки логирования
setup_logs_script = """#!/bin/bash
# Скрипт настройки ротации логов для Telegram to VK Poster

set -e

echo "📝 Настройка ротации логов..."

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен с правами суперпользователя (sudo)" 
   exit 1
fi

# Создание конфигурации logrotate
cat > /etc/logrotate.d/telegram-to-vk-poster << 'EOF'
/var/log/telegram-to-vk-poster/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 telegram-vk-poster telegram-vk-poster
    postrotate
        systemctl reload telegram-to-vk-poster 2>/dev/null || true
    endscript
}
EOF

echo "✅ Настройка ротации логов завершена"
echo "ℹ️ Логи будут автоматически ротироваться каждый день"
echo "ℹ️ Хранится последние 30 дней логов в сжатом виде"
"""

with open("setup-logs.sh", "w", encoding="utf-8") as f:
    f.write(setup_logs_script)

# Делаем скрипты исполняемыми (в Python мы не можем изменить права, но покажем это в README)
print("✅ Созданы служебные скрипты:")
print("  - uninstall.sh (скрипт удаления)")
print("  - update.sh (скрипт обновления)")  
print("  - setup-logs.sh (настройка ротации логов)")
print("\n📝 Примечание: После создания файлов выполните:")
print("chmod +x *.sh")