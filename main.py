#!venv/bin/python

import requests


params = {'group_by':'group',
          'group_by_filter':'stock_bonds',
          'iss.meta':'off',
          'is_trading':1}

"""
Класс для работоы с API Московской биржи. 
"""
class Moex():
    def __init__(self):
        #Создание объекта сессии 
        self.session = requests.Session()
        
    def request_to_api(self, query_type:str, **query_params):
        """
        Метод для отправки запроса к API Мосбиржи.

        :param str query_type: _description_
        :return _type_: _description_
        """
        data = self.session.get(f'https://iss.moex.com/iss/{query_type}.json', params=query_params).json()
        return data
    
    def get_bonds(self):
        """
        Метод класса для получения списка торгуемых на Мосбирже облигаций через запрос к API Moex
        """               
        bonds = self.request_to_api('securities', limit=100, start=0, group_by='group', group_by_filter='stock_bonds', is_trading=1)
        
        #Цикл для сборки нескольких страниц, выдаваемых запросом к API с параметром start
        for p in range(1,1000):
            page = self.request_to_api('securitie', limit=100, start=p*100, group_by='group', group_by_filter='stock_bonds', is_trading=1)
            
            for value in page['securities']['data']:
                bonds['securities']['data'].append(value)
            
            if len(page['securities']['data']) < 1:
                print('Загрузка завершена. Стр:{}'.format(p))
                break  
        return bonds 
    
    def get_stocks(self):
        pass
    
    def get_price(self):
        pass

    def get_cb_rates(self):
        #Простой запрос для получения курса ЦБ
        rates = self.session.get('https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json').json()
        usd, eur = rates['cbrf']['data'][0][3], rates['cbrf']['data'][0][6]

        return usd, eur


