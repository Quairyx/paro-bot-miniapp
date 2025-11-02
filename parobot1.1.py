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

# URL для Mini App (замініть на ваш домен)
WEBAPP_URL = "https://yourdomain.com"  # Замініть на реальний URL

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
        'latin_name': "📝 Прізвище та ім’я (латиницею):",
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
        'order_rejected_notice':'❌ Ваше замовлення було відхилено.\nБудь ласка, зв’яжіться з адміністратором ( /adm ) або зробіть нове замовлення.',
        'hi_text':'👋 Привіт!\n💖 Вітаємо в магазині рідин!\n🛒 Paro Store\n😍 Тут ти знайдеш найкращі продукти!\n⚙️ Допомога ( /help )',
        'Not_Flood': "⚠️ Будь ласка, зачекайте перед повторною командою.",
        'cart_cleared_manual1':'🧺 Ваш кошик очищено.',
        'order_accept_notice':'✅ Ваше замовлення прийнято!  Дякуємо за покупку! 🛒',
        'send_photo_only': 'Будь ласка, надішліть саме фотографію, а не документ чи інший файл.',
        'webapp_intro': '🌟 Відкрийте наш новий Mini App для зручнішого шопінгу!\n\n✨ У Mini App ви знайдете:\n• Зручний каталог товарів\n• Швидкий пошук\n• Красивий інтерфейс\n• Легке оформлення замовлень\n\n👆 Натисніть кнопку нижче:',
        'open_webapp': '🛍️ Відкрити магазин',
        'classic_interface': '📱 Звичайний інтерфейс'
        
        
        
        
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

        'total': 'Разом',
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
        'open_webapp': '🛍️ Otwórz sklep',
        'classic_interface': '📱 Klasyczny interfejs'
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
        'open_webapp': '🛍️ Открыть магазин',
        'classic_interface': '📱 Классический интерфейс'
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
conn.commit()
import time
user_last_start = {}

