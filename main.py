import telebot
import nltk
import random
import wget

import logging
logging.basicConfig(filename="savior.log", level=logging.INFO)

path = '/Users/ilyamirin/Projects/lang_savior/voices/'
token = '1132212407:AAErGfUDqfnSiZ5Qz_1OVYTqxKfPE6uLmG8' 

sentences = []

nltk.download('punkt')


for txt in ["./voyna-i-mir-tom-1.txt", 'petushki.txt']:
    f = open(txt, "r")
    if f.mode == 'r':
        contents = f.read()

    f.close()

    a_list = nltk.tokenize.sent_tokenize(contents)

    i = 1024 * 2
    while i > 0:
        line = a_list[random.randint(10, len(a_list)-1)]
        if len(line) <= 255 & len(line) > 29:
            #print(line)
            sentences.append(line)
            i -= 1


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['add_phrase'])
def add_phrase(message):
    bot.send_message(message.chat.id, 'Дорогой %(username)s, ответь на сообщение голосовым с фразой:' % {"username": message.chat.username})
    bot.send_message(message.chat.id, sentences[random.randint(0,len(sentences)-1)])
    print(message)


@bot.message_handler(func=lambda message: True, content_types=['voice'])
def get_audio(message):
    print(message)
    if message.reply_to_message:
        f = bot.get_file(message.voice.file_id)
        print(f)
        if message.voice.duration < 30:    
            wget.download('https://api.telegram.org/file/bot%(token)s/%(file_path)s' % {"token": token, "file_path": f.file_path}, path) 
            logging.info('File %(file)s -> Phrase %(phrase)s' % {'file': f.file_path, 'phrase': message.reply_to_message.text})
            bot.send_message(message.chat.id, 'Спасибо! Чтобы спасти живой русский язык, еще разок введи команду /add_phrase')
        else:
            bot.send_message(message.chat.id, 'Ты что то очень долго рассказывал! Давай, чтобы спасти живой русский язык, еще разок введи команду /add_phrase')
    else:
        bot.send_message(message.chat.id, 'Плиз сделай РЕПЛАЙ с голосовухой на текст, а то я путаюсь в сообщениях:))')
        bot.send_message(message.chat.id, sentences[random.randint(0,len(sentences)-1)])

@bot.message_handler(content_types=['text'])
def any_message(message):
    bot.send_message(message.chat.id, 'Привет! Чтобы спасти русский язык, введи команду /add_phrase')


bot.polling()
