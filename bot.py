import os
import sys
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime
from colorama import *
from urllib.parse import unquote,quote

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
putih = Fore.LIGHTWHITE_EX

class Data:
    def __init__(self,init_data,userid,username,secret):
        self.init_data = init_data
        self.userid = userid
        self.username = username
        self.secret = secret


class PixelTod:
    def __init__(self):
        self.DEFAULT_COUNTDOWN = 5 * 60
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,en-US;q=0.9",
            "Host": "api-clicker.pixelverse.xyz",
            "X-Requested-With": "org.telegram.messenger",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        }

    def get_secret(self, userid):
        rawr = "adwawdasfajfklasjglrejnoierjboivrevioreboidwa"
        secret = hmac.new(
            rawr.encode("utf-8"), str(userid).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return secret
    
    def data_parsing(self,data):
        redata = {}
        for i in unquote(data).split('&'):
            key,value = i.split('=')
            redata[key] = value
        
        return redata
            
    def main(self):
        banner = f"""
    {hijau}AUTO CLAIM PIXELTAP BY {biru}PIXELVERSE
    
    {putih}By : {hijau}t.me/AkasakaID
    {hijau}Github : {putih}@AkasakaID
        """
        arg = sys.argv
        if "noclear" not in arg:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        datas = open("data.txt","r").read().splitlines()
        self.log(f'{hijau}account detected : {len(datas)}')
        if len(datas) <= 0:
            self.log(f'{kuning}please fill / input your data to data.txt')
            sys.exit()
        print('~' * 50)
        while True:
            for no,data in enumerate(datas):
                self.log(f'{hijau}account number : {putih}{no + 1}')
                data_parse = self.data_parsing(data)
                user = json.loads(data_parse['user'])
                userid = str(user['id'])
                first_name = user['first_name']
                last_name = user['last_name']
                username = user['username']
                self.log(f'{hijau}login as : {putih}{first_name} {last_name}')
                secret = self.get_secret(userid)
                new_data = Data(data,userid,username,secret)
                self.get_me(new_data)
                self.get_mining_proccess(new_data)
                print('~' * 50)
            self.countdown(self.DEFAULT_COUNTDOWN)

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")
    
    def get_me(self,data:Data):
        url = 'https://api-clicker.pixelverse.xyz/api/users'
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        headers['username'] = data.username
        res = self.http(url,headers)
        balance = res.json()['clicksCount']
        self.log(f'{hijau}total balance : {putih}{balance}')
        return
        

    def get_mining_proccess(self, data:Data):
        url = "https://api-clicker.pixelverse.xyz/api/mining/progress"
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        headers['username'] = data.username
        res = self.http(url,headers)
        available = res.json()['currentlyAvailable']
        min_claim = res.json()['minAmountForClaim']
        self.log(f'{putih}amount available : {hijau}{available}')
        if available > min_claim:
            url_claim = 'https://api-clicker.pixelverse.xyz/api/mining/claim'
            res = self.http(url_claim,headers,'')
            claim_amount = res.json()['claimedAmount']
            self.log(f'{hijau}claim amount : {putih}{claim_amount}')
            return
        
        self.log(f'{kuning}amount too small to make claim !')
        return

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def http(self,url,headers,data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url,headers=headers)
                    return res
                
                if data == '':
                    res = requests.post(url,headers=headers)
                    return res
                
                res = requests.post(url,headers=headers,data=data)
                return res
            
            except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout,requests.exceptions.ReadTimeout,requests.exceptions.Timeout):
                self.log(f'{merah}connection error / connection timeout !')
                continue

if __name__ == "__main__":
    try:
        app = PixelTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()