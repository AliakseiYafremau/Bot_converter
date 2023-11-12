import requests
from googletrans import Translator
from values import currencies
from os import getenv
from env_handler import handler
from json import loads

handler()


class ConvertException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        url = f"http://apilayer.net/api/live?access_key={getenv('API_ACCESS_KEY')[1:-1]}" \
              f"&currencies={currencies[quote]}&source={currencies[base]}&format=0"

        r = requests.get(url)
        print(url)
        response = loads(r.content)
        print(response)

        if not response['success']:
            raise Exception('Ошибка в API')

        rate = response['quotes'][f'{currencies[base]}{currencies[quote]}']

        return rate * amount

    @staticmethod
    def get_list_of_currencies():
        url = f"http://apilayer.net/api/list?access_key={getenv('API_ACCESS_KEY')[1:-1]}"

        r = requests.get(url)
        response = loads(r.content)
        values = {}
        reversed_dict = response['currencies']
        translator = Translator(service_urls=['translate.google.com'])
        for key in reversed_dict.keys():
            translation = translator.translate(reversed_dict[key], dest='ru', src='en').text
            values.update({translation: key})
        print(values)

def is_float(s: str):
    if s.replace('.', '').isnumeric():
        return True
    else:
        return False


if __name__ == '__main__':
    c = Converter()
    c.get_list_of_currencies()