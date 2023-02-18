import asyncio
import json
import datetime

import requests


URL_BTC = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
URL_ETH = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
HEADERS = {'X-CoinAPI-Key' : 'A3097FDE-CF29-4D6F-88D3-AD9D9EAF8D86'}


async def get_rate():         # Collection of price data every 60 seconds
    while True:
        response_btc = requests.get(URL_BTC, headers=HEADERS)
        response_eth = requests.get(URL_ETH, headers=HEADERS)
        rate_btc = response_btc.json()['rate']
        rate_eth = response_eth.json()['rate']

        rate_dict = {'rate_btc' : [], 'rate_eth' : []}
        try:
            with open('rate.txt', 'r') as f:
                rate_dict = json.load(f)
        except FileNotFoundError:
            pass

        with open('rate.txt', 'w') as f:
            rate_dict['rate_btc'].append(rate_btc)
            rate_dict['rate_eth'].append(rate_eth)
            json.dump(rate_dict, f)
        
        await asyncio.sleep(60)


async def analysis():           # Data analysis every hour
    while True:
        with open('rate.txt', 'r') as f:
            rate_dict = json.load(f)

        rate_btc_list = rate_dict['rate_btc']
        rate_eth_list = rate_dict['rate_eth']

        b_last = 0
        e_last = 0
        own_movement = 0
        for b, e in zip(rate_btc_list, rate_eth_list) :

            if b_last == 0 and e_last == 0:
                b_last = b
                e_last = e
                continue
            else:
                diff_btc = (b - b_last) / b
                diff_eth = (e - e_last) / e
                if abs(diff_eth) <= 0.001:
                    continue                        # Small change - pass
                elif diff_btc > 0 and diff_eth < 0 \
                    or diff_btc < 0 and diff_eth > 0:      
                    own_movement += 1               # 1 - Own movement ETH
                elif diff_btc / diff_eth > 3:
                    own_movement += 1
                    
        e_first = rate_eth_list[0]
        per_change_eth = (e_last - e_first) / e_first * 100
        if own_movement >= 42 and per_change_eth > 1:
            print(f'Own ETH movement was: {per_change_eth}%')
            print(f'At {datetime.datetime.now()} ETHUSDT = {e_last}')
        await asyncio.sleep(3600)
 

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(get_rate()), ioloop.create_task(analysis())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()

