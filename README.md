# 🛍️ Paro Bot - Telegram Mini App для магазину рідин

Повнофункціональний Telegram бот з веб-інтерфейсом (Mini App) для продажу рідин для вейпінгу.

## ✨ Особливості

- 🤖 **Telegram Bot** з повною адмін-панеллю
- 🌟 **Mini App** - сучасний веб-інтерфейс
- 🌍 **Мультимовність** - Українська, Польська, Російська
- 💳 **Оплата** - Готівка, Карта (BLIK)
- 📦 **Доставка** - Самовивіз, Поштомат
- 🛒 **Кошик** з можливістю зміни кількості
- 📱 **Адаптивний дизайн** для мобільних

## 🚀 Швидкий старт

### 1. Клонування репозиторію
```bash
git clone https://github.com/YOUR_USERNAME/paro-bot.git
cd paro-bot
```

### 2. Встановлення залежностей
```bash
# Python залежності для бота
pip install aiogram==2.25.1

# Flask залежності для Mini App
cd webapp
pip install -r requirements.txt
```

### 3. Налаштування
```bash
# Створіть конфіг з шаблону
cp config_template.py config.py

# Відредагуйте config.py:
# - Додайте ваш BOT_TOKEN
# - Встановіть WEBAPP_URL
# - Налаштуйте ADMINS
```

### 4. Ініціалізація бази даних
```bash
python setup_db.py
```

### 5. Запуск

**Бот:**
```bash
python parobot1.1.py
```

**Mini App (у новому терміналі):**
```bash
cd webapp
python app.py
```

## 📁 Структура проекту

```
├── parobot1.1.py              # Основний бот
├── setup_db.py                # Ініціалізація БД
├── config_template.py         # Шаблон конфігурації
├── shop.db                    # База даних SQLite
├── photos/                    # Фото товарів
└── webapp/                    # Mini App
    ├── app.py                 # Flask сервер
    ├── requirements.txt       # Залежності
    ├── templates/
    │   └── index.html        # Веб-інтерфейс
    └── static/               # Статичні файли
```

## 🔧 Адмін-команди бота

- `/admin` - Панель адміністратора
- `/ban <user_id> <hours>` - Забанити користувача
- `/unban <user_id>` - Розбанити користувача
- `/send all <message>` - Розсилка всім
- `/send <user_id> <message>` - Повідомлення користувачу
- `/count` - Кількість товарів на складі

## 🌐 Розгортання на продакшн

### Timeweb Cloud

1. **Завантажте файли на сервер**
2. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   pip install aiogram==2.25.1
   ```

3. **Налаштуйте змінні середовища:**
   ```bash
   export BOT_TOKEN="ваш_токен"
   export WEBAPP_URL="https://yourdomain.com"
   export FLASK_HOST="0.0.0.0"
   export FLASK_PORT="80"
   ```

4. **Запустіть через systemd або screen:**
   ```bash
   # Бот
   python parobot1.1.py &
   
   # Mini App
   cd webapp && python app.py &
   ```

### Nginx конфігурація

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/photos/ {
        alias /path/to/your/photos/;
    }
}
```

## 📱 Налаштування Mini App в Telegram

1. **@BotFather** → `/mybots` → Ваш бот
2. **Bot Settings** → **Menu Button**
3. **Text**: "🛍️ Магазин"
4. **URL**: ваш домен

## 🔒 Безпека

- ❌ **НЕ ПУБЛІКУЙТЕ** токен бота в коді
- ✅ Використовуйте змінні середовища
- ✅ Додайте `config.py` в `.gitignore`
- ✅ Обмежте доступ до адмін-команд

## 📸 Скріншоти

*(Додайте скріншоти Mini App та бота)*

## 🤝 Внесок

1. Fork проекту
2. Створіть feature branch
3. Зробіть commit
4. Push в branch
5. Створіть Pull Request

## 📄 Ліцензія

MIT License - див. [LICENSE](LICENSE) файл.

## 📞 Підтримка

Якщо виникли питання:
- Створіть [Issue](https://github.com/YOUR_USERNAME/paro-bot/issues)
- Напишіть в Telegram: @your_username

---

**Створено з ❤️ для Paro Store**