# Додаємо команду для відкриття Mini App
@dp.message_handler(commands=['webapp'], state="*")
async def open_webapp(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or 'uk'
    
    # Створюємо кнопку з Mini App
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
        return  # !!! важливо: далі не йдемо, бо користувача ще нема в базі

    # -- нижче код тільки для тих, хто вже є в базі і має мову --
    if user_id in user_last_start:
        elapsed = current_time - user_last_start[user_id]
        if elapsed < 10:
            await message.answer(translations[lang]['Not_Flood'])
            return

    user_last_start[user_id] = current_time

    photo_path = 'photos/juja.gif'
    welcome_text = translations[lang]['hi_text']

    with open(photo_path, 'rb') as animation:
        await bot.send_animation(chat_id=message.chat.id, animation=animation, caption=welcome_text)

    await state.update_data(language=lang)

    # Основне меню з кнопкою Mini App
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
        markup.add(InlineKeyboardButton(translations[lang]['classic_interface'], callback_data='classic_interface'))

    await message.answer(
        "🛍️ Оберіть спосіб покупок:\n\n"
        "🌟 **Mini App** - новий красивий інтерфейс\n"
        "📱 **Звичайний** - класичні кнопки в Telegram",
        reply_markup=markup,
        parse_mode='Markdown'
    )



def save_user_language(user_id, username, lang_code):
    c.execute("INSERT OR REPLACE INTO users (id, username, language) VALUES (?, ?, ?)",
              (user_id, username, lang_code))
    conn.commit()
def get_user_language(user_id):
    c.execute("SELECT language FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    return row[0] if row else None

@dp.message_handler(commands=['adm'],state="*")
async def cmd_help(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or 'uk'  

    await message.answer(translations[lang]['help_contact_request'])
    await HelpFSM.waiting_for_help_contact.set()
def update_user_language(user_id, language_code):
    c.execute("UPDATE users SET language = ? WHERE id = ?", (language_code, user_id))
    conn.commit()

@dp.message_handler(commands=['ban'], user_id=ADMINS,state="*")
async def ban_user(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        await message.answer("Формат: /ban <user_id> <години>")
        return

    user_id = int(parts[1])
    hours = int(parts[2])
    banned_until = int(datetime.now(timezone.utc).timestamp()) + hours * 3600

    c.execute("INSERT INTO bans (user_id, banned_until) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET banned_until = ?",
              (user_id, banned_until, banned_until))
    conn.commit()

    await message.answer(f"Користувача {user_id} заблоковано на {hours} год.")
@dp.message_handler(commands=['unban'],state="*")
async def unban_user(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("⛔ У вас немає доступу до цієї команди.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("⚠️ Використання: /unban <user_id>")
        return

    user_id = int(parts[1])

    # Видаляємо бан з бази
    c.execute("UPDATE bans SET banned_until = 0 WHERE user_id = ?", (user_id,))

    conn.commit()

    await message.reply(f"✅ Користувач {user_id} розблокований.")
def is_user_banned(user_id: int) -> bool:
    result = c.execute("SELECT banned_until FROM bans WHERE user_id = ?", (user_id,)).fetchone()
    if result:
        banned_until = result[0]
        return int(datetime.now(timezone.utc).timestamp()) < banned_until
    return False 

@dp.message_handler(commands=['help'],state="*")
async def cmd_help(message: types.Message):
    lang = get_user_language(message.from_user.id)
    help_text = translations.get(lang, translations['uk'])['help_text']
    await message.answer(help_text)


from aiogram.dispatcher.filters.state import State, StatesGroup

class LanguageFSM(StatesGroup):
    choosing_language = State()


@dp.message_handler(commands=['language'],state="*")
async def cmd_language(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Українська"), KeyboardButton("Polski"), KeyboardButton("Русский"))
    await message.answer("Оберіть мову / Wybierz język / Выберите язык:", reply_markup=markup)
    await LanguageFSM.choosing_language.set()

@dp.message_handler(state=LanguageFSM.choosing_language)
async def process_language_choice(message: types.Message, state: FSMContext):
    text = message.text
    lang_map = {
        'Українська': 'uk',
        'Polski': 'en',
        'Русский': 'ru'
    }
    if text not in lang_map:
        await message.answer("Error")
        return

    new_lang = lang_map[text]
    update_user_language(message.from_user.id, new_lang)

    await message.answer(
        f"{translations[new_lang]['language_changed']}{text}.",
        reply_markup=ReplyKeyboardRemove()  
    )
    
    await state.finish()



@dp.message_handler(lambda message: message.text.lower() == '!db')
async def show_users_db(message: types.Message):

    try:
        users = c.execute("SELECT id, username, language FROM users").fetchall()
    except Exception as e:
        await message.reply(f"Помилка при доступі до бази: {e}")
        return

    if not users:
        await message.reply("База користувачів порожня.")
        return

    lines = []
    for i, (user_id, username, language) in enumerate(users, 1):
        lines.append(f"{i}. ID: {user_id}, Username: @{username or 'N/A'}, Language: {language}")

    msg_text = "\n".join(lines)

    # Надсилаємо повідомлення
    await message.reply(f"👥 Користувачі в базі:\n\n{msg_text}")


@dp.message_handler(commands=['send'],state="*")
async def admin_send_message(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("Error")
        return

    args = message.get_args()
    if not args:
        await message.reply("Використання:\n/send all <повідомлення>\nабо\n/send <user_id> <повідомлення>")
        return

    split_args = args.split(maxsplit=1)
    if len(split_args) < 2:
        await message.reply("Використання:\n/send all <повідомлення>\nабо\n/send <user_id> <повідомлення>")
        return

    target, text = split_args

    if target.lower() == "all":
        c.execute("SELECT id FROM users")
        users = c.fetchall()

        success = 0
        failed = 0
        for (user_id,) in users:
            try:
                await bot.send_message(user_id, text)
                success += 1
            except Exception:
                failed += 1
        await message.reply(f"Повідомлення надіслано {success} користувачам.\nНе вдалося надіслати: {failed}")
    else:
        if not target.isdigit():
            await message.reply("User ID має бути числом.")
            return

        user_id = int(target)
        c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        if not user:
            await message.reply("Користувача з таким ID не знайдено.")
            return

        try:
            await bot.send_message(user_id, text)
            await message.reply(f"Повідомлення надіслано користувачу {user_id}.")
        except Exception as e:
            await message.reply(f"Не вдалося надіслати повідомлення: {e}")

@dp.message_handler(state=HelpFSM.waiting_for_help_contact)
async def process_help_contact(message: types.Message, state: FSMContext):
    contact = message.text.strip()

    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"Користувач @{message.from_user.username} (ID {message.from_user.id}) просить допомоги.\n"
            f"Контакт для зв'язку: {contact}"
        )

    user_id = message.from_user.id
    lang = get_user_language(user_id) or 'uk'  

    await message.answer(translations[lang]['thanks_help'])
    await state.finish()

# Обробник для кнопки "Звичайний інтерфейс"
@dp.callback_query_handler(lambda c: c.data == 'classic_interface', state='*')
async def show_classic_interface(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = get_user_language(user_id) or 'uk'
    
    await state.update_data(language=lang)

    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    if not rows:
        await callback.message.edit_text("Категорії поки що відсутні.")
        return

    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'cat_{row[0]}'))

    await callback.message.edit_text(translations[lang]['category'], reply_markup=markup)
    await OrderFSM.choosing_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'), state=OrderFSM.choosing_language)
async def choose_language(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split('_')[1]
    user_id = callback.from_user.id
    username = callback.from_user.username or ''

    save_user_language(user_id, username, lang)
    await state.update_data(language=lang)

    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    if not rows:
        await callback.message.answer(translations[lang]['categories_empty'])
        return

    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'cat_{row[0]}'))

    await callback.message.edit_text(translations[lang]['category'], reply_markup=markup)
    await OrderFSM.choosing_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('cat_'), state=OrderFSM.choosing_category)
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    data = await state.get_data()
    lang = data['language']
    await state.update_data(category_id=cat_id)

    rows = c.execute(f"SELECT id, name_{lang}, quantity FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if not rows:
        await callback.message.answer(translations[lang]['no_products'])
        return

    markup = InlineKeyboardMarkup()
    for row in rows:
        prod_id, name, quantity = row
        if quantity > 0:
            markup.add(InlineKeyboardButton(f"{name}", callback_data=f'prod_{prod_id}'))
    markup.add(InlineKeyboardButton(translations[lang]['back'], callback_data='back_to_categories'))

    if not markup.inline_keyboard[:-1]:  
        await callback.message.answer(translations[lang]['no_products_available'])
        return

    await callback.message.delete()
    await bot.send_message(callback.from_user.id, translations[lang]['choose_liquid'], reply_markup=markup)

    await OrderFSM.choosing_product.set()


@dp.callback_query_handler(lambda c: c.data == 'back_to_categories', state=OrderFSM.choosing_product)
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['language']

    # 🧹 Видаляємо повідомлення з вибором ліквіду
    await callback.message.delete()

    # ⬅️ Створюємо клавіатуру з категоріями
    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'cat_{row[0]}'))

    # 📩 Надсилаємо нове повідомлення зі списком категорій
    await bot.send_message(callback.from_user.id, translations[lang]['category'], reply_markup=markup)

    await OrderFSM.choosing_category.set()
    await callback.answer()



@dp.callback_query_handler(lambda c: c.data.startswith('prod_'), state=OrderFSM.choosing_product)
async def choose_product(callback: types.CallbackQuery, state: FSMContext):
    prod_id = int(callback.data.split('_')[1])
    data = await state.get_data()
    lang = data.get('language', 'uk')
    user_id = callback.from_user.id
    
    if is_user_banned(user_id):
        await callback.answer(translations[lang]['banned_message'], show_alert=True)
        return

    product = c.execute(
        "SELECT name_{0}, description_{0}, price, photo, quantity FROM products WHERE id=?".format(lang),
        (prod_id,)
    ).fetchone()
    if not product:
        await callback.message.answer(translations[lang]['order_not_found'])
        return

    name, desc, price, photo, quantity = product
    if quantity <= 0:
        await callback.message.answer(translations[lang]['out_of_stock'])
        return

    await state.update_data(product_id=prod_id)

    cart = data.get('cart', {})  # cart = {prod_id: qty, ...}
    total_items = sum(cart.values()) if cart else 0

    # Формуємо текст кнопки "Кошик" з кількістю товарів, якщо є
    if total_items > 0:
        cart_text = f"{translations[lang]['cart_s']} ({total_items})"
    else:
        cart_text = translations[lang]['cart_s']

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(translations[lang]['add_to_cart_s'], callback_data='add_to_cart'),
        InlineKeyboardButton(translations[lang]['back'], callback_data='back_to_categories'),
        InlineKeyboardButton(cart_text, callback_data='show_cart')
    )

    photo_path = os.path.join(PHOTO_DIR, photo)
    await callback.message.delete()
    await bot.send_photo(
        user_id,
        InputFile(photo_path),
        caption=f"{name}\n\n{desc}\n\n{translations[lang]['price_label']} {price} zł",
        reply_markup=markup
    )
    await OrderFSM.confirming_product.set()


from asyncio import create_task, sleep, CancelledError

user_tasks = {}  


# async def release_reserved_items(user_id, state, manual_clear=False):
#     data = await state.get_data()
#     lang = data.get('language', 'uk')
#     cart = data.get('cart', {})
#     if not cart:
#         return
    
#     for prod_id, qty in cart.items():
#         c.execute("UPDATE products SET quantity = quantity + ? WHERE id=?", (qty, prod_id))
#     conn.commit()
#     await state.update_data(cart={})
#     await state.update_data(reservation_task_started=False)
#     if manual_clear:
#         await bot.send_message(user_id, translations[lang]['cart_cleared_manual1'])
#     else:
#         await bot.send_message(user_id, translations[lang]['cart_expired'])

# async def reservation_timer(user_id, state):
#     try:
#         await sleep(RESERVATION_TIME)
#         data = await state.get_data()
#         if data.get('cart'):
#             await release_reserved_items(user_id, state)
#             await state.update_data(reservation_task_started=False)
#     except CancelledError:
#         pass
#     finally:
#         user_tasks.pop(user_id, None)

@dp.callback_query_handler(lambda c: c.data == 'add_to_cart', state=OrderFSM.confirming_product)
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')
    cart = data.get('cart', {})
    prod_id = data.get('product_id')

    if prod_id is None:
        await callback.answer(translations[lang]['product_not_selected'], show_alert=True)
        return

    current_qty = c.execute("SELECT quantity FROM products WHERE id=?", (prod_id,)).fetchone()
    if current_qty is None:
        await callback.answer(translations[lang]['error_product_not_found'], show_alert=True)
        return

    available_qty = current_qty[0]
    already_in_cart = cart.get(prod_id, 0)

    if available_qty <= 0:
        await callback.answer(translations[lang]['error_out_of_stock'], show_alert=True)
        return

    #c.execute("UPDATE products SET quantity = quantity - 1 WHERE id=? AND quantity > 0", (prod_id,))
    #conn.commit()

    cart[prod_id] = already_in_cart + 1
    await state.update_data(cart=cart)

    await callback.answer(translations[lang]['product_added_to_cart'], show_alert=True)

    # Оновлення кнопки з кількістю товарів у кошику
    total_items = sum(cart.values())
    if total_items > 0:
        cart_text = f"{translations[lang]['cart_s']} ({total_items})"
    else:
        cart_text = translations[lang]['cart_s']

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(translations[lang]['add_to_cart_s'], callback_data='add_to_cart'),
        InlineKeyboardButton(translations[lang]['back'], callback_data='back_to_categories'),
        InlineKeyboardButton(cart_text, callback_data='show_cart')
    )

    # Оновлюємо клавіатуру у повідомленні із товаром
    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except Exception as e:
        # Якщо повідомлення видалене або не можна редагувати — просто ігноруємо
        print(f"Failed to update markup: {e}")

    task = user_tasks.get(callback.from_user.id)
    if task:
        task.cancel()
        try:
            await task
        except CancelledError:
            pass

    #user_tasks[callback.from_user.id] = create_task(reservation_timer(callback.from_user.id, state))


@dp.callback_query_handler(lambda c: c.data == 'clear_cart', state='*')
async def clear_cart(callback: types.CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get('language', 'uk')
    
    # Спочатку повертаємо зарезервовані товари на склад
    #await release_reserved_items(callback.from_user.id, state, manual_clear=True)
    
    # Очищуємо кошик в стані
    await state.update_data(cart={})
    
    await callback.answer(translations[lang]['cart_cleared'], show_alert=True)

    try:
        await bot.send_message(callback.from_user.id, translations[lang]['starts'])
        await callback.message.delete()  
    except Exception:
        pass



@dp.callback_query_handler(lambda c: c.data == 'show_cart', state='*')
async def show_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get('cart', {})
    lang = data.get('language', 'uk')

    if not cart:
        await callback.answer(translations[lang]['cart_empty'])
        return

    texts = []
    total = 0
    for prod_id, qty in cart.items():
        product = c.execute(
            "SELECT name_{0}, price FROM products WHERE id=?".format(lang),
            (prod_id,)
        ).fetchone()
        if product:
            name, price = product
            texts.append(f"{name} x {qty} = {price * qty} zł")
            total += price * qty

    cart_text = "\n".join(texts) + f"\n\n{translations[lang]['total_amount']} {total} zł"

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(translations[lang]['buy'], callback_data="start_order"),
        InlineKeyboardButton(translations[lang]['clear_cart'], callback_data="clear_cart")
    )
    await state.update_data(total=total)
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(cart_text, reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == 'start_order', state='*')
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')
    cart = data.get('cart', {})
    user_id = callback.from_user.id
    try:
        await callback.message.delete()  # видаляємо повідомлення з кошиком
    except Exception:
        pass
    if is_user_banned(user_id):
        await callback.answer(translations[lang]['banned_message'], show_alert=True)
        return
    if not cart:
        await callback.answer(translations[lang]['cart_empty'], show_alert=True)
        return

    await state.update_data(cart=cart)
    await OrderFSM.entering_name.set()

    user_id = callback.from_user.id
    row = c.execute("SELECT full_name FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if row and row[0]:
        keyboard.add(KeyboardButton(row[0]))

    await bot.send_message(user_id, translations[lang]['name'], reply_markup=keyboard)

    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == 'checkout', state=OrderFSM.confirming_product)
async def checkout(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')

    # Запускаємо анкету (початок замовлення)
    await callback.message.answer(translations[lang]['enter_name'])
    await OrderFSM.entering_name.set()

@dp.callback_query_handler(lambda c: c.data == 'back_to_categories', state=[OrderFSM.choosing_product, OrderFSM.confirming_product])
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['language']

    rows = c.execute(f"SELECT id, name_{lang} FROM categories").fetchall()
    if not rows:
        await callback.message.answer(translations[lang]['categories_empty'])
        return

    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'cat_{row[0]}'))

    await callback.message.delete()

    await callback.message.answer(translations[lang]['category'], reply_markup=markup)
    await OrderFSM.choosing_category.set()
    await callback.answer()





