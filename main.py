import requests
import json


params = {'group_by':'group',
          'group_by_filter':'stock_bonds',
          'iss.meta':'off'}

"""
Класс для работоы с API Московской биржи. 
"""
class Moex():
    def __init__(self):
        #Создание объекта сессии 
        self.session = requests.Session()
        
    def request_to_api(self, **query_params):
        data = self.session.get('https://iss.moex.com/iss/securities.json', params=query_params).json()
        return data
    
r = Moex()
r1= r.request_to_api(**params)

print(r1)