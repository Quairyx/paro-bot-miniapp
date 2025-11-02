from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import json
from datetime import datetime, timezone

app = Flask(__name__)

# Подключение к существующей базе данных бота
DB_PATH = os.getenv('DATABASE_PATH', '../shop.db')
PHOTOS_PATH = os.getenv('PHOTOS_PATH', '../photos')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Главная страница Mini App"""
    return render_template('index.html')

@app.route('/api/categories')
def get_categories():
    """API для получения категорий"""
    lang = request.args.get('lang', 'uk')
    
    conn = get_db_connection()
    query = f"SELECT id, name_{lang} as name FROM categories"
    categories = conn.execute(query).fetchall()
    conn.close()
    
    return jsonify([dict(category) for category in categories])

@app.route('/api/products/<int:category_id>')
def get_products(category_id):
    """API для получения товаров по категории"""
    lang = request.args.get('lang', 'uk')
    
    conn = get_db_connection()
    query = f"""
        SELECT id, name_{lang} as name, description_{lang} as description, 
               price, quantity, photo 
        FROM products 
        WHERE category_id = ? AND quantity > 0
    """
    products = conn.execute(query, (category_id,)).fetchall()
    conn.close()
    
    # Добавляем полный путь к фото
    result = []
    for product in products:
        product_dict = dict(product)
        if product_dict['photo']:
            product_dict['photo_url'] = f"/static/photos/{product_dict['photo']}"
        else:
            product_dict['photo_url'] = None
        result.append(product_dict)
    
    return jsonify(result)

@app.route('/api/product/<int:product_id>')
def get_product(product_id):
    """API для получения детальной информации о товаре"""
    lang = request.args.get('lang', 'uk')
    
    conn = get_db_connection()
    query = f"""
        SELECT id, name_{lang} as name, description_{lang} as description, 
               price, quantity, photo, category_id
        FROM products 
        WHERE id = ?
    """
    product = conn.execute(query, (product_id,)).fetchone()
    conn.close()
    
    if product:
        product_dict = dict(product)
        if product_dict['photo']:
            product_dict['photo_url'] = f"/static/photos/{product_dict['photo']}"
        else:
            product_dict['photo_url'] = None
        return jsonify(product_dict)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/order', methods=['POST'])
def create_order():
    """API для создания заказа"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    full_name = data.get('full_name')
    contact = data.get('contact')
    delivery = data.get('delivery')
    delivery_info = data.get('delivery_info', '')
    payment_method = data.get('payment_method')
    cart = data.get('cart', [])  # [{"product_id": 1, "quantity": 2}, ...]
    lang = data.get('lang', 'uk')
    
    if not all([user_id, full_name, contact, delivery, payment_method, cart]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    
    try:
        # Проверяем наличие товаров
        for item in cart:
            product = conn.execute("SELECT quantity FROM products WHERE id = ?", 
                                 (item['product_id'],)).fetchone()
            if not product or product['quantity'] < item['quantity']:
                return jsonify({'error': f'Not enough stock for product {item["product_id"]}'}), 400
        
        # Создаем заказ
        cursor = conn.execute('''
            INSERT INTO orders (user_id, full_name, payment_method, status, contact, delivery, delivery_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, full_name, payment_method, 'pending', contact, delivery, delivery_info))
        
        order_id = cursor.lastrowid
        
        # Добавляем товары в заказ
        total_sum = 0
        for item in cart:
            # Получаем цену товара
            product = conn.execute("SELECT price FROM products WHERE id = ?", 
                                 (item['product_id'],)).fetchone()
            if product:
                total_sum += product['price'] * item['quantity']
                
                # Добавляем в order_items
                conn.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity)
                    VALUES (?, ?, ?)
                ''', (order_id, item['product_id'], item['quantity']))
        
        # Добавляем стоимость доставки для пачкомата
        if delivery == 'post':
            total_sum += 12
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'total': total_sum
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/static/photos/<filename>')
def serve_photo(filename):
    """Обслуживание фотографий товаров"""
    from flask import send_from_directory
    return send_from_directory(PHOTOS_PATH, filename)

@app.route('/api/translations')
def get_translations():
    """API для получения переводов"""
    translations = {
        'uk': {
            'app_title': 'Paro Store',
            'categories': 'Категорії',
            'products': 'Товари',
            'cart': 'Кошик',
            'checkout': 'Оформити замовлення',
            'add_to_cart': 'Додати до кошика',
            'price': 'Ціна',
            'quantity': 'Кількість',
            'total': 'Всього',
            'name': "Ваше ім'я",
            'contact': 'Контакт (Telegram або телефон)',
            'delivery': 'Спосіб доставки',
            'pickup': 'Самовивіз',
            'post': 'Поштомат',
            'payment': 'Спосіб оплати',
            'cash': 'Готівка',
            'card': 'Карта',
            'order_success': 'Замовлення успішно оформлено!',
            'error': 'Помилка',
            'empty_cart': 'Кошик порожній',
            'back': 'Назад',
            'pickup_info': 'Місце та дата самовивозу',
            'post_name': 'Прізвище та імя (латиницею)',
            'post_phone': 'Номер телефону',
            'post_email': 'Email',
            'post_address': 'Адреса поштомату',
            'required_field': 'Обовязкове поле',
            'loading': 'Завантаження...',
            'choose_flavor': 'Оберіть смак',
            'choose_volume': 'Оберіть обєм',
            'choose_nicotine': 'Рівень нікотину'
        },
        'en': {
            'app_title': 'Paro Store',
            'categories': 'Kategorie',
            'products': 'Produkty',
            'cart': 'Koszyk',
            'checkout': 'Złóż zamówienie',
            'add_to_cart': 'Dodaj do koszyka',
            'price': 'Cena',
            'quantity': 'Ilość',
            'total': 'Razem',
            'name': 'Twoje imię',
            'contact': 'Kontakt (Telegram lub telefon)',
            'delivery': 'Sposób dostawy',
            'pickup': 'Odbiór osobisty',
            'post': 'Paczkomat',
            'payment': 'Sposób płatności',
            'cash': 'Gotówka',
            'card': 'Karta',
            'order_success': 'Zamówienie zostało złożone!',
            'error': 'Błąd',
            'empty_cart': 'Koszyk jest pusty',
            'back': 'Wstecz',
            'pickup_info': 'Miejsce i data odbioru',
            'post_name': 'Nazwisko i imię (alfabetem łacińskim)',
            'post_phone': 'Numer telefonu',
            'post_email': 'Email',
            'post_address': 'Adres paczkomatu',
            'required_field': 'Pole wymagane',
            'loading': 'Ładowanie...',
            'choose_flavor': 'Wybierz smak',
            'choose_volume': 'Wybierz objętość',
            'choose_nicotine': 'Poziom nikotyny'
        },
        'ru': {
            'app_title': 'Paro Store',
            'categories': 'Категории',
            'products': 'Товары',
            'cart': 'Корзина',
            'checkout': 'Оформить заказ',
            'add_to_cart': 'Добавить в корзину',
            'price': 'Цена',
            'quantity': 'Количество',
            'total': 'Всего',
            'name': 'Ваше имя',
            'contact': 'Контакт (Telegram или телефон)',
            'delivery': 'Способ доставки',
            'pickup': 'Самовывоз',
            'post': 'Почтомат',
            'payment': 'Способ оплаты',
            'cash': 'Наличные',
            'card': 'Карта',
            'order_success': 'Заказ успешно оформлен!',
            'error': 'Ошибка',
            'empty_cart': 'Корзина пуста',
            'back': 'Назад',
            'pickup_info': 'Место и дата самовывоза',
            'post_name': 'Фамилия и имя (латиницей)',
            'post_phone': 'Номер телефона',
            'post_email': 'Email',
            'post_address': 'Адрес почтомата',
            'required_field': 'Обязательное поле',
            'loading': 'Загрузка...',
            'choose_flavor': 'Выберите вкус',
            'choose_volume': 'Выберите объем',
            'choose_nicotine': 'Уровень никотина'
        }
    }
    
    lang = request.args.get('lang', 'uk')
    return jsonify(translations.get(lang, translations['uk']))

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host=host, port=port)