def get_user_button(user_id, field_name):
    row = c.execute(f"SELECT {field_name} FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    if row and row[0]:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(KeyboardButton(row[0]))
        return kb
    return ReplyKeyboardRemove()
class ExtendedOrderFSM(StatesGroup):
    entering_contact = State()
    choosing_payment = State()
    choosing_delivery = State()
    entering_pickup_date = State()
    entering_post_name = State()
    entering_post_phone = State()
    entering_post_email = State()
    entering_post_address = State()
    waiting_for_payment_screenshot = State()


@dp.callback_query_handler(lambda c: c.data == 'buy', state=OrderFSM.confirming_product)
async def buy_product(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = (await state.get_data()).get('language', 'uk')

    data = await state.get_data()
    print(f"User data: {data}")

    keyboard = get_user_button(user_id, "full_name")
    print(f"Keyboard buttons: {keyboard.inline_keyboard if keyboard else 'None'}")

    await bot.send_message(user_id, translations[lang]['name'], reply_markup=keyboard)
    await OrderFSM.entering_name.set()
   
@dp.message_handler(state=OrderFSM.entering_name)
async def enter_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()
    user_id = message.from_user.id
    await state.update_data(full_name=full_name)

    c.execute("INSERT INTO user_profiles (user_id, full_name) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET full_name=?",
              (user_id, full_name, full_name))
    conn.commit()

    lang = (await state.get_data()).get('language', 'uk')
    keyboard = get_user_button(user_id, "contact")
    await message.answer(translations[lang]['contact'], reply_markup=keyboard)
    await ExtendedOrderFSM.entering_contact.set()


@dp.message_handler(state=ExtendedOrderFSM.entering_contact)
async def enter_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    contact = message.text.strip()
    lang = (await state.get_data()).get('language', 'uk')

    if not (contact.startswith('@') or sum(char.isdigit() for char in contact) >= 9):
        await message.answer(translations[lang]['invalid_contact'])
        return

    await state.update_data(contact=contact)
    c.execute("INSERT INTO user_profiles (user_id, contact) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET contact=?", (user_id, contact, contact))
    conn.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(translations[lang]['pickup']), KeyboardButton(translations[lang]['paczkomat']))
    await message.answer(translations[lang]['delivery'], reply_markup=markup)
    await ExtendedOrderFSM.choosing_delivery.set()

@dp.message_handler(state=ExtendedOrderFSM.choosing_payment)
async def choose_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')
    tr = translations.get(lang, translations['uk'])

    method = message.text.strip().lower()
    valid_methods = [tr['cash'].lower(), tr['card'].lower()]

    if method not in valid_methods:
        await message.answer(tr['invalid_payment_method'])
        return

    await state.update_data(payment=method)

    # Визначаємо вартість з урахуванням доставки
    delivery = data.get('delivery', '').lower()
    price = data.get('total', 0)
    payment_info = f"{tr['payment_amount']} {price} zl."

    if method == tr['card'].lower():
        # Виводимо інформацію про оплату картою + суму
        await message.answer(f"{tr['payment_card_info']}\n\n{payment_info}")
        await ExtendedOrderFSM.waiting_for_payment_screenshot.set()
    else:
        # Якщо готівка, також виводимо суму для оплати
        await finish_order(message, state)

@dp.message_handler(content_types=['document'], state=ExtendedOrderFSM.waiting_for_payment_screenshot)
async def handle_payment_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')  
    tr = translations.get(lang, translations['uk'])

    document = message.document

    if document.mime_type != 'application/pdf':
        await message.answer("Будь ласка, надішліть саме PDF-файл або скріншот.")
        return

    pdf_file_id = document.file_id
    await state.update_data(payment_pdf_id=pdf_file_id)

    await finish_order(message, state)

@dp.message_handler(content_types=['photo'], state=ExtendedOrderFSM.waiting_for_payment_screenshot)
async def handle_payment_screenshot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')  
    tr = translations.get(lang, translations['uk'])

    photo_id = message.photo[-1].file_id
    await state.update_data(payment_photo_id=photo_id)

    await finish_order(message, state)
@dp.message_handler(lambda message: True, state=ExtendedOrderFSM.waiting_for_payment_screenshot)
async def invalid_screenshot_format(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language', 'uk')  
    tr = translations.get(lang, translations['uk'])

    await message.answer(tr.get('send_photo_only', 'Будь ласка, надішліть саме **фотографію**, а не документ чи інший файл.'))

@dp.message_handler(state=ExtendedOrderFSM.choosing_delivery)
async def choose_delivery(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get('language', 'uk')

    choice = message.text.strip().lower()
    if choice == translations[lang]['pickup'].lower():
        await state.update_data(delivery="pickup")
        
        await ExtendedOrderFSM.entering_pickup_date.set()
        row = c.execute("SELECT pickup_date FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if row and row[0]:
            keyboard.add(KeyboardButton(row[0]))

        await message.answer(translations[lang]['pickup_date'], reply_markup=keyboard)
        
    elif choice == translations[lang]['paczkomat'].lower():
        await state.update_data(delivery="post")
        
        # Отримуємо попереднє ім'я з бази
        row = c.execute("SELECT post_name FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if row and row[0]:
            keyboard.add(KeyboardButton(row[0]))
        
        await message.answer(translations[lang]['latin_name'], reply_markup=keyboard)
        await ExtendedOrderFSM.entering_post_name.set()

    else:
        await message.answer(translations[lang]['invalid_delivery_choice'])

@dp.message_handler(state=ExtendedOrderFSM.entering_pickup_date)
async def enter_pickup_date(message: types.Message, state: FSMContext):
    await state.update_data(pickup_date=message.text.strip())

    data = await state.get_data()
    lang = data.get('language', 'uk')
    tr = translations.get(lang, translations['uk'])

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(tr['cash']), KeyboardButton(tr['card']))

    await message.answer(tr['choose_payment_method'], reply_markup=markup)
    
    await ExtendedOrderFSM.choosing_payment.set()
    
@dp.message_handler(state=ExtendedOrderFSM.entering_contact)
async def enter_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    contact = message.text.strip()
    lang = (await state.get_data()).get('language', 'uk')

    if not (contact.startswith('@') or sum(char.isdigit() for char in contact) >= 9):
        await message.answer(translations[lang]['invalid_contact'])
        return

    await state.update_data(contact=contact)
    c.execute("INSERT INTO user_profiles (user_id, contact) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET contact=?", (user_id, contact, contact))
    conn.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(translations[lang]['pickup']), KeyboardButton(translations[lang]['paczkomat']))
    await message.answer(translations[lang]['delivery'], reply_markup=markup)
    await ExtendedOrderFSM.choosing_delivery.set()

@dp.message_handler(state=ExtendedOrderFSM.entering_contact)
async def enter_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    contact = message.text.strip()
    lang = (await state.get_data()).get('language', 'uk')

    if not (contact.startswith('@') or sum(char.isdigit() for char in contact) >= 9):
        await message.answer(translations[lang]['invalid_contact'])
        return

    await state.update_data(contact=contact)
    c.execute("INSERT INTO user_profiles (user_id, contact) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET contact=?", (user_id, contact, contact))
    conn.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(translations[lang]['pickup']), KeyboardButton(translations[lang]['paczkomat']))
    await message.answer(translations[lang]['delivery'], reply_markup=markup)
    await ExtendedOrderFSM.choosing_delivery.set()

@dp.message_handler(state=ExtendedOrderFSM.entering_post_name)
async def enter_post_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get('language', 'uk')

    await state.update_data(post_name=message.text.strip())

    keyboard = get_user_button(user_id, "post_phone")  

    await message.answer(translations[lang]['post_phone'], reply_markup=keyboard)
    await ExtendedOrderFSM.entering_post_phone.set()

@dp.message_handler(state=ExtendedOrderFSM.entering_post_phone)
async def enter_post_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = (await state.get_data()).get('language', 'uk')

    phone = message.text.strip()
    if sum(char.isdigit() for char in phone) < 9:
        await message.answer(translations[lang]['invalid_phone'])
        return

    await state.update_data(post_phone=phone)
    keyboard = get_user_button(user_id, "post_email")
    await message.answer(translations[lang]['email'], reply_markup=keyboard)
    await ExtendedOrderFSM.entering_post_email.set()

@dp.message_handler(state=ExtendedOrderFSM.entering_post_email)
async def enter_post_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = (await state.get_data()).get('language', 'uk')

    email = message.text.strip()
    if "@" not in email or "." not in email:
        await message.answer(translations[lang]['invalid_email'])
        return

    await state.update_data(post_email=email)
    keyboard = get_user_button(user_id, "post_address")
    await message.answer(translations[lang]['address'], reply_markup=keyboard)
    await ExtendedOrderFSM.entering_post_address.set()

@dp.message_handler(state=ExtendedOrderFSM.entering_post_address)
async def enter_post_address(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(post_address=message.text.strip())

    data = await state.get_data()
    lang = data.get('language', 'uk')
    tr = translations.get(lang, translations['uk'])

    delivery = data.get('delivery', '').lower()
    price = data.get('total', 0)
    if delivery == "post":
        price += 12  
    payment_info = f"{tr['payment_amount']} {price} zl."

    if delivery == "post":
        await state.update_data(payment=tr['card'])
        await message.answer(f"{tr['post_payment_notice']}\n\n{payment_info}")
        await ExtendedOrderFSM.waiting_for_payment_screenshot.set()
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton(tr['cash']), KeyboardButton(tr['card']))
        await message.answer(f"{tr['choose_payment_method']}\n\n{payment_info}", reply_markup=markup)
        await ExtendedOrderFSM.choosing_payment.set()
        

@dp.callback_query_handler(lambda c: c.data.startswith('order_accept_'))
async def admin_accept_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split('_')[-1])

    # Отримуємо всі товари і кількість з order_items
    items = c.execute("SELECT product_id, quantity FROM order_items WHERE order_id=?", (order_id,)).fetchall()
    if not items:
        await callback.answer("Замовлення не знайдено або без товарів.")
        return

    # Зменшуємо кількість товарів у products
    for product_id, quantity in items:
        c.execute("UPDATE products SET quantity = quantity - ? WHERE id=? AND quantity >= ?", (quantity, product_id, quantity))

    # Оновлюємо статус замовлення
    c.execute("UPDATE orders SET status = 'accepted' WHERE id=?", (order_id,))
    conn.commit()

    # Отримуємо user_id для можливого повідомлення
    user_row = c.execute("SELECT user_id FROM orders WHERE id=?", (order_id,)).fetchone()
    user_id = user_row[0] if user_row else None
    lang_row = c.execute("SELECT language FROM users WHERE id=?", (user_id,)).fetchone()
    lang = lang_row[0] if lang_row else 'uk'
    tr = translations.get(lang, translations['uk'])
    await callback.answer("Замовлення прийняте ✅")
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(callback.message.chat.id, f"Замовлення #{order_id} прийняте.")

    # За бажанням можна повідомити користувача, що його замовлення прийняте
    if user_id:
        try:
            await bot.send_message(user_id, tr['order_accept_notice'])
        except Exception as e:
            print(f"❗ Помилка при надсиланні повідомлення користувачу user_id={user_id}: {e}")


@dp.callback_query_handler(lambda c: c.data.startswith('order_reject_'))
async def admin_reject_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split('_')[-1])

    # Отримуємо user_id
    user_row = c.execute("SELECT user_id FROM orders WHERE id=?", (order_id,)).fetchone()
    if not user_row:
        await callback.answer("Замовлення не знайдено.")
        return
    user_id = user_row[0]

    # Отримуємо товари і кількість
    items = c.execute("SELECT product_id, quantity FROM order_items WHERE order_id=?", (order_id,)).fetchall()

    # Повертаємо кількість товарів на склад
    for product_id, quantity in items:
        c.execute("UPDATE products SET quantity = quantity + ? WHERE id=?", (quantity, product_id))

    # Оновлюємо статус замовлення
    c.execute("UPDATE orders SET status = 'rejected' WHERE id=?", (order_id,))
    conn.commit()

    # Отримуємо мову користувача для перекладу
    lang_row = c.execute("SELECT language FROM users WHERE id=?", (user_id,)).fetchone()
    lang = lang_row[0] if lang_row else 'uk'
    tr = translations.get(lang, translations['uk'])

    await callback.answer("Замовлення відхилене ❌")
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(callback.message.chat.id, f"Замовлення #{order_id} відхилене та кількість товару відновлена.")

    # Повідомлення користувачу про відхилення
    try:
        await bot.send_message(user_id, tr['order_rejected_notice'])
    except Exception as e:
        print(f"❗ Помилка при надсиланні повідомлення користувачу user_id={user_id}: {e}")




