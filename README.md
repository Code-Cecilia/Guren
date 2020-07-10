<h1 align="center">
  <br>
  <a href=""><img src="https://cdn.discordapp.com/attachments/713430084039737354/731176680139522139/wallpaperflare.com_wallpaper_2.jpg" alt="Guren"></a>
  <br>
  Guren Ichinose Discord Bot
  <br>
</h1>

<h4 align="center">Utilities, Moderation, Memes.</h4>

<p align="center">
  <a href="https://discord.gg/8wCez2n">
    <img src="https://discordapp.com/api/guilds/133049272517001216/widget.png?style=shield" alt="Discord Server">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge" alt="Made with Python 3.8">
  <a href="https://github.com/Rapptz/discord.py/">
      <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>


# Guren
[![Build Status](https://travis-ci.com/Uplodading-Team/Guren.svg?branch=master)](https://travis-ci.com/Uplodading-Team/Guren)


A discord bot written by [YuiiiiPTChan](https://github.com/YuiiiPTChan) in python using the library discord.py [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html#)
Don't use my code without crediting. You are free to host it and fork it yourself but don't claim my code as yours.


The token in the screenshot is invalid so you don't have to worry :P
Dashboard included, developer of the python module is fixing the issue #2. When fixed, dependencies here will be updated

# Usage and installation

### Linux:
Open a temrinal window and type in the following

```bash
chmod +x ./startbot.sh
sudo apt-get install python3
sudo apt-get update
sudo apt-get install python3-pip
```

Verify that you have the terminal window linked to the folder where file.txt is
If you are not, simply cd into it

```bash
cd ./Guren
```

Install python modules.

```bash
python3 -m pip install -r file.txt
```

Edit botstart.py token with your bot token. Assuming you have a bot user associated with your Application at [Discord Developers](https://discord.com/developers/applications)

![Screenshot_4](images/Screenshot_4.png?raw=true "Developer Portal")

The copied value is what you are gonna put in the gap of "".

>
![Screenshot_3](images/Screenshot_3.png?raw=true "Token")

Navigate to these files: `_Levels.py` | `Server Owner.py` | `botstart.py`
Edit those lines to match the path for their respective JSON in your system / vps 

- `botstart.py` - Line 18
- `_Levels.py` - Lines 13 and 19
- `Server Owner.py` - Lines 17 and 23

![Screenshot_2](images/Screenshot_2.png?raw=true "Lines to edit")

Run the bot
```bash
python3 botstart.py
```
or

```bash
./startbot.sh
```


### Windows: 
Download latest python version from the official website and dont forget to check ADD PYTHON X.X.X to PATH.

> [Python](https://www.python.org/downloads/release/python-383/)

![Screenshot_1](images/Screenshot_1.png?raw=true "PATH Checkbox")

After installing, open a cmd window, also linked to the place where the file.txt is and run the following

```bash
python3 -m pip install -r file.txt
```

Edit botstart.py token with your bot token. Assuming you have a bot user associated with your Application at [Discord Developers](https://discord.com/developers/applications)

![Screenshot_4](images/Screenshot_4.png?raw=true "Developer Portal")

The copied value is what you are gonna put in the gap of "".

> 
![Screenshot_3](images/Screenshot_3.png?raw=true "Token")

Navigate to these files: `_Levels.py` | `Server Owner.py` | `botstart.py`.
Edit those lines to match the path for their respective JSON in your system / vps. 

- `botstart.py` - Line 18
- `_Levels.py` - Lines 13 and 19
- `Server Owner.py` - Lines 17 and 23

![Screenshot_2](images/Screenshot_2.png?raw=true "Lines to edit")

Run the bot

Double click on botstart.bat
