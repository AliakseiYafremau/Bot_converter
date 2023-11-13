import requests
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


def is_float(s: str):
    if s.replace('.', '').isnumeric():
        return True
    else:
        return False


if __name__ == '__main__':
    c = Converter()
    c.get_price('белорусский рубль', 'евро', 4.0)
