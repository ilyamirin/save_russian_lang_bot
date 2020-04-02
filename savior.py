import telebot
import nltk
import random
import wget
import re
import logging
import sys

logging.basicConfig(filename="savior.log", level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')

path = sys.argv[1]
token = '1132212407:AAErGfUDqfnSiZ5Qz_1OVYTqxKfPE6uLmG8' 

sentences = []

nltk.download('punkt')

for txt in ["voyna-i-mir-tom-1.txt", 'petushki.txt']:
    f = open(txt, "r")
    if f.mode == 'r':
        contents = f.read()

    f.close()

    a_list = nltk.tokenize.sent_tokenize(contents)

    i = 1024 * 2
    while i > 0:
        line = a_list[random.randint(10, len(a_list)-1)]
        if re.match('(?!–\s)(?!\()(?!\d).{29,155}(?!\S{2}\.)', line):
            sentences.append(line)
            i -= 1


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    try:
        bot.send_message(message.chat.id, 'В прошлом выжили только те языки, у которых была письменность. Письменность Будущего – это обученный понимать и производить человеческую речь искусственный интеллект. Если ИИ не будет адекватно владеть русским языком, это может поставить его на грань вымирания. Оставим эту фразу двусмысленной. Кухарка должна учиться управлять государством, микроволновка должна учиться языку Пушкина и Жириновского. Мы создаём единственный открытый академический размеченный корпус живой русской речи, которым смогут пользоваться все. И учить любые виды ИИ с его помощью. Чтобы внести свою лепту, используйте команду /add_phrase ')
    except Exception as e:
        logging.error('Error while sending /help', exc_info=e)

@bot.message_handler(commands=['add_phrase'])
def add_phrase(message):
    bot.send_message(message.chat.id, 'Дорогой %(username)s, ответь на сообщение голосовым с фразой:' % {"username": message.chat.username})
    bot.send_message(message.chat.id, sentences[random.randint(0,len(sentences)-1)])


@bot.message_handler(func=lambda message: True, content_types=['voice'])
def get_audio(message):
    #logging.info(message)
    if message.reply_to_message:
        f = bot.get_file(message.voice.file_id)
        if message.voice.duration < 30:    
            try:
                wget.download('https://api.telegram.org/file/bot%(token)s/%(file_path)s' % {"token": token, "file_path": f.file_path}, path) 
                logging.info('User %(username)s File %(file)s -> Phrase %(phrase)s' % {'username': message.from_user.username, 'file': f.file_path, 'phrase': message.reply_to_message.text})
            except Exception as e:
                logging.error('Error at %(username)s File %(file)s', {'username': message.from_user.username, 'file': f.file_path}, exc_info=e)

            bot.send_message(message.chat.id, 'Спасибо! Чтобы спасти живой русский язык, еще разок введи команду /add_phrase')
        else:
            bot.send_message(message.chat.id, 'Ты что то очень долго рассказывал! Давай, чтобы спасти живой русский язык, еще разок введи команду /add_phrase')
    else:
        bot.send_message(message.chat.id, 'Плиз сделай РЕПЛАЙ с голосовухой на текст, а то я путаюсь в сообщениях:))')
        bot.send_message(message.chat.id, sentences[random.randint(0,len(sentences)-1)])

@bot.message_handler(content_types=['text'])
def any_message(message):
    bot.send_message(message.chat.id, 'Привет! Узнать о проекте можно командой /help. Чтобы спасти русский язык, введи команду /add_phrase')


bot.polling()
