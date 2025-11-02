# 🚀 Інструкція: GitHub → Timeweb Cloud

## 📤 Частина 1: Завантаження на GitHub

### Крок 1: Створіть репозиторій на GitHub
1. Відкрийте https://github.com
2. Натисніть "New repository"
3. Назва: `paro-bot-miniapp`
4. Опис: `Telegram Bot з Mini App для магазину рідин`
5. **НЕ** ставте галочку "Add a README file"
6. Натисніть "Create repository"

### Крок 2: Підключіть локальний репозиторій
Скопіюйте команди з GitHub і виконайте:

```bash
# У вашій папці проекту (ви вже тут)
git remote add origin https://github.com/YOUR_USERNAME/paro-bot-miniapp.git
git branch -M main
git push -u origin main
```

## 🌐 Частина 2: Розгортання на Timeweb Cloud

### Крок 1: Підключіться до сервера
```bash
ssh root@your-server-ip
```

### Крок 2: Клонуйте репозиторій
```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/paro-bot-miniapp.git
cd paro-bot-miniapp
```

### Крок 3: Встановіть Python залежності
```bash
# Встановіть pip (якщо немає)
apt update && apt install python3-pip -y

# Встановіть залежності
pip3 install -r requirements.txt
```

### Крок 4: Налаштуйте конфігурацію
```bash
# Створіть конфіг з шаблону
cp config_template.py config.py

# Відредагуйте конфіг
nano config.py
```

**У config.py змініть:**
```python
BOT_TOKEN = "8024597010:AAGf9pAtUJ4lX_CPMI6qxqjhH3MO_zM852I"  # Ваш токен
WEBAPP_URL = "http://your-server-ip"  # IP вашого сервера
ADMINS = {664943604, 6766894203}  # Ваші Telegram ID
```

### Крок 5: Ініціалізуйте базу даних
```bash
python3 setup_db.py
```

### Крок 6: Налаштуйте systemd сервіси

**Створіть сервіс для бота:**
```bash
nano /etc/systemd/system/paro-bot.service
```

Вміст файлу:
```ini
[Unit]
Description=Paro Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/paro-bot-miniapp
ExecStart=/usr/bin/python3 parobot1.1.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Створіть сервіс для Mini App:**
```bash
nano /etc/systemd/system/paro-webapp.service
```

Вміст файлу:
```ini
[Unit]
Description=Paro Mini App Flask Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/paro-bot-miniapp/webapp
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Крок 7: Запустіть сервіси
```bash
# Перезавантажте systemd
systemctl daemon-reload

# Запустіть і увімкніть автозапуск
systemctl enable paro-bot
systemctl enable paro-webapp

systemctl start paro-bot
systemctl start paro-webapp

# Перевірте статус
systemctl status paro-bot
systemctl status paro-webapp
```

### Крок 8: Налаштуйте Nginx (опціонально)
```bash
# Встановіть Nginx
apt install nginx -y

# Створіть конфіг
nano /etc/nginx/sites-available/paro-bot
```

Вміст файлу:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # або IP сервера
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static/photos/ {
        alias /var/www/paro-bot-miniapp/photos/;
        expires 30d;
    }
}
```

```bash
# Активуйте конфіг
ln -s /etc/nginx/sites-available/paro-bot /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## 🔧 Крок 9: Налаштуйте Telegram Bot

### В @BotFather:
1. `/mybots` → Ваш бот → `Bot Settings` → `Menu Button`
2. **Text**: "🛍️ Магазин"
3. **URL**: `http://your-server-ip` (або ваш домен)

## ✅ Крок 10: Перевірка

```bash
# Перевірте логи
journalctl -u paro-bot -f
journalctl -u paro-webapp -f

# Перевірте порти
netstat -tlnp | grep :5000

# Перевірте веб-додаток
curl http://localhost:5000
```

## 🔄 Оновлення проекту

Коли ви вносите зміни:

```bash
# Локально
git add .
git commit -m "Опис змін"
git push

# На сервері
cd /var/www/paro-bot-miniapp
git pull
systemctl restart paro-bot
systemctl restart paro-webapp
```

## 🆘 Вирішення проблем

### Перевірте статус:
```bash
systemctl status paro-bot
systemctl status paro-webapp
```

### Подивіться логи:
```bash
journalctl -u paro-bot --since "10 minutes ago"
journalctl -u paro-webapp --since "10 minutes ago"
```

### Перевірте порти:
```bash
ss -tlnp | grep 5000
```

### Перевірте права доступу:
```bash
chmod +x parobot1.1.py
chmod +x webapp/app.py
```

## 🎉 Готово!

Тепер ваш бот працює на сервері і доступний 24/7!
Mini App доступний за адресою: `http://your-server-ip`