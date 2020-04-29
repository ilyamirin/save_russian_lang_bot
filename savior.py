# -*- coding: utf-8 -*-
import telebot
import requests
import logging
import nltk
import random
import re
import argparse
from os.path import exists, dirname, basename
from os import makedirs, listdir
import csv

# парсер аргументов
parser = argparse.ArgumentParser(description='telebot for gathering records of spoken text messages')
parser.add_argument("token", type=str)
parser.add_argument('-t',
                    '--texts',
                    action="store",
                    dest="texts",
                    type=str,
                    nargs="*",
                    help="files for sentences generation",
                    default=listdir("data/text_files"))
args = parser.parse_args()
texts = [i for i in args.texts if i.endswith(".txt")]
token = args.token

# инциализация логгера
logging.basicConfig(filename="data/savior.log", level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
telebot.console_output_handler = logging.StreamHandler()


# получаем список прокси
def get_proxy():
    global proxies_provider
    global proxies
    if 'proxies_provider' not in globals():
        proxies_provider = 'https://www.proxy-list.download/api/v1/get?type=socks5'
        try:
            proxies = [i for i in requests.get(proxies_provider).text.split()]
            print('Proxies list recieved.')
        except ConnectionError:
            print('Unable to get proxies list, check your internet connection')
        except AssertionError:
            pass
    for each in proxies:
        yield(each)


def run_bot():
    try:
        bot.polling(timeout=1000, none_stop=True, interval = 1)
    except Exception as e:
        print('failed', e)
        connection_resolve()


def connection_resolve():
    print('Connection troubles, trying to apply proxies...')
    telebot.apihelper.proxy = {'https': 'socks5h://{}'.format(next(get_proxy_instance))}
    print(telebot.apihelper.proxy['https'])
    run_bot()


# возвращает список предложений из данного ей списка текстовых файлов
def get_sentences():

    # устанавливаем прокси на даунлоадер nltk...
    # nltk.set_proxy('https://proxy.dvfu.ru:3128')
    # и скачиваем пунктуацию
    nltk.download('punkt')

    # идем по текстовым файлам...
    if len(texts) == 0:
        print("there is no data in text_files, value by default is 'give me some text'")
        sentences = ["give me some text"]*2048
    else:
        sentences = []
        for txt in texts:
            # ...открываем каждый файл...
            f = open("data/text_files/"+txt, "r")
            if f.mode == 'r':
                contents = f.read()

            f.close()
            # ...токенизируем содержимое по предложениям...
            a_list = nltk.tokenize.sent_tokenize(contents)

            i = 1024 * 2
            while i > 0:
                line = a_list[random.randint(0, len(a_list)-1)]
                # фильтруем предложения по регулярке.
                # Не должно начинаться с тире и пробела после,
                # не должно начинаться со скобки
                # не должно начинаться с цифры
                # количество символов от 29 до 155
                # не должно заканичваться двумя непробельными символами
                # должно заканчиваться точкой
                if re.match('(?!–\s)(?!\()(?!\d).{29,155}(?!\S{2}\.)', line):
                    sentences.append(line)
                    i -= 1

    return sentences


bot = telebot.TeleBot(token, threaded=False)
get_proxy_instance = get_proxy()
sentences = get_sentences()


# блок хендлеров
@bot.message_handler(commands=['start', 'help'])
def help(message):
    msg_text = 'Данный бот был создан для того, чтобы озвучивать текст, связанный с деятельностью банка,\
                для обучения модели распознавания речи. Чтобы помочь в этом деле, используйте команду /add_phrase '
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=['add_phrase'])
def add_phrase(message):
    bot.send_message(message.chat.id, 'Дорогой %(username)s, ответьте, пожалуйста на сообщение голосовым с фразой:' % {"username": message.chat.username})
    bot.send_message(message.chat.id, sentences[random.randint(0,len(sentences)-1)])


@bot.message_handler(func=lambda message: True, content_types=['voice'])
def get_audio(message):
    # logging.info(message)
    if message.reply_to_message:
        if message.voice.duration < 10:
            try:
                f = bot.get_file(message.voice.file_id)
                print(f.file_path)
                path = f.file_path
                downloaded_file = bot.download_file(f.file_path)
                if not exists("data/"+dirname(path)):
                    makedirs("data/"+dirname(path))
                with open("data/"+path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                # пишем в csv-файлик название аудио и стенограмму
                with open("data/"+dirname(path)+'/voice.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([basename(path), message.reply_to_message.text])
                    csv_file.close()
                logging.info('User %(username)s File %(file)s -> Phrase %(phrase)s' % {'username': message.from_user.username, 'file': f.file_path, 'phrase': message.reply_to_message.text})
            except Exception as e:
                logging.error('Error at %(username)s File %(file)s', {'username': message.from_user.username, 'file': f.file_path}, exc_info=e)
            bot.send_message(message.chat.id, 'Спасибо! Чтобы записать еще один файл, введите команду /add_phrase')
        else:
            bot.send_message(message.chat.id, 'Извините, сообщения длиной больше 10 секунд, не подходят.\
                                                Чтобы записать еще один файл, введите команду /add_phrase')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выделите функцией "Ответить" сообщение с текстом,\
                                            которое озвучивали, чтобы однозначно определить соответствие')
        bot.send_message(message.chat.id, sentences[random.randint(0, len(sentences)-1)])


@bot.message_handler(content_types=['text'])
def any_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Узнать о проекте можно командой /help. Чтобы озвучить предложение, введите команду /add_phrase')


if __name__ == "__main__":
    run_bot()
