import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime, timedelta,timezone
#TOKEN = '8024597010:AAGf9pAtUJ4lX_CPMI6qxqjhH3MO_zM852I'
TOKEN = '8137198869:AAHB25nKX6EAf_5A3elSsTWMnsoaK4u8YoU'

# URL для Mini App (замените на ваш домен)
WEBAPP_URL = "https://quairyx.github.io/paro-bot-miniapp/"  # Замените на реальный URL

ADMINS = {664943604,6766894203}
#ADMINS = {948158971}
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
PHOTO_DIR = 'photos'
os.makedirs(PHOTO_DIR, exist_ok=True)

translations = {
    'uk': {
        'start': '🌐 Виберіть мову',
        'category': '💨 Оберіть категорію рідини:',
        'buy': "🛒 Купити",
        'name': "📝 Ваше ім\'я:",
        'pay': '💵 Оплата: карта чи готівка?',
        'thanks': '📦 Дякуємо за замовлення!',
        'contact': "📱 Введіть ваш Telegram (@username) або номер телефону:",
        'invalid_contact': "⚠️ Некоректний формат. Введіть ще раз (@username або номер):",
        'delivery': "📦 Оберіть спосіб отримання:",
        'pickup': "Самовивіз",
        'paczkomat': "Поштомат",
        'pickup_date': "🗓️ Вкажіть місце та дату отримання товару (Wittchen Завтра):",
        'latin_name': "📝 Прізвище та ім'я (латиницею):",
        'post_phone': "📞 Номер телефону (мінімум 9 цифр):",
        'email': "✉️ Введіть email:",
        'invalid_email': "⚠️ Невірний email. Спробуйте ще раз:",
        'address': "✉️ Введіть адресу поштомату:",
        'invalid_payment_method': "❌ Будь ласка, оберіть 'Готівка' або 'Карта'.",
        'payment_card_info': "💳 Оплата картою (BLIK): 574338271\nПісля переказу, будь ласка, скиньте скріншот або PDF файл  оплати в чат.",
        'payment_received': "❤️ Дякую! Квитанція отримана, будь ласка, підтвердьте замовлення командою або натисніть кнопку.",
        'choose_payment_method': "💳 Оберіть спосіб оплати:",
        'invalid_delivery_choice': "❌ Будь ласка, оберіть 'Самовивіз' або 'Поштомат'.",
        'enter_telegram_or_phone': "📨 Введіть ваш Telegram або номер телефону:",
        'invalid_phone': "❌ Введіть правильний номер (мінімум 9 цифр).",
        'invalid_email_format': "❌ Невірний формат email.",
        'thanks_help': "❤️ Дякуємо! Адміністратор зв'яжеться з вами найближчим часом.",
        'order_not_found': "❌ Товар не знайдено.",
        'out_of_stock': "❌ Цей товар наразі відсутній у наявності.",
        'no_products': "❌ У цій категорії ще немає товарів.",
        'no_products_available': "❌ У цій категорії поки немає товарів у наявності.",
        'categories_empty': "❌ Категорії поки що відсутні.",
        'choose_liquid': "💧 Оберіть рідину:",
        'back': "⬅️ Назад",
        'self_pickup_notice': "Оскільки ви обрали самовивіз, оплата доступна карткою або готівкою.",
        'post_payment_notice': "Оскільки ви обрали поштомат, оплата доступна тільки картою (BLIK): 574338271\nПісля переказу, будь ласка, надішліть скріншот або PDF файл оплати в чат.\n\nВажливо! + 12 zl за доставку!",
        'cash': 'Готівка',
        'card': 'Карта',
        'help_contact_request': "Будь ласка, надішліть свій Telegram @username або номер телефону для зв'язку.",
        'help_text': "Команди:\n/language - Зміна мови\n/adm - зв'язатися з адміністратором\n/webapp - Відкрити Mini App",
        'language_changed': "Мова змінена на ",
        'thanks_post': "Дякуємо за замовлення!",
        'add_to_cart_s': "🛒 Додати в кошик",
        'cart_s': '🛒 Кошик',
        'price_label': '💰 Ціна:',
        'cart_expired': "⏰ Час резервування товарів минув, ваш кошик очищено.",
        'product_not_selected': "❌ Помилка: Товар не вибрано!",
        'error_product_not_found': "❌ Помилка: Товар не знайдено!",
        'error_out_of_stock': "❌ Не вистачає товару на складі!",
        'product_added_to_cart': "✅ Товар додано до кошика!",
        'cart_empty': "⚠️ Кошик порожній!",
        'total_amount': "💵 Сума:",
        'banned_message': "⛔ Ви тимчасово заблоковані і не можете оформити замовлення.",
        'clear_cart': "🗑️ Очистити кошик",
        'cart_cleared':"🗑️ Кошик очищено",
        'starts':"▶️ Для продовження напиши /start",
        'payment_amount': '💵 Сума до оплати:',
        'order_rejected_notice':'❌ Ваше замовлення було відхилено.\nБудь ласка, зв'яжіться з адміністратором ( /adm ) або зробіть нове замовлення.',
        'hi_text':'👋 Привіт!\n💖 Вітаємо в магазині рідин!\n🛒 Paro Store\n😍 Тут ти знайдеш найкращі продукти!\n⚙️ Допомога ( /help )',
        'Not_Flood': "⚠️ Будь ласка, зачекайте перед повторною командою.",
        'cart_cleared_manual1':'🧺 Ваш кошик очищено.',
        'order_accept_notice':'✅ Ваше замовлення прийнято!  Дякуємо за покупку! 🛒',
        'send_photo_only': 'Будь ласка, надішліть саме фотографію, а не документ чи інший файл.',
        'webapp_intro': '🌟 Відкрийте наш новий Mini App для зручнішого шопінгу!\n\n✨ У Mini App ви знайдете:\n• Зручний каталог товарів\n• Швидкий пошук\n• Красивий інтерфейс\n• Легке оформлення замовлень\n\n👆 Натисніть кнопку нижче:',
        'open_webapp': '🛍️ Відкрити магазин'
    },
    'en': {
        'start': '🌐 Wybierz język',
        'category': '💨 Wybierz kategorię liquidów:',
        'buy': "🛒 Kupić",
        'name': '📝 Twoje imię:',
        'pay': '💵 Płatność: karta czy gotówka?',
        'thanks': '📦 Dziękujemy za zamówienie!',
        'contact': "📱 Wprowadź swój Telegram (@username) lub numer telefonu:",
        'invalid_contact': "⚠️ Niepoprawny format. Wprowadź ponownie (@username lub numer):",
        'delivery': "📦 Wybierz sposób odbioru:",
        'pickup': "Odbiór osobisty",
        'paczkomat': "Paczkomat",
        'pickup_date': "🗓️ Podaj miejsce i datę odbioru towaru (Wittchen Jutro):",
        'latin_name': "📝 Nazwisko i imię (w alfabecie łacińskim):",
        'post_phone': "📞 Numer telefonu (minimum 9 cyfr):",
        'email': "✉️ Wprowadź email:",
        'invalid_email': "⚠️ Niepoprawny email. Spróbuj ponownie:",
        'address': "✉️ Wprowadź adres paczkomatu:",
        'invalid_payment_method': "❌ Proszę wybrać 'Gotówka' lub 'Karta'.",
        'payment_card_info': "💳 Płatność kartą (BLIK): 574338271\nPo przelewie prosimy o przesłanie potwierdzenia płatności na czacie.",
        'payment_received': "❤️ Dziękujemy! Potwierdzenie otrzymane, prosimy potwierdzić zamówienie komendą lub przyciskiem.",
        'choose_payment_method': "Wybierz metodę płatności:",
        'invalid_delivery_choice': "❌ Proszę wybrać 'Odbiór osobisty' lub 'Paczkomat'.",
        'enter_telegram_or_phone': "📨 Wprowadź swój Telegram lub numer telefonu:",
        'invalid_phone': "❌ Wprowadź poprawny numer (minimum 9 cyfr).",
        'invalid_email_format': "❌ Niepoprawny format email.",
        'thanks_help': "❤️ Dziękujemy! Administrator skontaktuje się z Tobą wkrótce.",
        'order_not_found': "❌ Produkt nie znaleziony.",
        'out_of_stock': "❌ Ten produkt jest obecnie niedostępny.",
        'no_products': "❌ W tej kategorii nie ma jeszcze produktów.",
        'no_products_available': "❌ W tej kategorii nie ma dostępnych produktów.",
        'categories_empty': "❌ Kategorie są obecnie niedostępne.",
        'choose_liquid': "💧 Wybierz liquid:",
        'back': "⬅️ Wstecz",
        'self_pickup_notice': "Ponieważ wybrałeś odbiór osobisty, płatność dostępna jest kartą lub gotówką.",
        'post_payment_notice': "Ponieważ wybrałeś paczkomat, płatność dostępna jest tylko kartą (BLIK): 574338271\nPo przelewie prosimy o przesłanie potwierdzenia płatności na czacie.\n\nWażne! + 12 zł za dostawę!",
        'cash': 'Gotówka',
        'card': 'Karta',
        'choose_payment_method': 'Wybierz metodę płatności:',
        'help_contact_request': "Proszę, wyślij swój Telegram @username lub numer telefonu do kontaktu.",
        'help_text': "Polecenia:\n/language - Zmień język\n/adm - skontaktuj się z administratorem\n/webapp - Otwórz Mini App",
        'language_changed': "Język został zmieniony na ",
        'total': 'Razem',
        'post_fee_notice': '+12 zł за доставку Paczkomat включено',
        'thanks_post': "Dziękujemy za zamówienie!",
        'add_to_cart_s': "🛒 Dodaj do koszyka",
        'cart_s': '🛒 Koszyk',
        'price_label': '💰 Cena:',
        'cart_expired': "⏰ Czas rezerwacji produktów minął, Twój koszyk został opróżniony.",
        'product_not_selected': "❌ Błąd: Nie wybrano produktu!",
        'error_product_not_found': "❌ Błąd: Towar nie znaleziony!",
        'error_out_of_stock': "❌ Brak towaru na magazynie!",
        'product_added_to_cart': "✅ Produkt dodany do koszyka!",
        'cart_empty': "⚠️ Koszyk jest pusty!",
        'total_amount': "💵 Suma:",
        'banned_message': "⛔ Jesteś tymczasowo zablokowany i nie możesz złożyć zamówienia.",
        'clear_cart': "🗑️ Wyczyść koszyk",
        'cart_cleared': "🗑️ Koszyk wyczyszczony",
        'starts': "▶️ Aby kontynuować, napisz /start",
        'payment_amount': '💵 Kwota do zapłaty:',
        'order_rejected_notice':'❌ Twoje zamówienie zostało odrzucone.\nSkontaktuj się z administratorem lub złóż nowe zamówienie.',
        'hi_text':'👋 Cześć!\n💖 Witamy w sklepie z liquidami!\n🛒 Paro Store\n😍 Tutaj znajdziesz najlepsze produkty\n⚙️ Pomoc ( /help )',
        'Not_Flood': "⚠️ Proszę, poczekaj przed ponownym użyciem komendy.",
        'cart_cleared_manual1':'🧺 Twój koszyk został opróżniony.',
        'order_accept_notice':'✅ Twoje zamówienie zostało przyjęte!  Dziękujemy za zakup! 🛒',
        'send_photo_only': 'Proszę wysłać dokładnie zdjęcie, a nie dokument lub inny plik.',
        'webapp_intro': '🌟 Otwórz naszą nową Mini App dla wygodniejszego zakupu!\n\n✨ W Mini App znajdziesz:\n• Wygodny katalog produktów\n• Szybkie wyszukiwanie\n• Piękny interfejs\n• Łatwe składanie zamówień\n\n👆 Naciśnij przycisk poniżej:',
        'open_webapp': '🛍️ Otwórz sklep'
    },
    'ru': {
        'start': '🌐 Выберите язык',
        'category': '💨 Выберите категорию жидкости:',
        'buy': "🛒 Купить",
        'name': '📝 Ваше имя:',
        'pay': '💵 Оплата: карта или наличные?',
        'thanks': '📦 Спасибо за заказ!',
        'contact': "📱 Введите ваш Telegram (@username) или номер телефона:",
        'invalid_contact': "⚠️ Некорректный формат. Введите еще раз (@username или номер):",
        'delivery': "📦 Выберите способ получения:",
        'pickup': "Самовывоз",
        'paczkomat': "Почтомат",
        'pickup_date': "🗓️ Укажите место и дату получения товара (Wittchen Завтра):",
        'latin_name': "📝 Фамилия и имя (латиницей):",
        'post_phone': "📞 Номер телефона (минимум 9 цифр):",
        'email': "✉️ Введите email:",
        'invalid_email': "⚠️ Неверный email. Попробуйте еще раз:",
        'address': "✉️ Введите адрес почтомата:",
        'invalid_payment_method': "❌ Пожалуйста, выберите 'Наличные' или 'Карта'.",
        'payment_card_info': "💳 Оплата картой (BLIK): 574338271\nПосле перевода, пожалуйста, отправьте скриншот либо PDF файл  оплаты в чат.",
        'payment_received': "❤️ Спасибо! Квитанция получена, пожалуйста, подтвердите заказ командой или кнопкой.",
        'choose_payment_method': "Выберите способ оплаты:",
        'invalid_delivery_choice': "❌ Пожалуйста, выберите 'Самовывоз' или 'Почтомат'.",
        'enter_telegram_or_phone': "📨 Введите ваш Telegram или номер телефона:",
        'invalid_phone': "❌ Введите правильный номер (минимум 9 цифр).",
        'invalid_email_format': "❌ Неверный формат email.",
        'thanks_help': "❤️ Спасибо! Администратор свяжется с вами в ближайшее время.",
        'order_not_found': "❌ Товар не найден.",
        'out_of_stock': "❌ Этот товар в данный момент отсутствует в наличии.",
        'no_products': "❌ В этой категории пока нет товаров.",
        'no_products_available': "❌ В этой категории пока нет товаров в наличии.",
        'categories_empty': "❌ Категории пока отсутствуют.",
        'choose_liquid': "💧 Выберите жидкость:",
        'back': "⬅️ Назад",
        'self_pickup_notice': "Так как вы выбрали самовывоз, оплата возможна картой или наличными.",
        'post_payment_notice': "Так как вы выбрали почтомат, оплата доступна только картой \n\n(BLIK): 574338271\n\nПосле перевода, пожалуйста, отправьте скриншот либо PDF файл оплаты в чат.\n\nВажно! + 12 злотых за доставку!",
        'cash': 'Наличные',
        'card': 'Карта',
        'choose_payment_method': 'Выберите способ оплаты:',
        'help_contact_request': "Пожалуйста, отправьте свой Telegram @username или номер телефона для связи.",
        'help_text': "Команды:\n/language - Изменить язык\n/adm - связаться с администратором\n/webapp - Открыть Mini App",
        'language_changed': "Язык изменён на ",
        'thanks_post': "Спасибо за заказ!",
        'add_to_cart_s': "🛒 Добавить в корзину",
        'cart_s': '🛒 Корзина',
        'price_label': '💰 Цена:',
        'cart_expired': "⏰ Время резервирования товаров истекло, ваша корзина очищена.",
        'product_not_selected': "❌ Ошибка: Товар не выбран!",
        'error_product_not_found': "❌ Ошибка: Товар не найден!",
        'error_out_of_stock': "❌ Нет товара на складе!",
        'product_added_to_cart': "✅ Товар добавлен в корзину!",
        'cart_empty': "⚠️ Корзина пуста!",
        'total_amount': "💵 Сумма:",
        'banned_message': "⛔ Вы временно заблокированы и не можете оформить заказ.",
        'clear_cart': "🗑️ Очистить корзину",
        'cart_cleared': "🗑️ Корзина очищена",
        'starts': "▶️ Для продолжения напиши /start",
        'payment_amount': '💵 Сумма к оплате:',
        'order_rejected_notice':'❌ Ваш заказ был отклонён.\nПожалуйста, свяжитесь с администратором или оформите новый заказ.',
        'hi_text':'👋 Привет!\n💖 Добро пожаловать в магазин жидкостей!\n🛒 Paro Store\n😍 Здесь ты найдёшь лучшие продукты⬇\n⚙️ Помощь ( /help )',
        'Not_Flood': "⚠️ Будь ласка, зачекайте перед повторною командою.",
        'cart_cleared_manual1':'🧺 Ваша корзина очищена.',
        'order_accept_notice':'✅ Ваш заказ принят!  Спасибо за покупку! 🛒',
        'send_photo_only': 'Пожалуйста, отправьте именно фотографию, а не документ или другой файл.',
        'webapp_intro': '🌟 Откройте наше новое Mini App для удобного шопинга!\n\n✨ В Mini App вы найдете:\n• Удобный каталог товаров\n• Быстрый поиск\n• Красивый интерфейс\n• Легкое оформление заказов\n\n👆 Нажмите кнопку ниже:',
        'open_webapp': '🛍️ Открыть магазин'
    }
}

