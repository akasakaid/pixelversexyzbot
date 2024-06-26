import os
import sys
import json
import time
import hmac
import hashlib
import argparse
import requests
from colorama import *
from datetime import datetime, timezone
from urllib.parse import unquote, quote, parse_qs

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
putih = Fore.LIGHTWHITE_EX


class Data:
    def __init__(self, init_data, userid, username, secret):
        self.init_data = init_data
        self.userid = userid
        self.username = username
        self.secret = secret


class PixelTapTod:
    def __init__(self):
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,en-US;q=0.9",
            "Host": "api-clicker.pixelverse.xyz",
            "X-Requested-With": "org.telegram.messenger",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        }
        self.marin_kitagawa = lambda data: {
            key: value[0] for key, value in parse_qs(data).items()}

    def get_secret(self, userid):
        rawr = "adwawdasfajfklasjglrejnoierjboivrevioreboidwa"
        secret = hmac.new(
            rawr.encode("utf-8"), str(userid).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return secret

    def data_parsing(self, data):
        redata = {}
        for i in unquote(data).split('&'):
            key, value = i.split('=')
            redata[key] = value

        return redata

    def get_me(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/users'
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        if data.username is not None:
            headers['username'] = data.username

        while True:
            res = self.http(url, headers)
            balance = res.json().get('clicksCount', None)
            if balance is None:
                self.log(f'{kuning}failed fetch balance !')
                time.sleep(2)
                continue
            self.log(f'{hijau}total balance : {putih}{balance}')
            self.user_balance = balance
            return

    def daily_reward(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/daily-rewards'
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        if data.username is not None:
            headers['username'] = data.username

        res = self.http(url, headers)
        today_reward = res.json().get('todaysRewardAvailable')
        if today_reward is None:
            self.log(f'{merah}failed fetch today reward !')
            return

        if today_reward:
            url_claim = 'https://api-clicker.pixelverse.xyz/api/daily-rewards/claim'
            res = self.http(url_claim, headers, '')
            amount = res.json().get('amount')
            if amount is None:
                self.log(f'{merah}failed claim today reward !')
                return

            self.log(f'{hijau}success claim today reward : {putih}{amount}')
            return

        self.log(f'{kuning}already claim today reward !')
        return

    def get_mining_proccess(self, data: Data):
        url = "https://api-clicker.pixelverse.xyz/api/mining/progress"
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        if data.username is not None:
            headers['username'] = data.username

        while True:
            res = self.http(url, headers)
            if res.json().get('currentlyAvailable', None) is None:
                continue
            break
        available = res.json()['currentlyAvailable']
        min_claim = res.json()['minAmountForClaim']
        self.log(f'{putih}amount available : {hijau}{available}')
        if available > min_claim:
            url_claim = 'https://api-clicker.pixelverse.xyz/api/mining/claim'
            res = self.http(url_claim, headers, '')
            if 'claimedAmount' not in res.json().keys():
                self.log(f'{merah}claim failed, maybe to many request !')
                return

            claim_amount = res.json()['claimedAmount']
            self.log(f'{hijau}claim amount : {putih}{claim_amount}')
            return

        self.log(f'{kuning}amount too small to make claim !')
        return

    def daily_combo(self, data: Data):
        url = "https://api-clicker.pixelverse.xyz/api/cypher-games/current"
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        if data.username is not None:
            headers['username'] = data.username

        res = self.http(url, headers)
        if res.status_code != 200:
            self.log(f'{kuning}you have complete daily combo !')
            return

        today = datetime.now(timezone.utc).isoformat().split("T")[0]
        list_combo = open("combo.txt").read().strip().split(',')
        list_option = res.json().get('availableOptions')
        if list_option is None:
            self.log(f'{merah}failed fetch combo option !')
            return
        list_option = [i["id"] for i in list_option]
        combo = {list_option[int(v) - 1]: k for k, v in enumerate(list_combo)}
        combo_id = res.json()['id']
        answer_url = f"https://api-clicker.pixelverse.xyz/api/cypher-games/{combo_id}/answer"
        res = requests.post(answer_url, headers=headers, json=combo)
        if res.status_code != 201:
            self.log(f'{merah}failed apply daily combo !')
            return

        self.log(f'{hijau}success apply daily combo !')
        reward = res.json().get('rewardAmount', None)
        self.log(f'{hijau}reward daily combo : {putih}{reward}')

    def pets(self, data: Data):
        url = "https://api-clicker.pixelverse.xyz/api/pets"
        headers = self.base_headers.copy()
        headers['initData'] = data.init_data
        headers['secret'] = data.secret
        headers['tg-id'] = data.userid
        if data.username is not None:
            headers['username'] = data.username
        while True:
            if self.AUTO_BUY_PET:
                self.log(f'{putih}auto buy pet is {hijau}enable !')
                res = self.http(f"{url}/buy", headers, "")
                _pet = res.json().get('id')
                if _pet is None:
                    self.log(f'{merah}failed buy new pet !')
                else:
                    _pet_name = res.json()['pet']['name']
                    self.log(
                        f'{hijau}success buy new pet, pet name : {putih}{_pet_name} !')
            res = self.http(url, headers)
            data_pets = res.json().get('data', [])
            if len(data_pets) <= 0:
                self.log(f'{merah}failed fetch data pets !')
                continue

            for pet in data_pets:
                user_pet_name = pet['name']
                user_pet_id = pet['userPet']['id']
                user_pet_level = pet['userPet']['level']
                user_level_up_price = pet['userPet']['levelUpPrice']
                self.log(f'{hijau}pet id : {putih}{user_pet_id}')
                self.log(f'{hijau}pet name : {putih}{user_pet_name}')
                self.log(f'{hijau}pet level : {putih}{user_pet_level}')
                if self.AUTO_UPGRADE_PET:
                    if user_pet_level > self.MAX_LEVEL_UPGRADE_PET:
                        self.log(
                            f'{kuning}limit max level pet reacted from config !')
                        continue

                    if user_level_up_price > self.user_balance:
                        self.log(
                            f'{kuning}balance not enough to upgrade {putih}{user_pet_name}{kuning} !')
                        continue
                    upgrade_url = f"https://api-clicker.pixelverse.xyz/api/pets/user-pets/{user_pet_id}/level-up"
                    res = self.http(upgrade_url, headers, '')
                    if res.status_code != 201:
                        self.log(f'{merah}failed upgrade pet {user_pet_name}')
                        continue
                    self.log(
                        f'{hijau}success upgrade pet {putih}{user_pet_name}')
                    self.user_balance -= user_level_up_price
                    continue

            break

    def main(self):
        banner = f"""
    {hijau}AUTO CLAIM PIXELTAP BY {biru}PIXELVERSE
    
    {putih}By : {hijau}t.me/AkasakaID
    {hijau}Github : {putih}@AkasakaID
        """
        arg = argparse.ArgumentParser()
        arg.add_argument('--marin', action="store_true")
        arg.add_argument('--data', default="data.txt", help="")
        args = arg.parse_args()
        if args.marin is False:
            os.system("cls" if os.name == "nt" else "clear")

        print(banner)
        print('~' * 50)
        self.load_config()
        while True:
            for no, data in enumerate(self.load_data(args.data)):
                self.log(f'{hijau}account number : {putih}{no + 1}')
                parser = self.marin_kitagawa(data)
                user = json.loads(parser['user'])
                userid = str(user['id'])
                first_name = user['first_name']
                last_name = user['last_name']
                username = None
                if "username" in user.keys():
                    username = user['username']

                self.log(f'{hijau}login as : {putih}{first_name} {last_name}')
                secret = self.get_secret(userid)
                new_data = Data(data, userid, username, secret)
                self.get_me(new_data)
                self.daily_combo(new_data)
                self.daily_reward(new_data)
                self.get_mining_proccess(new_data)
                self.pets(new_data)
                print('~' * 50)
                self.countdown(self.DEFAULT_INTERVAL)
            self.countdown(self.DEFAULT_COUNTDOWN)

    def load_config(self):
        config = json.loads(open("config.json").read())
        self.DEFAULT_COUNTDOWN = config['countdown']
        self.DEFAULT_INTERVAL = config['interval']
        self.AUTO_BUY_PET = config['auto_buy_pet']
        self.AUTO_UPGRADE_PET = config['auto_upgrade_pet']
        self.MAX_LEVEL_UPGRADE_PET = config['max_level_upgrade_pet']
        self.MAX_PET = config['max_pet']

    def load_data(self, file):
        if not os.path.exists(file):
            self.log(f"{merah}{file} not found !")
            sys.exit()
        datas = open(file).read().splitlines()
        if len(datas) <= 0:
            self.log(f"{merah}there no account detected, fill {file} first !")
            sys.exit()
        self.log(f'{hijau}account detected : {putih}{len(datas)}')
        return datas

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ",
                  flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers, timeout=30)
                    open('http.log', 'a',
                         encoding='utf-8').write(f'{res.text}\n')
                    return res

                if data == '':
                    res = requests.post(url, headers=headers, timeout=30)
                    open('http.log', 'a',
                         encoding='utf-8').write(f'{res.text}\n')
                    return res

                res = requests.post(url, headers=headers,
                                    data=data, timeout=30)
                open('http.log', 'a', encoding='utf-8').write(f'{res.text}\n')
                return res

            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout):
                self.log(f'{merah}connection error / connection timeout !')
                continue


if __name__ == "__main__":
    try:
        app = PixelTapTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
