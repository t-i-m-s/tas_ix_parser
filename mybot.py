import telebot
from telebot import types
from telebot.types import Message
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
idea1 = [30]#256370991
idea = [8]#544463656
ID = []
call_title = []
site_check = []
film_check = []
sites = [['http://kinotasx.uz/search.php?keywords=','&video-id=']]
names = []
finish_names = []
hrefs = []
#-------------------------------------------------------------------------------
TOKEN = '1007184768:AAFjwERR1Mz0KinRny5EkTh7FVR9EnV4cI4'
bot = telebot.TeleBot(TOKEN)
#-------------------------------------------------------------------------------
headers = {'accept': '*/*' , 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
base_url = 'http://tasix.sarkor.uz/cgi-bin/checker.py?site='
# base_url = 'https://mover.uz/video/anime/'
#-------------------------------------------------------------------------------
#ID = open('ID.txt', 'w')

@bot.message_handler(commands=['start'])
def welcome(message):
    #ID.write(str(message.chat.id))
    #sti = open('C1.webp', 'rb')
    #bot.send_sticker(message.chat.id, sti)
    ID.insert(0,message.chat.id)
    markup =  types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Продолжить ➡️", callback_data='next')
    markup.add(button1)
    bot.send_message(ID[0], "Добро пожаловать!", reply_markup=markup)
    # bot.send_message(256370991, ID[0])
    # print(message)
    #ID.close()
@bot.message_handler(regexp=r"['][a-z0-9-A-Zа-яА-ЯёЁ]+[.][a-z0-9A-Z]+[']")#content_types=['text']   regexp="['][a-z0-9A-Z]+[.][a-z0-9A-Z]+[']"
def answer(message):
    site_check.insert(0, base_url + re.split(r"'",message.text)[1])

    def mover_parse(headers, site_check):
        session = requests.Session()
        request = session.get(site_check, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            divs = soup.find_all('p', attrs = {'class': 'success'})

        markupofsite = types.InlineKeyboardMarkup()
        markupofsite.add( types.InlineKeyboardButton(text = "⬅️ Вернуться к меню", callback_data = 'back'))

        if len(divs) > 0:
            bot.send_message(message.chat.id, "Сайт " + re.split(r"'",message.text)[1] + " входит в сеть TAS-IX! ✔", reply_markup=markupofsite)
        else:
            bot.send_message(message.chat.id, "Сайт " + re.split(r"'",message.text)[1] + " НЕ входит в сеть TAS-IX! ❌", reply_markup=markupofsite)

    mover_parse(headers, site_check[0])

@bot.message_handler(regexp=r"[!][a-z0-9-A-Z а-яА-ЯёЁ]+[!]")#content_types=['text']   regexp="['][a-z0-9A-Z]+[.][a-z0-9A-Z]+[']"
def answer_1(message):
	print('something!')
	film_check.insert(0, message.text)

	message.text = message.text.replace(" ","+")

	film_check.insert(0, sites[0][0] + re.split(r"!", message.text)[1] + sites[0][1])


	def mover_parse_1(headers, checkfilm):
		session = requests.Session()
		request = session.get(checkfilm, headers=headers)
		if request.status_code == 200:
			soup = bs(request.content, 'html.parser')
			divs = soup.find_all('a', attrs={'class': 'ellipsis'})#r"[!][a-z0-9-A-Z а-яА-ЯёЁ]+[!]"
		for i in divs:
			names.append(i.get('title'))
			hrefs.append(i.get('href'))
		if len(names) == 0:
			markup =  types.InlineKeyboardMarkup()
			markup.add( types.InlineKeyboardButton(text="⬅️ Вернуться к меню", callback_data='back'))
			bot.send_message(message.chat.id, "Увы ничего не найдено :( Поробуйте другое название", reply_markup=markup)

		elif len(names) < 9:
			markup =  types.InlineKeyboardMarkup()
			for i in range(0,len(names)):
				# markup.add(types.InlineKeyboardButton(names[i], callback_data=None))
				markup.add(types.InlineKeyboardButton(text=names[i], url=hrefs[i]))
			markup.add( types.InlineKeyboardButton(text="⬅️ Вернуться к меню", callback_data='back'))
			bot.send_message(message.chat.id, "Готовый список : ", reply_markup=markup)
			names.clear()
			hrefs.clear()

		else:
			markup =  types.InlineKeyboardMarkup()
			for i in range(0,8):
				# markup.add(types.InlineKeyboardButton(names[i], callback_data=None))
				markup.add(types.InlineKeyboardButton(text=names[i], url=hrefs[i]))
			markup.add( types.InlineKeyboardButton(text="⬅️ Вернуться к меню", callback_data='back'))
			bot.send_message(message.chat.id, "Готовый список : ", reply_markup=markup)
			names.clear()
			hrefs.clear()

	mover_parse_1(headers, film_check[0])

	#markupMOVER = types.InlineKeyboardMarkup()
	#markupMOVER.add( types.InlineKeyboardButton(text = tims1[0], url = tims1[1])

    # def mover_parse(headers, film_check):
    #     session = requests.Session()
    #     request = session.get(film_check, headers=headers)
    #     if request.status_code == 200:
    #         soup = bs(request.content, 'html.parser')
    #         divs = soup.find_all('a', attrs = {'title': r"[!][a-z0-9-A-Z а-яА-ЯёЁ]+[!]"})

            # markupofsite = types.InlineKeyboardMarkup()
            # markupofsite.add( types.InlineKeyboardButton(text = "⬅️ Вернуться к меню", callback_data = 'back'))
            # try:
    # bot.edit_message_text(chat_id=256370991, message_id=call_title[0], text="Подождите, информация обрабатывается!")
        # except IndexError:
        #     bot.edit_message_text(chat_id=256370991, message_id=call.message.message_id, text="Подождите, информация обрабатывается!")

@bot.callback_query_handler(func=lambda call: True)
def welcome_first(call):
    if call.data == 'next':
        markup =  types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Найти фильм в Tas-ix!", callback_data='check_film')
        button2 = types.InlineKeyboardButton("Tas-ix проверка!", callback_data='check_site')
        button3 = types.InlineKeyboardButton("----------", callback_data='clock')
        markup.add(button1,button2)
        markup.add(button3)
        bot.edit_message_text(chat_id=ID[0], message_id=call.message.message_id, text="Выберите один из разделов:", reply_markup=markup)
    elif call.data == 'check_film':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add( types.InlineKeyboardButton(text = "⬅️ Вернуться к меню", callback_data = 'back'))
        bot.edit_message_text(chat_id=256370991, message_id=call.message.message_id, text="""Отправьте название фильма или ключевое слово вида :
!пример фильма!""", reply_markup=markup2)
        # markup2 =  types.InlineKeyboardMarkup()
        # button1 = types.InlineKeyboardButton("Рэп",callback_data='but1')
        # button2 = types.InlineKeyboardButton("Поп-музыка",callback_data='but2')
        # button3 = types.InlineKeyboardButton("Электронная музыка",callback_data='but3')
        # button4 = types.InlineKeyboardButton("Зарубежная",callback_data='but4')
        # button5 = types.InlineKeyboardButton("Топ-40 музыки",callback_data='but5')
        # button6 = types.InlineKeyboardButton("⬅️ Вернуться к меню", callback_data='back')
        # markup2.add(button1, button2)
        # markup2.add(button3, button4)
        # markup2.add(button5)
        # markup2.add(button6)
        # bot.edit_message_text(chat_id=ID[0], message_id=call.message.message_id, text="🎧Выберите интересующую Вас тематику:🎧", reply_markup=markup2)


    elif call.data == 'back':
        markup1 =  types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Найти фильм в Tas-ix!", callback_data='check_film')
        button2 = types.InlineKeyboardButton("Tas-ix проверка!", callback_data='check_site')
        button3 = types.InlineKeyboardButton("Будильник", callback_data='clock')
        markup1.add(button1,button2)
        markup1.add(button3)
        bot.edit_message_text(chat_id=256370991, message_id=call.message.message_id, text="Выберите один из разделов:", reply_markup=markup1)


    elif call.data == 'check_site':
        markup3 = types.InlineKeyboardMarkup()
        markup3.add( types.InlineKeyboardButton(text = "⬅️ Вернуться к меню", callback_data = 'back'))
        bot.edit_message_text(chat_id=256370991, message_id=call.message.message_id, text="Отправьте адрес сайта вида : 'пример.соm'", reply_markup=markup3)
        call_title.insert(0,call.message.message_id)

bot.polling(none_stop=True)
