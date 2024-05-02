import sys
import os
import json
import hashlib
import hmac
import time
import requests
import random
from urllib.parse import unquote
from telethon import TelegramClient,sync,events
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.errors import SessionPasswordNeededError
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

def login(phone):
    session_folder = "session"
    api_id = 2040
    api_hash = "b18441a1ff607e10a989891a5462e627"
    
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    
    if not valid_number(pp(phone)):
        log(f'{merah}phone number invalid !')
        sys.exit()
    
    client = TelegramClient(f'{session_folder}/{phone}',api_id=api_id,api_hash=api_hash)
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(phone)
            code = input(f"{putih}input login code : ")
            client.sign_in(phone=phone,code=code)
        except SessionPasswordNeededError:
            pw2fa = input(f"{putih}input password 2fa : ")
            client.sign_in(phone=phone,password=pw2fa)
    
    me = client.get_me()
    first_name = me.first_name
    last_name = me.last_name
    username = me.username
    log(f'{putih}Login as {hijau}{first_name} {last_name}')
    return client

def bot(client:TelegramClient):
    try:
        auto_upgrade = (True if os.getenv('auto_upgrade') == 'true' else False)
        sleep = os.getenv('sleep')
        min_energy = os.getenv('min_energy')
        interval = os.getenv('interval')
        result = client(RequestWebViewRequest(
            peer=peer,
            bot=peer,
            from_bot_menu=False,
            url='https://sexyzbot.pxlvrs.io/',
            platform='Android',
        ))
        param = unquote(result.url).split('#tgWebAppData=')[1]
        data_web = {}
        for x in param.split('&'):
            key,value = x.split('=')
            data_web[key] = value

        user = json.loads(unquote(data_web['user']))
        rawr = 'adwawdasfajfklasjglrejnoierjboivrevioreboidwa'
        secret = hmac.new(rawr.encode('utf-8'),str(user['id']).encode('utf-8'),hashlib.sha256).hexdigest()
        url = 'https://api-clicker.pixelverse.xyz/api/users'
        headers = {
                'tg-id': str(user['id']),
                'secret': secret,
                'Content-Type':'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
        }
        while True:
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
                    if 'error' in res.text:
                        print(merah + res.text)
                        break
                    
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
                        break
                    
                    countdown(int(interval))
                    
            log(f'{kuning}entering sleep mode !')
            countdown(int(sleep))
            
    finally:
        client.disconnect()
    
    
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
              
python {arg[0]} phone_number

example:
python {arg[0]} +628969696969
              """)
        sys.exit()
    
    phone = arg[1]
    client = login(phone)
    bot(client)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
