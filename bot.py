import sys
import os
import json
import hashlib
import hmac
import time
import requests
import random
from urllib.parse import unquote
from phonenumbers import is_valid_number as valid_number,parse as pp
from dotenv import load_dotenv
from colorama import *
init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX

load_dotenv()

peer = 'pixelversexyzbot'

def log(message):
    year,mon,day,hour,minute,second,a,b,c = time.localtime()
    mon = str(mon).zfill(2)
    hour = str(hour).zfill(2)
    minute = str(minute).zfill(2)
    second = str(second).zfill(2)
    print(f'{biru}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}')

def countdown(t):
    while t:
        menit,detik = divmod(t,60)
        jam,menit = divmod(menit,60)
        jam = str(jam).zfill(2)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(f'waiting until {jam}:{menit}:{detik} ',flush=True,end='\r')
        t -= 1
        time.sleep(1)
    print('                          ',flush=True,end='\r')


def bot(user_id):
    try:
        auto_upgrade = (True if os.getenv('auto_upgrade') == 'true' else False)
        sleep = os.getenv('sleep')
        min_energy = os.getenv('min_energy')
        interval = os.getenv('interval')

        rawr = 'adwawdasfajfklasjglrejnoierjboivrevioreboidwa'
        secret = hmac.new(rawr.encode('utf-8'),str(user_id).encode('utf-8'),hashlib.sha256).hexdigest()
        url = 'https://api-clicker.pixelverse.xyz/api/users'
        
        headers = {
                'tg-id': str(user_id),
                'secret': secret,
                'Content-Type':'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
        }
        
        res = requests.get(url,headers=headers)
        click_count = res.json()['clicksCount']
        id = res.json()['id']
        pet_id = res.json()['pet']['id']
        energy = res.json()['pet']['energy']
        pet_level = res.json()['pet']['level']
        log(f'{hijau}click count : {putih}{click_count}')
        log(f'{hijau}energy : {putih}{energy}')
        log(f'{hijau}pet level : {putih}{pet_level}')
        print('~' * 40)
        if int(energy) > int(min_energy):
            while True:
                click = random.randint(1,10)
                data = {
                    'clicksAmount': click
                }
                res = requests.post('https://api-clicker.pixelverse.xyz/api/users',json=data,headers=headers)
                open('hasil.json','w').write(res.text)
                if 'error' in res.text:
                    print(merah + res.text)
                    countdown(int(sleep))
                    continue
                
                if "clicksCount" not in res.json().keys():
                    print(merah + res.text)
                    countdown(60)
                    continue
                
                click_count = res.json()['clicksCount']
                energy = res.json()['pet']['energy']
                pet_level = res.json()['pet']['level']
                pet_id = res.json()['pet']['id']
                level_up_price = res.json()['pet']['levelUpPrice']
                log(f'{hijau}click : {putih}{click}')
                log(f'{hijau}click count : {putih}{click_count}')
                log(f'{hijau}energy : {putih}{energy}')
                log(f'{hijau}pet level : {putih}{pet_level}')
                print('~' * 40)
                if auto_upgrade:
                    if int(click_count) >= int(level_up_price):
                        url_upgrade = f'https://api-clicker.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up'
                        res = requests.post(url_upgrade,headers=headers)
                
                if int(min_energy) > int(energy):
                    log(f'{kuning}min energy detected !')
                    log(f'{kuning}entering sleep mode !')
                    countdown(int(sleep))
                    continue
                
                countdown(int(interval))
                continue

    except Exception as e:
        print(merah + str(e))
        return
    
    
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
    {hijau}Auto click/tap PIXELVERSEXYZBOT

    {putih}by t.me/AkasakaID
    {putih}github: @AkasakaID
    
    """
    print(banner)
    arg = sys.argv
    if len(arg) < 2:
        print(f"""How to use :
              
python {arg[0]} telegram_account_user_id

example:
python {arg[0]} 6969696
              """)
        sys.exit()
    
    user_id = arg[1]
    bot(user_id)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
