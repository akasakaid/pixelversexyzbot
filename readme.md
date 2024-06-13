# pixelversexyzbot

Auto claim for pixeltap by pixelverse

<center>
<img src="./image/image.png" width="400px" height="300px">
</center>

# Table of Contents
- [pixelversexyzbot](#pixelversexyzbot)
- [Table of Contents](#table-of-contents)
- [Feature](#feature)
- [Registration](#registration)
- [How to Use](#how-to-use)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Termux](#termux)
- [How to Get Data](#how-to-get-data)
- [Video Guide \& Android Guide](#video-guide--android-guide)
- [Javascript Command to Get Telegram Data for Desktop](#javascript-command-to-get-telegram-data-for-desktop)
- [Support](#support)
- [Discussion](#discussion)
- [Thank you \< 3](#thank-you--3)

# Feature

- [x] Auto Claim Point
- [x] Auto Claim Daily Reward
- [x] Suppport Multi Account
- [x] Input data manually (no login require)

# Registration

Start bot : [HERE](https://t.me/pixelversexyzbot?start=629438076)

# How to Use

## Windows 

1. Make sure you computer was installed python and git.
   
   python site : [https://python.org](https://python.org)
   
   git site : [https://git-scm.com/](https://git-scm.com/)

2. Clone this repository
   ```shell
   git clone https://github.com/akasakaid/pixelversexyzbot.git
   ```

3. goto pixelversexyzbot directory
   ```
   cd pixelversexyzbot
   ```

4. install the require library
   ```
   python -m pip install -r requirements.txt
   ```

5. fill the `data.txt` file with your data, how to get data you can refer to [How to Get Data](#how-to-get-data)
6. execute the main program 
   ```
   python bot.py
   ```

## Linux

1. Make sure you computer was installed python and git.
   
   python
   ```shell
   sudo apt install python3 python3-pip
   ```
   git
   ```shell
   sudo apt install git
   ```

2. Clone this repository
   
   ```shell
   git clone https://github.com/akasakaid/pixelversexyzbot.git
   ```

3. goto pixelversexyzbot directory

   ```shell
   cd pixelversexyzbot
   ```

4. Install the require library
   
   ```
   python3 -m pip install -r requirements.txt
   ```

5. fill the `data.txt` file with your data, how to get data you can refer to [How to Get Data](#how-to-get-data)
6. execute the main program 
   ```
   python bot.py
   ```

## Termux

1. Make sure you termux was installed python and git.
   
   python
   ```
   pkg install python
   ```

   git
   ```
   pkg install git
   ```

2. Clone this repository
   ```shell
   git clone https://github.com/akasakaid/pixelversexyzbot.git
   ```

3. goto pixelversexyzbot directory
   ```
   cd pixelversexyzbot
   ```

4. install the require library
   ```
   python -m pip install -r requirements.txt
   ```

5. fill the `data.txt` file with your data, how to get data you can refer to [How to Get Data](#how-to-get-data)
6. execute the main program 
   ```
   python bot.py
   ```

# How to Get Data
   
   1. Active web inspecting in telegram app, How to activate follow the video [https://youtu.be/NYxHmck_GjE](https://youtu.be/NYxHmck_GjE)
   2. Goto gamee bot and open the apps
   3. Press `F12` on your keyboard to open devtool or right click on app and select `Inspect`
   4. Goto `console` menu and copy [javascript code](#javascript-command-to-get-telegram-data-for-desktop) then paste on `console` menu
   5. If you don't receive error message, it means you successfully copy telegram data then paste on `data.txt` (1 line for 1 telegram data)
   
   Example telegram data

   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   ```

   6. If you want to add more account. Just paste telegram second account data in line number 2.
   
   Maybe like this sample in below

   ```
   1.query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   2.query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   ```

# Video Guide & Android Guide

Watch the video via following link for guidance : [https://youtu.be/KTZW9A75guI](https://youtu.be/KTZW9A75guI)

# Javascript Command to Get Telegram Data for Desktop

```javascript
copy(Telegram.WebApp.initData)
```

# Support

To support me you can buy me a coffee via website in below

- Send IDR directly via QRIS : [https://s.id/nusanqr](https://s.id/nusanqr)
- https://trakteer.id/fawwazthoerif/tip
- https://sociabuzz.com/fawwazthoerif/tribe

# Discussion

If you have any question or something you can ask in here : [@sdsproject_chat](https://t.me/sdsproject_chat)

# Thank you < 3