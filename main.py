#!venv/bin/python

import requests

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
        q = f'https://iss.moex.com/iss/{query_type}.json'
        data = self.session.get(q, params=query_params).json()
        return data
    
    def get_bonds(self):
        """
        Метод класса для получения списка торгуемых на Мосбирже облигаций через запрос к API Moex
        """               
        bonds = self.request_to_api('securities', limit=100, start=0, group_by='group', group_by_filter='stock_bonds', is_trading=1)
        
        #Цикл для сборки нескольких страниц, выдаваемых запросом к API с параметром start
        for p in range(1,1000):
            page = self.request_to_api('securities', limit=100, start=p*100, group_by='group', group_by_filter='stock_bonds', is_trading=1)
            
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
    
    def get_trade_history(self, secid):
        
        self.secid = secid
                
        query = 'history/engines/stock/markets/shares/securities/{}'.format(secid)
        
        params={'sort_order':'TRADEDATE',
                'from':'2022-01-01','till':'2037-12-31',
                'start':0, 'limit':100,
                'numtrades':0,
                }
        
        
        dt = self.request_to_api(query_type=query, query_params=params)
        
        for p in range(1,1000):
            params['start'] = p*100
            page = self.request_to_api(query_type=query, query_params=params)
            
            for value in page['history']['data']:
                dt['history']['data'].append(value)
                
                if len(page['history']['data']) < 1:
                    break
            
        
        return dt
    
    #TODO: Доделать вывод и сделать визуализацию свечей в ноутбуке
    #убрать метадату, сделать плоский json, добавить цикл для добавления данных в список

    def get_cb_rates(self):
        #Простой запрос для получения курса ЦБ
        rates = self.session.get('https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json').json()
        usd, eur = rates['cbrf']['data'][0][3], rates['cbrf']['data'][0][6]

        return usd, eur


r = Moex()
r.get_trade_history(secid='GAZP')
