# Создаем дополнительные файлы для продакшена

# 1. .gitignore
gitignore_content = """# Конфигурационные файлы
.env
*.env
!.env.example

# Файлы сессии Telegram
*.session
*.session-journal

# Логи
*.log
logs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Виртуальное окружение
venv/
env/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Временные файлы
*.tmp
temp/
tmp/

# Системные файлы
.DS_Store
Thumbs.db

# Медиафайлы
media/
downloads/
uploads/
"""

with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content)

print("✅ Создан файл .gitignore")

# 2. LICENSE (MIT)
license_content = """MIT License

Copyright (c) 2025 svod011929

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open("LICENSE", "w", encoding="utf-8") as f:
    f.write(license_content)

print("✅ Создан файл LICENSE")

# 3. CHANGELOG.md
changelog_content = """# Changelog

Все значимые изменения в этом проекте будут документированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и этот проект следует [Семантическому версионированию](https://semver.org/lang/ru/).

## [1.0.0] - 2025-01-12

### Добавлено
- 🎉 Первый релиз Telegram to VK Poster
- 🔄 Автоматический репост сообщений из Telegram канала в VK группу
- 🛡️ Отказоустойчивость с отслеживанием последнего поста
- 📸 Поддержка автоматической загрузки изображений
- ⚙️ Конфигурация через .env файлы
- 🐧 Поддержка systemd для работы в качестве сервиса
- 📝 Подробное логирование всех операций
- ✍️ Настраиваемые подписи к постам
- 🔒 Безопасная работа под отдельным пользователем
- 📋 Автоматический скрипт установки
- 📖 Подробная документация

### Технические особенности
- Асинхронная работа с Telegram API через Telethon
- Интеграция с VK API для публикации постов
- Автоматическое управление файлами сессии
- Ограничения ресурсов через systemd
- Поддержка ротации логов

### Безопасность  
- Работа под непривилегированным пользователем
- Изоляция файловой системы
- Ограничения памяти и CPU
- Защита конфигурационных файлов

## [Планируется]

### В следующих версиях
- 📹 Поддержка видеофайлов
- 🔗 Поддержка ссылок и вложений
- 📊 Веб-интерфейс для мониторинга
- 🔄 Поддержка множественных каналов
- 📈 Метрики и статистика
- 🌐 Docker контейнеризация
- 🚀 API для внешней интеграции
"""

with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write(changelog_content)

print("✅ Создан файл CHANGELOG.md")