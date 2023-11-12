import telebot
from extensions import ConvertException, is_float, Converter
from values import currencies
from env_handler import handler
from os import getenv

handler()


class BotConverter(telebot.TeleBot):
    def run(self):
        self.handler()
        self.polling()

    def handler(self):
        @self.message_handler(commands=['start', 'help'])
        def handle_start_help(message: telebot.types.Message):
            reference = 'Здравствуйте, я бот конвертер валют. \nЧтоб перевести валюту напишите:\n \
<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \n\
Для того, чтоб узнать поддерживаемые валюты введите /values \n\
Для справки введите /start или /help'
            bot.send_message(message.chat.id, reference)

        @self.message_handler(commands=['values'])
        def enable_values(message: telebot.types.Message):
            currencies_reference = 'Поддерживаемые валюты: '
            for currency in currencies.keys():
                currencies_reference += f'\n{currency}'
            bot.send_message(message.chat.id, currencies_reference)

        @self.message_handler(content_types=['text'])
        def convert(message: telebot.types.Message):
            try:
                text = message.text.lower()
                possibles_values = {}
                for currency in currencies:
                    index_currency = text.find(currency)
                    if index_currency != -1:
                        if len(set(text.split())) != len(text.split()):
                            raise ConvertException('Нельзя перевести деньги в ту же валюту')
                        possibles_values.update({index_currency: currency})

                if len(possibles_values) != 2:
                    raise ConvertException('Вы должны ввести два имя валюты.')

                base = possibles_values.pop(min(possibles_values.keys()))
                quote = possibles_values.pop(min(possibles_values.keys()))

                amount = text.removeprefix(base).strip()
                amount = amount.removeprefix(quote).strip()

                if not is_float(amount):
                    raise ConvertException(f'{amount} не является число')

                amount = float(amount)

                converter = Converter()
                result = converter.get_price(base, quote, amount)

            except ConvertException as e:
                bot.reply_to(message, f'Неправильный ввод. {e}')
            except Exception as e:
                bot.reply_to(message, f'Ошибка на серверной части. {e}')
            else:
                bot.send_message(message.chat.id, f'{amount} {currencies[base]}({base})'
                                                  f' равняется {result} {currencies[quote]}({quote})')


bot = BotConverter(getenv('TOKEN'))

bot.run()
