# SAGG
Steam Achievements Guide Generator

This script will simply fetch the given game's achievements page then download all the achievement icons and generate a 3-columns table in [steam format](https://steamcommunity.com/comment/Guide/formattinghelp) contains achievement title, description and custom description.

This idea came into my head after I wrote a achievements guide about Serious Sam 4, it just so painful I have to copy/paste so many times to create a table and take so many screenshots to get the achievement icons.

## Requirements

- Python 3.5+
    - multiprocessing
    - Beautiful Soup 4
    - lxml

## Usage

Simply execute

```shell
git clone https://github.com/azhuge233/SAGG.git
cd SAGG
python3 SteamAchievements.py
```

Then input the steam game's App ID, which can be found once you open the game's store page, it's in the URL, or you can search App ID at [SteamDB](https://steamdb.info).

The results will be stored in the directory named after the game's name.

## Screenshots

![1](https://github.com/azhuge233/SAGG/raw/main/1.png)

![2](https://github.com/azhuge233/SAGG/raw/main/2.png)

![3](https://github.com/azhuge233/SAGG/raw/main/3.png)

