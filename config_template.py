# Конфігурація для продакшн
import os

# Telegram Bot Token (НЕ ПУБЛІКУЙТЕ ЦЕ!)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8137198869:AAHB25nKX6EAf_5A3elSsTWMnsoaK4u8YoU')

# URL для Mini App (замініть на ваш домен)
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com')

# Адміністратори (ID Telegram)
ADMINS = {
    int(os.getenv('ADMIN_ID_1', '664943604')),
    int(os.getenv('ADMIN_ID_2', '6766894203'))
}

# База даних
DATABASE_PATH = os.getenv('DATABASE_PATH', 'shop.db')
PHOTOS_PATH = os.getenv('PHOTOS_PATH', 'photos')

# Flask настройки
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
