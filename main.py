import telebot
from config import currencys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для того, чтобы получить конвертируемое значение - введите команду в таком формате:\n<название переводимой валюты>  \
        <название валюты, в которую необходимо перевести>  \
<количество переводимой валюты>\n Посмотреть список всех доступных валют: /currency'
    bot.reply_to(message, text)

@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for currency in currencys.keys():
        text = '\n'.join((text, currency, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        currency = message.text.split(' ')

        if len(currency) != 3:
            raise ConvertionException('Большое количество параметров.')

        quote, base, amount = currency
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()


