# Создаем requirements.txt
requirements = """telethon==1.41.1
vk-api==11.10.0
python-dotenv==1.0.1
requests==2.32.3
aiofiles==24.1.0
"""

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)

print("✅ Создан файл requirements.txt")