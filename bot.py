import telebot
from telebot import types
from main import *

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

element = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, """Привет. Я - бот, строящий график полураспада некоторых (многих) элементов.
Для того чтобы начать, напиши порядковый номер элемента.""")

@bot.message_handler(commands=['list'])
def send_list(message):
	bot.send_message(message.chat.id, "Список элементов:\n" + "\n".join([f"{elem['name']} ({elem['symbol']}) - {elem['number']}" for elem in elements]))

@bot.message_handler(func=lambda m: True)
def elem_faq(message):
    global element
    if message.text not in numbers:
        bot.send_message(message.chat.id, "Элемент не найден. Проверь правильность ввода или попробуй другой.")
    else:
        element = Element(message.text)
        bot.reply_to(message, element)
        bot.send_message(message.chat.id, "Введи любую точку...")
        bot.register_next_step_handler(message, send_graph)

def send_graph(message):
    point = eval(message.text) 
    if point < 0:
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуй еще раз.")
        bot.register_next_step_handler(message, send_graph)
    
    plotter = Plotter(eval(message.text), element())
    img = plotter.create_plot()
    bot.send_photo(message.chat.id, open(element.symbol + str(eval(message.text)) + ".png", 'rb'))

 
bot.polling()