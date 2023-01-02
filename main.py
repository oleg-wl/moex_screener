import requests
import json

session = requests.Session()

response = session.get('https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off').json()

print(response)