# Guren

A discord bot written in python using the library discord.py [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html#)


the token in the screenshot is invalid so you don't have to worry :P
dashboard included, developer of the python module is fixing the issue #2. When fixed, dependencies here will be updated

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

![Screenshot_4](images/Screenshot_4.png?raw=true "Title")

The copied value is what you are gonna put in the gap of "".

>
![Screenshot_3](images/Screenshot_3.png?raw=true "Title")

Navigate to these files: `_Levels.py` | `Server Owner.py` | `botstart.py`

```bash
Edit those lines to match the path for their respective JSON in your system / vps 
```

- `botstart.py` - Line 18
- `_Levels.py` - Lines 13 and 19
- `Server Owner.py` - Lines 17 and 23

![Screenshot_2](images/Screenshot_2.png?raw=true "Title")

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

![Screenshot_1](images/Screenshot_1.png?raw=true "Title")

After installing, open a cmd window, also linked to the place where the file.txt is and run the following

> python3 -m pip install -r file.txt

Edit botstart.py token with your bot token. Assuming you have a bot user associated with your Application at [Discord Developers](https://discord.com/developers/applications)

![Screenshot_4](images/Screenshot_4.png?raw=true "Title")

The copied value is what you are gonna put in the gap of "".

> TOKEN = "PLACE YOUR BOT TOKEN HERE"
![Screenshot_3](images/Screenshot_3.png?raw=true "Title")

Navigate to these files: `_Levels.py` | `Server Owner.py` | `botstart.py`

> Edit those lines to match the path for their respective JSON in your system / vps 

- `botstart.py` - Line 18
- `_Levels.py` - Lines 13 and 19
- `Server Owner.py` - Lines 17 and 23

![Screenshot_2](images/Screenshot_2.png?raw=true "Title")

Run the bot

> Double click on botstart.bat
