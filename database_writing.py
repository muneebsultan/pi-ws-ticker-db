import pandas as pd
import sqlalchemy
import json
import requests
import time

import json

pairs = ["XLMUSDT", "LINKUSDT", "LTCUSDT"]
file_name = "./data.json"

    # data = json.load(file)
while True:
    for pair in pairs:
        with open(file_name, 'a') as file:
            # old_data = json.load(file)
            new_data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")  
            new_data = new_data.json()
            new_data['time'] = int(time.time())
            print(new_data)
            # file.seek(0) 
            json.dump(new_data, file)
            file.write(',\n')
            file.close()
            time.sleep(1)            

