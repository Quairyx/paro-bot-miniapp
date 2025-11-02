import sqlite3

# Создаем дополнительные таблицы для профилей пользователей и банов
def setup_additional_tables():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # Таблица профилей пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        contact TEXT,
        delivery TEXT,
        pickup_date TEXT,
        post_name TEXT,
        post_phone TEXT,
        post_email TEXT,
        post_address TEXT,
        payment TEXT
    )''')
    
    # Таблица банов
    c.execute('''CREATE TABLE IF NOT EXISTS bans (
        user_id INTEGER PRIMARY KEY,
        banned_until INTEGER
    )''')
    
    # Таблица элементов заказа (уже должна быть, но проверим)
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    
    conn.commit()
    conn.close()
    print("Дополнительные таблицы созданы успешно!")

if __name__ == '__main__':
    setup_additional_tables()