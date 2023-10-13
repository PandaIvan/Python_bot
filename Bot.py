import telebot
from telebot import types

TOKEN = 'Написать токен бота'




bot = telebot.TeleBot(TOKEN)


categories = {
    'Продукты': 0,
    'Транспорт': 0,
    'Развлечение': 0,
    'Подписки': 0,
    'Зарплата': 0,
    'Дом и химия': 0
}

@bot.message_handler(commands=['start'])
def start(message):
    # Приветственное сообщение
    response = "Привет! Я чат-бот для учета финансовых расходов и доходов.\n" \
               "Доступные категории:\n" \
               "- Продукты\n" \
               "- Транспорт\n" \
               "- Развлечение\n" \
               "- Подписки\n" \
               "- Зарплата\n" \
               "- Дом и химия\n\n" \
               "Для внесения данных используйте команды:\n" \
               "/add"

    bot.reply_to(message, response)

@bot.message_handler(commands=['add'])
def add_transaction(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        markup.add(category)

    msg = bot.reply_to(message, "Выберите категорию:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_category)

def process_category(message):
    category = message.text
    if category in categories:
        bot.send_message(message.chat.id, f"Вы выбрали категорию: {category}")
        user_data = {'category': category}
        bot.reply_to(message, "Введите сумму:")
        bot.register_next_step_handler(message, process_amount, user_data)
    else:
        bot.reply_to(message, "Неверная категория")

def process_amount(message, user_data):
    try:
        amount = float(message.text)
        category = user_data['category']
        if category == 'Зарплата':
            categories[category] += amount
            bot.reply_to(message, f"Зарплата успешно добавлена: {amount}")
        else:
            categories[category] -= amount
            bot.reply_to(message, f"Расходы в категории '{category}' успешно добавлены: {amount}")
    except ValueError:
        bot.reply_to(message, "Неверный формат суммы")

@bot.message_handler(commands=['total'])
def show_total(message):
    total_expenses = sum(categories.values()) - categories['Зарплата']
    response = "Общий итог:\n" \
               f"Зарплата: {categories['Зарплата']}\n" \
               f"Продукты: {categories['Продукты']}\n" \
               f"Транспорт: {categories['Транспорт']}\n" \
               f"Развлечение: {categories['Развлечение']}\n" \
               f"Подписки: {categories['Подписки']}\n" \
               f"Дом и химия: {categories['Дом и химия']}\n\n" \
               f"Итог: {total_expenses}"

    bot.reply_to(message, response)

bot.polling()
