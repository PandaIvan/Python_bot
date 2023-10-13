import telebot
import datetime
import pytz
import random

TOKEN = 'нужен токен бота'

#Бот для планировщик для личного пользования

HELP = """/help - command list.
/add - add a task.
/show - show tasks.
/random - random fun.
/time - look at the time.
/clean - delete tasks for today.
/trans - move tasks from tomorrow to today."""

RANDOM_TASKS = ['get drunk', 'read a book', 'play a game', 'walk for an hour']

bot = telebot.TeleBot(TOKEN)

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

tasks = {
    str(today): [],
    str(tomorrow): []
}

date_options = {
    'today': today,
    'tomorrow': tomorrow
}

user_state = {}


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['add'])
def add_task(message):
    chat_id = message.chat.id

    date_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    date_markup.add('Today', 'Tomorrow')

    msg = bot.reply_to(message, "Select the date:", reply_markup=date_markup)
    bot.register_next_step_handler(msg, process_date)


def process_date(message):
    chat_id = message.chat.id
    date = message.text.lower()

    if date in date_options:
        user_state[chat_id] = {'date': date}
        bot.reply_to(message, "Enter the task description:")
    else:
        bot.reply_to(message, "Invalid date. Task not added.")


@bot.message_handler(func=lambda message: message.chat.id in user_state and 'date' in user_state[message.chat.id])
def process_task(message):
    chat_id = message.chat.id
    date = user_state[chat_id]['date']
    task_text = message.text.strip()

    if task_text:
        selected_date = date_options[date]
        task_list = tasks[str(selected_date)]
        task_list.append(task_text)
        task_index = len(task_list)
        bot.reply_to(message, f"Task added successfully. Index: {task_index}")
    else:
        bot.reply_to(message, "Task description cannot be empty.")

    user_state.pop(chat_id)


@bot.message_handler(commands=['show'])
def show_tasks(message):
    chat_id = message.chat.id
    date_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    date_markup.add('Today', 'Tomorrow')

    msg = bot.reply_to(message, "Select the date to show tasks:", reply_markup=date_markup)
    bot.register_next_step_handler(msg, process_show_date)


def process_show_date(message):
    chat_id = message.chat.id
    date = message.text.lower()

    if date in date_options:
        selected_date = date_options[date]
        task_list = tasks[str(selected_date)]
        if task_list:
            response = f"Tasks for {selected_date}:\n"
            for index, task in enumerate(task_list, start=1):
                response += f"{index}. {task}\n"
        else:
            response = f"No tasks for {selected_date}."
    else:
        response = "Invalid date. Please use 'today' or 'tomorrow'."

    bot.reply_to(message, response)


@bot.message_handler(commands=['random'])
def add_random_task(message):
    chat_id = message.chat.id
    random_task = random.choice(RANDOM_TASKS)
    tasks[str(today)].append(random_task)
    bot.reply_to(message, f"Random task added to today's list: {random_task}")


@bot.message_handler(commands=['time'])
def show_time(message):
    chat_id = message.chat.id

    tz_thailand = pytz.timezone('Asia/Bangkok')
    tz_moscow = pytz.timezone('Europe/Moscow')
    tz_kiev = pytz.timezone('Europe/Kiev')

    time_thailand = datetime.datetime.now(tz_thailand).strftime('%H:%M:%S')
    time_moscow = datetime.datetime.now(tz_moscow).strftime('%H:%M:%S')
    time_kiev = datetime.datetime.now(tz_kiev).strftime('%H:%M:%S')

    response = f"Time:\nThailand: {time_thailand}\nMoscow: {time_moscow}\nKiev: {time_kiev}"
    bot.reply_to(message, response)


@bot.message_handler(commands=['clean'])
def clean_tasks(message):
    chat_id = message.chat.id
    tasks[str(today)] = []
    bot.reply_to(message, "Tasks for today have been deleted.")


@bot.message_handler(commands=['trans'])
def move_tasks(message):
    chat_id = message.chat.id
    tasks[str(today)] += tasks[str(tomorrow)]
    tasks[str(tomorrow)] = []
    bot.reply_to(message, "Tasks moved from tomorrow to today.")


bot.polling(none_stop=True)
