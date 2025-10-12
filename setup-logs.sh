#!/bin/bash
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
