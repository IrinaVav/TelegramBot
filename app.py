import telebot
from config import keys, TOKEN
from extensions import APIException, CriptoConverter

bot = TeleBot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите название валюты с маленькой буквы, в следующем формате:' \
           '\nимя валюты\
            \nв какую валюту перевести\
            \nколичество переводимой валюты\
            \n\
            \nЧтобы увидеть список доступных валют введите команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользоватея.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
