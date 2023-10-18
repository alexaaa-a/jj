import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("5754325559:AAGwGVgqSp30mpiw84F_E1VaMdYu4E3CZrI",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Маленький опрос про _Вас_"
text_button_1 = "Математика. `Интегралы`"
text_button_2 = "Математика. `Производные`"
text_button_3 = "Математика. `Пределы последовательности`"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Это бот *Артёма Мясникова* и я очень хочу помогать людям ;) ',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Тааак, ну что, начнём?! *Ваше* _имя_? [Видео на приятную музыку](https://www.youtube.com/watch?v=ZbZSe6N_BXs)')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Красивое :) \n Твоё отношение к математике?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за ответ!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Интегралы :)](https://www.youtube.com/watch?v=2lFUgZjhOH8)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Производные :)](https://www.youtube.com/watch?v=sSnyhOXFLqc)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Пределы последовательности :)](https://www.youtube.com/watch?v=ZmwdHAhVsPM)", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()