@dp.message_handler(state=ExtendedOrderFSM.waiting_for_payment_screenshot, content_types=types.ContentTypes.PHOTO)
async def receive_payment_screenshot(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(payment_screenshot=file_id)
    await finish_order(message, state)


async def finish_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    lang = data.get('language', 'uk')
    contact = data.get('contact')
    full_name = data.get('full_name')
    payment = data.get('payment')
    delivery = data.get('delivery', '')
    cart = data.get('cart', {})
    user_id = message.from_user.id
    data = await state.get_data()
    await save_user_profile(user_id, data)
    if not cart:
        await message.answer("Ваш кошик порожній.")
        return

    # Формуємо опис доставки
    if delivery == "pickup":
        delivery_info = f"Самовивіз\nДата: {data.get('pickup_date', '')}"
    elif delivery == "post":
        delivery_info = (
            f"Поштомат\nІмʼя: {data.get('post_name', '')}\n"
            f"Телефон: {data.get('post_phone', '')}\n"
            f"Email: {data.get('post_email', '')}\n"
            f"Адреса: {data.get('post_address', '')}"
        )
    else:
        delivery_info = "Не вказано"

    c.execute('''
        INSERT INTO orders (user_id, full_name, payment_method, status, contact, delivery, delivery_info)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, full_name, payment, 'pending', contact, delivery, delivery_info))
    conn.commit()

    order_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]

    total_sum = 0
    product_lines = []
    for prod_id, qty in cart.items():
        c.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                  (order_id, prod_id, qty))
        #c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ? AND quantity >= ?",
        #          (qty, prod_id, qty))

        # Отримуємо ім’я й ціну
        product = c.execute('''
    SELECT p.name_uk, p.price, c.name_uk 
    FROM products p 
    JOIN categories c ON p.category_id = c.id
    WHERE p.id=?
''', (prod_id,)).fetchone()

        if product:
            name, price, category_name = product
            product_lines.append(f"[{category_name}] {name} x {qty} = {price * qty} zł")
            total_sum += price * qty


    conn.commit()

    # Кнопки для адміна
    admin_markup = InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        InlineKeyboardButton(f"✅ Прийняти #{order_id}", callback_data=f'order_accept_{order_id}'),
        InlineKeyboardButton(f"❌ Відмовити #{order_id}", callback_data=f'order_reject_{order_id}')
    )

    # Якщо є квитанція
    payment_photo_id = data.get('payment_photo_id')
    if payment_photo_id:
        for admin_id in ADMINS:
            await bot.send_photo(
                admin_id,
                photo=payment_photo_id,
                caption=f"Квитанція від {full_name} (ID {user_id}) для замовлення #{order_id}"
            )
    payment_pdf_id = data.get('payment_pdf_id')
    if payment_pdf_id:
        for admin_id in ADMINS:
            await bot.send_document(
                admin_id,
                document=payment_pdf_id,
                caption=f"PDF-квитанція від {full_name} (ID {user_id}) для замовлення #{order_id}"
            )
    # Повідомлення адмінам
    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"📦 НОВЕ ЗАМОВЛЕННЯ #{order_id}\n\n"
            f"Імʼя: {full_name}\nКонтакт: {contact}\n"
            f"Товари:\n" + "\n".join(product_lines) + f"\n\nСума: {total_sum} zł\n"
            f"Оплата: {payment}\n"
            f"Спосіб доставки: {delivery_info}\n"
            f"Користувач: @{username if username else 'без username'}\nChat ID: {user_id}",
            
            
            reply_markup=admin_markup
        )

    

    if delivery == "post":
        await message.answer(translations[lang]['thanks_post'], reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(translations[lang]['thanks'], reply_markup=ReplyKeyboardRemove())
    await state.finish()

async def save_user_profile(user_id: int, data: dict):
    c.execute('''
        INSERT INTO user_profiles (user_id, full_name, contact, delivery, pickup_date,
                                   post_name, post_phone, post_email, post_address, payment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            full_name=excluded.full_name,
            contact=excluded.contact,
            delivery=excluded.delivery,
            pickup_date=excluded.pickup_date,
            post_name=excluded.post_name,
            post_phone=excluded.post_phone,
            post_email=excluded.post_email,
            post_address=excluded.post_address,
            payment=excluded.payment
    ''', (
        user_id,
        data.get('full_name'),
        data.get('contact'),
        data.get('delivery'),
        data.get('pickup_date'),
        data.get('post_name'),
        data.get('post_phone'),
        data.get('post_email'),
        data.get('post_address'),
        data.get('payment')
    ))
    conn.commit()



# -------------------- АДМІН ПАНЕЛЬ --------------------


@dp.message_handler(commands=['admin'], state='*')
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ Категорія", callback_data='admin_add_cat'),
        InlineKeyboardButton("➕ Товар", callback_data='admin_add_prod'),
        InlineKeyboardButton("➕ Додати кількість товару", callback_data='admin_add_quantity'),
        InlineKeyboardButton("➖ Відняти кількість товару", callback_data='admin_subtract_quantity'),
        InlineKeyboardButton("✏️ Редагувати товар", callback_data='admin_edit_prod'),
        InlineKeyboardButton("🗑️ Видалити товар", callback_data='admin_delete_prod'),
        InlineKeyboardButton("🗑️ Видалити категорію", callback_data='admin_delete_cat')  # Ось ця кнопка
    )
    await message.answer("🛠️ Панель адміністратора:", reply_markup=markup)
    await AdminFSM.choosing_action.set()

@dp.callback_query_handler(lambda c: c.data == 'admin_delete_cat', state=AdminFSM.choosing_action)
async def admin_delete_category_start(callback: types.CallbackQuery):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    if not rows:
        await callback.message.answer("Категорій немає для видалення.")
        await AdminFSM.choosing_action.set()  # повернутися до меню
        return
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'delcat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для видалення:", reply_markup=markup)
    await AdminFSM.deleting_category.set()

@dp.callback_query_handler(lambda c: c.data == 'admin_add_cat', state=AdminFSM.choosing_action)
async def admin_add_category(callback: types.CallbackQuery):
    await callback.message.answer("Надішли назви категорії через |: name_uk|name_en|name_ru")
    await AdminFSM.adding_category.set()

@dp.message_handler(state=AdminFSM.adding_category)
async def save_category(message: types.Message, state: FSMContext):
    try:
        name_uk, name_en, name_ru = message.text.split('|')
        c.execute("INSERT INTO categories (name_uk, name_en, name_ru) VALUES (?, ?, ?)", (name_uk, name_en, name_ru))
        conn.commit()
        await message.answer("✅ Категорія додана")
    except:
        await message.answer("❌ Помилка. Перевір формат")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'admin_add_prod', state=AdminFSM.choosing_action)
async def admin_add_product(callback: types.CallbackQuery, state: FSMContext):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'selcat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для товару:", reply_markup=markup)
    await AdminFSM.choosing_product_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('selcat_'), state=AdminFSM.choosing_product_category)
async def admin_select_product_category(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    await state.update_data(category_id=cat_id)
    await callback.message.answer("Введи назви товару через |: name_uk|name_en|name_ru")
    await AdminFSM.adding_product_name.set()

@dp.message_handler(state=AdminFSM.adding_product_name)
async def admin_product_name(message: types.Message, state: FSMContext):
    try:
        name_uk, name_en, name_ru = message.text.split('|')
        await state.update_data(name_uk=name_uk, name_en=name_en, name_ru=name_ru)
        await message.answer("Опис через |: desc_uk|desc_en|desc_ru")
        await AdminFSM.adding_product_description.set()
    except:
        await message.answer("❌ Формат помилковий")
        await state.finish()

@dp.message_handler(state=AdminFSM.adding_product_description)
async def admin_product_description(message: types.Message, state: FSMContext):
    try:
        desc_uk, desc_en, desc_ru = message.text.split('|')
        await state.update_data(description_uk=desc_uk, description_en=desc_en, description_ru=desc_ru)
        await message.answer("Введи ціну в zł")
        await AdminFSM.adding_product_price.set()
    except:
        await message.answer("❌ Формат опису помилковий")
        await state.finish()

@dp.message_handler(state=AdminFSM.adding_product_price)
async def admin_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await message.answer("Введи кількість")
    await AdminFSM.adding_product_quantity.set()

@dp.message_handler(state=AdminFSM.adding_product_quantity)
async def admin_product_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=int(message.text))
    await message.answer("Надішли фото товару")
    await AdminFSM.adding_product_photo.set()

@dp.message_handler(content_types=['photo'], state=AdminFSM.adding_product_photo)
async def admin_product_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = f"{file_id}.jpg"
    full_path = os.path.join(PHOTO_DIR, filename)
    await bot.download_file(file_path, full_path)

    c.execute("INSERT INTO products (category_id, name_uk, name_en, name_ru, description_uk, description_en, description_ru, price, quantity, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (data['category_id'], data['name_uk'], data['name_en'], data['name_ru'],
               data['description_uk'], data['description_en'], data['description_ru'],
               data['price'], data['quantity'], filename))
    conn.commit()
    await message.answer("✅ Товар додано")
    await state.finish()
@dp.callback_query_handler(lambda c: c.data == 'admin_edit_prod', state=AdminFSM.choosing_action)
async def admin_edit_product_start(callback: types.CallbackQuery):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'editcat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для редагування товару:", reply_markup=markup)
    await AdminFSM.choosing_product_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('editcat_'), state=AdminFSM.choosing_product_category)
async def admin_edit_choose_product(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    await state.update_data(category_id=cat_id)
    products = c.execute("SELECT id, name_uk FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if not products:
        await callback.message.answer("У цій категорії немає товарів.")
        await state.finish()
        return
    markup = InlineKeyboardMarkup()
    for prod in products:
        markup.add(InlineKeyboardButton(prod[1], callback_data=f'editprod_{prod[0]}'))
    await callback.message.answer("Оберіть товар для редагування:", reply_markup=markup)
    await AdminFSM.selecting_product_for_edit.set()

@dp.callback_query_handler(lambda c: c.data.startswith('editprod_'), state=AdminFSM.selecting_product_for_edit)
async def admin_edit_choose_field(callback: types.CallbackQuery, state: FSMContext):
    prod_id = int(callback.data.split('_')[1])
    await state.update_data(product_id=prod_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Назва (укр)", callback_data='edit_name_uk'),
        InlineKeyboardButton("Назва (анг)", callback_data='edit_name_en'),
        InlineKeyboardButton("Назва (ру)", callback_data='edit_name_ru'),
        InlineKeyboardButton("Опис (укр)", callback_data='edit_desc_uk'),
        InlineKeyboardButton("Опис (анг)", callback_data='edit_desc_en'),
        InlineKeyboardButton("Опис (ру)", callback_data='edit_desc_ru'),
        InlineKeyboardButton("Ціна", callback_data='edit_price'),
        InlineKeyboardButton("Кількість", callback_data='edit_quantity')
    )
    await callback.message.answer("Оберіть поле для редагування:", reply_markup=markup)
    await AdminFSM.editing_product_field.set()

@dp.callback_query_handler(lambda c: c.data.startswith('edit_'), state=AdminFSM.editing_product_field)
async def admin_edit_enter_new_value(callback: types.CallbackQuery, state: FSMContext):
    field_key = callback.data[5:]  # наприклад, 'name_uk' або 'desc_en'
    await state.update_data(edit_field=field_key)
    await callback.message.answer(f"Введіть нове значення для {field_key}:")
    await AdminFSM.entering_new_value.set()
@dp.message_handler(Command("count"))
async def handle_count_command(message: types.Message):
    if message.from_user.id not in ADMINS:
        
        return

    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    c.execute("SELECT name_uk, quantity FROM products")
    products = c.fetchall()
    conn.close()

    if not products:
        await message.answer("📦 У базі немає товарів.")
        return

    lines = [f"{name} — {qty}" for name, qty in products]
    response = "📊 Кількість товарів:\n\n" + "\n".join(lines)

    await message.answer(response)
@dp.message_handler(state=AdminFSM.entering_new_value)
async def admin_edit_save_new_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    prod_id = data['product_id']
    field_key = data['edit_field']
    
    field_map = {
        'name_uk': 'name_uk',
        'name_en': 'name_en',
        'name_ru': 'name_ru',
        'desc_uk': 'description_uk',
        'desc_en': 'description_en',
        'desc_ru': 'description_ru',
        'price': 'price',
        'quantity': 'quantity'
    }
    
    if field_key not in field_map:
        await message.answer("Невідоме поле для редагування.")
        await state.finish()
        return
    
    db_field = field_map[field_key]
    new_value = message.text
    
    # Перевірка типів
    if db_field == 'price':
        try:
            new_value = float(new_value)
        except:
            await message.answer("Помилка: введіть число для ціни")
            return
    elif db_field == 'quantity':
        try:
            new_value = int(new_value)
        except:
            await message.answer("Помилка: введіть ціле число для кількості")
            return
    
    c.execute(f"UPDATE products SET {db_field}=? WHERE id=?", (new_value, prod_id))
    conn.commit()
    await message.answer("✅ Значення оновлено")
    await state.finish()

# --- Додати кількість ---
@dp.callback_query_handler(lambda c: c.data == 'admin_add_quantity', state=AdminFSM.choosing_action)
async def admin_add_quantity_start(callback: types.CallbackQuery):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'addqtycat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для додавання кількості товару:", reply_markup=markup)
    await AdminFSM.choosing_product_category.set()
# --- Відняти кількість ---

@dp.callback_query_handler(lambda c: c.data == 'admin_subtract_quantity', state=AdminFSM.choosing_action)
async def admin_subtract_quantity_start(callback: types.CallbackQuery):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'subqtycat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для віднімання кількості товару:", reply_markup=markup)
    await AdminFSM.choosing_product_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('subqtycat_'), state=AdminFSM.choosing_product_category)
async def admin_sub_quantity_choose_product(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    await state.update_data(category_id=cat_id)
    products = c.execute("SELECT id, name_uk, quantity FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if not products:
        await callback.message.answer("У цій категорії немає товарів.")
        await state.finish()
        return
    markup = InlineKeyboardMarkup()
    for prod in products:
        markup.add(InlineKeyboardButton(f"{prod[1]} (Зараз: {prod[2]})", callback_data=f'subqtyprod_{prod[0]}'))
    await callback.message.answer("Оберіть товар, з якого хочете відняти кількість:", reply_markup=markup)
    await AdminFSM.selecting_product_for_quantity_sub.set()
@dp.callback_query_handler(lambda c: c.data.startswith('subqtyprod_'), state=AdminFSM.selecting_product_for_quantity_sub)
async def admin_sub_quantity_enter(callback: types.CallbackQuery, state: FSMContext):
    prod_id = int(callback.data.split('_')[1])
    await state.update_data(product_id=prod_id)
    await callback.message.answer("Введіть кількість, яку хочете відняти:")
    await AdminFSM.entering_quantity_to_sub.set()
@dp.message_handler(state=AdminFSM.entering_quantity_to_sub)
async def admin_sub_quantity_save(message: types.Message, state: FSMContext):
    try:
        sub_qty = int(message.text)
        if sub_qty < 0:
            raise ValueError("Negative number")

        data = await state.get_data()
        prod_id = data['product_id']

        current_qty = c.execute("SELECT quantity FROM products WHERE id=?", (prod_id,)).fetchone()[0]
        if sub_qty > current_qty:
            await message.answer(f"❌ У товарі лише {current_qty} шт. Неможливо відняти {sub_qty}.")
        else:
            c.execute("UPDATE products SET quantity = quantity - ? WHERE id=?", (sub_qty, prod_id))
            conn.commit()
            await message.answer("✅ Кількість оновлено")
    except:
        await message.answer("❌ Введіть коректне ціле додатне число")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('addqtycat_'), state=AdminFSM.choosing_product_category)
async def admin_add_quantity_choose_product(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    await state.update_data(category_id=cat_id)
    products = c.execute("SELECT id, name_uk, quantity FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if not products:
        await callback.message.answer("У цій категорії немає товарів.")
        await state.finish()
        return
    markup = InlineKeyboardMarkup()
    for prod in products:
        markup.add(InlineKeyboardButton(f"{prod[1]} (Зараз: {prod[2]})", callback_data=f'addqtyprod_{prod[0]}'))
    await callback.message.answer("Оберіть товар, до якого хочете додати кількість:", reply_markup=markup)
    await AdminFSM.selecting_product_for_quantity_add.set()

@dp.callback_query_handler(lambda c: c.data.startswith('addqtyprod_'), state=AdminFSM.selecting_product_for_quantity_add)
async def admin_add_quantity_enter(callback: types.CallbackQuery, state: FSMContext):
    prod_id = int(callback.data.split('_')[1])
    await state.update_data(product_id=prod_id)
    await callback.message.answer("Введіть кількість, яку хочете додати:")
    await AdminFSM.entering_quantity_to_add.set()

@dp.message_handler(state=AdminFSM.entering_quantity_to_add)
async def admin_add_quantity_save(message: types.Message, state: FSMContext):
    try:
        add_qty = int(message.text)
        data = await state.get_data()
        prod_id = data['product_id']
        c.execute("UPDATE products SET quantity = quantity + ? WHERE id=?", (add_qty, prod_id))
        conn.commit()
        await message.answer("✅ Кількість оновлено")
    except:
        await message.answer("❌ Введіть коректне ціле число")
    await state.finish()

# --- Видалення товару ---
@dp.callback_query_handler(lambda c: c.data == 'admin_delete_prod', state=AdminFSM.choosing_action)
async def admin_delete_product_start(callback: types.CallbackQuery):
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'delcat_{row[0]}'))
    await callback.message.answer("Оберіть категорію для видалення товару:", reply_markup=markup)
    await AdminFSM.choosing_product_category.set()

@dp.callback_query_handler(lambda c: c.data.startswith('delcat_'), state=AdminFSM.choosing_product_category)
async def admin_delete_choose_product(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    await state.update_data(category_id=cat_id)
    products = c.execute("SELECT id, name_uk FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if not products:
        await callback.message.answer("У цій категорії немає товарів.")
        await state.finish()
        return
    markup = InlineKeyboardMarkup()
    for prod in products:
        markup.add(InlineKeyboardButton(prod[1], callback_data=f'delprod_{prod[0]}'))
    await callback.message.answer("Оберіть товар для видалення:", reply_markup=markup)
    await AdminFSM.selecting_product_for_delete.set()

@dp.callback_query_handler(lambda c: c.data.startswith('delprod_'), state=AdminFSM.selecting_product_for_delete)
async def admin_delete_confirm(callback: types.CallbackQuery, state: FSMContext):
    prod_id = int(callback.data.split('_')[1])
    await state.update_data(product_id=prod_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Так, видалити", callback_data='confirm_delete_yes'),
        InlineKeyboardButton("Ні, скасувати", callback_data='confirm_delete_no')
    )
    await callback.message.answer("Ви впевнені, що хочете видалити цей товар?", reply_markup=markup)
    await AdminFSM.confirming_delete.set()

@dp.callback_query_handler(lambda c: c.data.startswith('confirm_delete_'), state=AdminFSM.confirming_delete)
async def admin_delete_execute(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'confirm_delete_yes':
        data = await state.get_data()
        prod_id = data['product_id']
        c.execute("DELETE FROM products WHERE id=?", (prod_id,))
        conn.commit()
        await callback.message.answer("✅ Товар видалено.")
    else:
        await callback.message.answer("Видалення скасовано.")
    await state.finish()

@dp.message_handler(commands=['admin_delete_category'], state='*')
async def admin_delete_category_start(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    rows = c.execute("SELECT id, name_uk FROM categories").fetchall()
    if not rows:
        await message.answer("Категорій немає для видалення.")
        return
    markup = InlineKeyboardMarkup()
    for row in rows:
        markup.add(InlineKeyboardButton(row[1], callback_data=f'delcat_{row[0]}'))
    await message.answer("Оберіть категорію для видалення:", reply_markup=markup)
    await AdminFSM.deleting_category.set()

# Обробка вибору категорії для видалення
@dp.callback_query_handler(lambda c: c.data.startswith('delcat_'), state=AdminFSM.deleting_category)
async def admin_delete_category_confirm(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[1])
    # Перевірка чи є товари в категорії
    products = c.execute("SELECT id FROM products WHERE category_id=?", (cat_id,)).fetchall()
    if products:
        # Якщо є товари — питаємо підтвердження видалення разом із товарами
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Так, видалити категорію і всі товари", callback_data=f'confirm_delcat_yes_{cat_id}'),
            InlineKeyboardButton("Ні, скасувати", callback_data='confirm_delcat_no')
        )
        await callback.message.answer(
            "У цій категорії є товари. Ви впевнені, що хочете видалити категорію та всі її товари?",
            reply_markup=markup
        )
    else:
        # Якщо товарів немає — просто підтвердження видалення категорії
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Так, видалити категорію", callback_data=f'confirm_delcat_yes_{cat_id}'),
            InlineKeyboardButton("Ні, скасувати", callback_data='confirm_delcat_no')
        )
        await callback.message.answer("Ви впевнені, що хочете видалити цю категорію?", reply_markup=markup)

# Виконання видалення
@dp.callback_query_handler(lambda c: c.data.startswith('confirm_delcat_'), state=AdminFSM.deleting_category)
async def admin_delete_category_execute(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'confirm_delcat_no':
        await callback.message.answer("Видалення категорії скасовано.")
        await state.finish()
        return

    # confirm_delcat_yes_{cat_id}
    cat_id = int(callback.data.split('_')[-1])

    # Видаляємо товари категорії (якщо є)
    c.execute("DELETE FROM products WHERE category_id=?", (cat_id,))
    # Видаляємо категорію
    c.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()

    await callback.message.answer("✅ Категорію та всі її товари видалено.")
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
