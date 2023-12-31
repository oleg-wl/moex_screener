import requests
import pandas as pd


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
        data = self.session.get(f'https://iss.moex.com/iss/{query_type}s.json', params=query_params).json()
        return data
    
    def get_bonds(self):
        """
        Экземпляр класса для получения списка торгуемых на Мосбирже облигаций через запрос к API Moex
        """               
        bonds = self.request_to_api('securitie', limit=100, start=0, group_by='group', group_by_filter='stock_bonds', is_trading=1)
        
        #Цикл для сборки нескольких страниц, выдаваемых запросом к API
        for p in range(1,1000):
            page = self.request_to_api('securitie', limit=100, start=p*100, group_by='group', group_by_filter='stock_bonds', is_trading=1)
            
            for value in page['securities']['data']:
                bonds['securities']['data'].append(value)
        
            print('Загружена страница: ', p)
            
            if len(page['securities']['data']) < 1:
                print('Загрузка завершена.')
                break  
        return bonds 
    
    def get_stocks(self):
        pass
    
    def get_price(self):
        pass            


if __name__ == "__main__":    
    r = Moex()

    page = r.get_bonds()

    df  = pd.DataFrame(page['securities']['data'], columns=page['securities']['columns'])
    print(df.head(), len(df))
   
