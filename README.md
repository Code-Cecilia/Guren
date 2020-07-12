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
 <a href="https://travis-ci.com/Uplodading-Team/Guren"><img src="https://travis-ci.com/Uplodading-Team/Guren.svg?branch=master"></a>
  <a href="https://github.com/Rapptz/discord.py/">
      <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>


# Guren

A discord bot written by [YuiiiiPTChan](https://github.com/YuiiiPTChan) in python using the library discord.py [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html#)
Don't use my code without crediting. You are free to host it and fork it yourself but don't claim my code as yours.


The token in the screenshot is invalid so you don't have to worry :P
Dashboard included, developer of the python module is fixing the issue #2. When fixed, dependencies here will be updated

# Usage and installation

Download the repo as zip or do the following below in a terminal window:

```bash
sudo apt-get install git
git clone https://github.com/Uplodading-Team/Guren
``` 

# MongoDB Configuration Tutorial

- Get an account [here](https://www.mongodb.com/)
- Create a cluster and wait for it to complete setup. (It's free per 1 project)
- Whitelist your system/vps external ip address on the network tab
- After whitelisting and the cluster creation is complete, press on connect
- Create a user with password
- Select 2 method to connect
- Change nodejs to Python, 3.6 or later
- Copy the link it generated but edit `<password>` with the password you set on the previous step

Done

### Linux:
Open a temrinal window and type in the following

```bash
chmod +x ./startbot.sh
sudo apt-get install python3.8
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

Get your bot token to place in `bot_config/secrets.json` [Discord Developers](https://discord.com/developers/applications)

![Screenshot_4](images/Screenshot_4.png?raw=true "Developer Portal")

Navigate to these files: `Levels.py` | `bot_config/secrets.json`
Edit those to match your bot configuration

- `Levels.py` - Lines 13 and 19
- `secrets.json` - "token" and "mongo"

![Screenshot_2](images/Screenshot_5.png?raw=true "Lines to edit")

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

Get your bot token to place in `bot_config/secrets.json` [Discord Developers](https://discord.com/developers/applications)

![Screenshot_4](images/Screenshot_4.png?raw=true "Developer Portal")


Navigate to these files: `Levels.py` | `bot_config/secrets.json`
Edit those to match your bot configuration

- `Levels.py` - Lines 13 and 19
- `secrets.json` - "token" and "mongo"

![Screenshot_2](images/Screenshot_5.png?raw=true "Lines to edit")

Run the bot

Double click on botstart.bat
