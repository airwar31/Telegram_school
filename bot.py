import time
import telebot
from telebot import types
from bs4 import BeautifulSoup as BS
from requests import get
bot=telebot.TeleBot("6578892721:AAH2J1HsqO6LKD6xBYaHT9MBHbJY3i-jAAw")


joinedFile = open("id.txt", "r")
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()


r=get("https://pogoda.mail.ru/prognoz/sankt_peterburg/24hours/")
soup = BS(r.content, "html.parser")
temp=soup.find_all(class_="p-forecast__temperature-value")
temp=int(temp[0].text.strip()[:2])
wind=soup.find_all(class_="p-forecast__data")[2]
wind=int(wind.text.strip()[:1])
feel=soup.find_all(class_="p-forecast__data")[0]
feel=int(feel.text.strip()[:2])

tempmess="Температура: "+str(temp)+"℃"
windmess="Скорость ветра: "+str(wind)+"м/с"
feelmess="Ощущается как: "+str(feel)+"℃"

@bot.message_handler(commands=["start"])
def start(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("id.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(str(message.chat.id))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Актировка")
    btn2 = types.KeyboardButton("Рассылка")
    btn3 = types.KeyboardButton("Электронный журнал")
    btn4 = types.KeyboardButton("Отзывы")
    btn5 = types.KeyboardButton("Расписание")
    if str(message.chat.id)!="998618198" :
        markup.add(btn4)
    markup.add(btn5)
    markup.add(btn1)
    markup.add(btn3)
    if str(message.chat.id)=="998618198" or str(message.chat.id)=="1262543088" :
        markup.add(btn2)
    mess=f"Привет,{message.from_user.first_name}"
    bot.send_message(message.chat.id,mess,reply_markup = markup,parse_mode="html")

@bot.message_handler(content_types=['text'])
def reaction(message):
    if message.text=="Рассылка" and (str(message.chat.id)=="998618198" or str(message.chat.id)=="1262543088"):    
        for user in joinedUsers:
            photo=open("95.jpg","rb")
            photo1=open("74.jpg","rb")
            if user=="998618198":
                continue
            bot.send_photo(user,photo)
            bot.send_photo(user,photo1)

    elif message.text=="Актировка":
        if wind==0:
            if temp<=-36:
                mes=("Отмена с 1 по 11")
            elif temp<=-32:
                mes=("Отмена с 1 по 8")
            elif temp<=-29:
                mes=("Отмена с 1 по 4")
            else:
                mes=("В школу всем")

        elif wind<5:
            if temp<=-34:
                mes=("Отмена с 1 по 11")
            elif temp<=-30:
                mes=("Отмена с 1 по 8")
            elif temp<=-27:
                mes=("Отмена с 1 по 4")  
            else:
                mes=("В школу всем")

        elif 5<=wind<10:
            if temp<=-32:
                mes=("Отмена с 1 по 11")
            elif temp<=-28:
                mes=("Отмена с 1 по 8")
            elif temp<=-25:
                mes=("Отмена с 1 по 4")
            else:
                mes=("В школу всем")

        elif wind>=10:
            if temp<=-31:
                mes=("Отмена с 1 по 11")
            elif temp<=-27:
                mes=("Отмена с 1 по 8")
            elif temp<=-24:
                mes=("Отмена с 1 по 4") 
            else:
                mes=("В школу всем")

        bot.send_message(message.chat.id,mes)
        time.sleep(1)
        bot.send_message(message.chat.id,"Погодные условия на момент запроса:")
        time.sleep(1.5)
        bot.send_message(message.chat.id,tempmess) 
        time.sleep(1)
        bot.send_message(message.chat.id,windmess)
        time.sleep(1)
        bot.send_message(message.chat.id,feelmess)


    elif message.text=="Электронный журнал":
        markup = types.InlineKeyboardMarkup()
        button2 = types.InlineKeyboardButton("Электронный журнал", url='https://cop.admhmao.ru/elk')
        markup.add(button2)
        bot.send_message(message.chat.id,"Нажмите на кнопку и перейдите в электронный журнал".format(message.from_user),reply_markup=markup)


    elif message.text=="Расписание":
        photo=open("95.jpg","rb")
        photo1=open("74.jpg","rb")
        bot.send_photo(message.chat.id,photo)
        bot.send_photo(message.chat.id,photo1)


    elif message.text=="Отзывы":
        markup = types.InlineKeyboardMarkup()
        button5 = types.InlineKeyboardButton("Написать отзыв", url='https://t.me/airwar31')
        markup.add(button5)
        bot.send_message(message.chat.id,"Оставить отзыв о нашем проекте".format(message.from_user),reply_markup=markup)   

    else:
        bot.send_message(message.chat.id,"Извините, я вас не понимаю. Воспользуйтесь, пожалуйста, кнопками")     


bot.polling(non_stop=True)      