class OrderFSM(StatesGroup):
    choosing_language = State()
    choosing_category = State()
    choosing_product = State()
    confirming_product = State()
    entering_name = State()
    entering_contact = State() 
    choosing_payment = State()
    waiting_for_payment_screenshot = State()

class HelpFSM(StatesGroup):
    waiting_for_help_contact = State()

class AdminFSM(StatesGroup):
    choosing_action = State()
    adding_category = State()
    choosing_product_category = State()
    adding_product_name = State()
    adding_product_description = State()
    adding_product_price = State()
    adding_product_quantity = State()
    adding_product_photo = State()
    selecting_product_for_edit = State()          
    editing_product_field = State()
    entering_new_value = State()
    selecting_product_for_quantity_add = State()
    entering_quantity_to_add = State()
    selecting_product_for_delete = State()
    confirming_delete = State()
    deleting_category = State()
    selecting_product_for_quantity_sub = State()
    entering_quantity_to_sub = State()   

conn = sqlite3.connect('shop.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    language TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name_en TEXT,
    name_uk TEXT,
    name_ru TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    category_id INTEGER,
    name_en TEXT,
    name_uk TEXT,
    name_ru TEXT,
    description_en TEXT,
    description_uk TEXT,
    description_ru TEXT,
    price REAL,
    quantity INTEGER,
    photo TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    full_name TEXT,
    payment_method TEXT,
    status TEXT
)''')
try:
    c.execute("ALTER TABLE orders ADD COLUMN contact TEXT")
except sqlite3.OperationalError:
    pass

try:
    c.execute("ALTER TABLE orders ADD COLUMN delivery TEXT")
except sqlite3.OperationalError:
    pass

try:
    c.execute("ALTER TABLE orders ADD COLUMN delivery_info TEXT")
except sqlite3.OperationalError:
    pass
try:
    c.execute("ALTER TABLE orders ADD COLUMN quantity INTEGER")
except sqlite3.OperationalError:
    pass

# Дополнительные таблицы для профилей и банов
try:
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
except sqlite3.OperationalError:
    pass

try:
    c.execute('''CREATE TABLE IF NOT EXISTS bans (
        user_id INTEGER PRIMARY KEY,
        banned_until INTEGER
    )''')
except sqlite3.OperationalError:
    pass

try:
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
except sqlite3.OperationalError:
    pass

conn.commit()

import time
user_last_start = {}

# Добавляем команду для открытия Mini App
@dp.message_handler(commands=['webapp'], state="*")
async def open_webapp(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or 'uk'
    
    # Создаем кнопку с Mini App
    markup = InlineKeyboardMarkup()
    webapp_btn = InlineKeyboardButton(
        text=translations[lang]['open_webapp'], 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_btn)
    
    await message.answer(
        translations[lang]['webapp_intro'],
        reply_markup=markup
    )

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    current_time = time.time()
    user_id = message.from_user.id

    lang = get_user_language(user_id)

    if not lang:
        # Користувач новий — показуємо вибір мови
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Українська 🇺🇦", callback_data='lang_uk'),
            InlineKeyboardButton("Polski 🇵🇱", callback_data='lang_en'),
            InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')
        )
        await message.answer("Виберіть мову / Wybierz język / Выберите язык", reply_markup=markup)
        await OrderFSM.choosing_language.set()
        return

    # Антифлуд
    if user_id in user_last_start:
        elapsed = current_time - user_last_start[user_id]
        if elapsed < 10:
            await message.answer(translations[lang]['Not_Flood'])
            return

    user_last_start[user_id] = current_time

    # Отправляем приветствие с гифкой
    photo_path = 'photos/juja.gif'
    welcome_text = translations[lang]['hi_text']

    try:
        with open(photo_path, 'rb') as animation:
            await bot.send_animation(chat_id=message.chat.id, animation=animation, caption=welcome_text)
    except FileNotFoundError:
        await message.answer(welcome_text)

    await state.update_data(language=lang)

    # Основное меню с кнопкой Mini App
    markup = InlineKeyboardMarkup()
    
    # Кнопка Mini App
    webapp_btn = InlineKeyboardButton(
        text=f"🌟 {translations[lang]['open_webapp']}",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_btn)
    
    # Обычные категории (для совместимости)
    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    if rows:
        markup.add(InlineKeyboardButton("📱 Звичайний інтерфейс", callback_data='classic_interface'))

    await message.answer(
        "🛍️ Оберіть спосіб покупок:\n\n"
        "🌟 **Mini App** - новий красивий інтерфейс\n"
        "📱 **Звичайний** - класичні кнопки в Telegram",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@dp.callback_query_handler(lambda c: c.data == 'classic_interface', state='*')
async def show_classic_interface(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = get_user_language(user_id) or 'uk'
    
    await state.update_data(language=lang)

    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    if not rows:
        await callback.message.answer("Категорії поки що відсутні.")
        return

    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'cat_{row[0]}'))

    await callback.message.edit_text(translations[lang]['category'], reply_markup=markup)
    await OrderFSM.choosing_category.set()

def save_user_language(user_id, username, lang_code):
    c.execute("INSERT OR REPLACE INTO users (id, username, language) VALUES (?, ?, ?)",
              (user_id, username, lang_code))
    conn.commit()

def get_user_language(user_id):
    c.execute("SELECT language FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    return row[0] if row else None

# Остальной код остается таким же...
# [Здесь остальные обработчики из оригинального файла]
