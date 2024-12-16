# Achievement Converter - Program for game achievement file conversion. 
## Description
Achievement Converter is a python program for converting achievement files and from different store platforms' formats.
Currently supported formats are Steam (.vdf), MS Store (.xml) and Epic (.csv).
## Table of contents
## Installation
### Dependencies
Python version 3.13.0 or newer to run.
vdf 3.4. library (https://pypi.org/project/vdf/)

### Update python
See which version you have installed with 
python --version
For Windows: download latest version of python (https://www.python.org/downloads/windows/)
For MAC: download latest version of python from (https://www.python.org/downloads/macos/)
Linux/Debian-based: run sudo apt install python3 to update run sudo apt-get update and sudo apt-get updgrade

Use pip (https://pip.pypa.io/en/stable/) to install the vdf library:
pip install vdf

## Usage
Run the program from terminal with 
achievement-converter\src\python main.py
or
achievement-converter\src\python3 main.py
depending on your settings.

This will open the graphical user interface. 
From here you can choose to import a new achievement file. 
Importing the file lists all of the achievements in a table. You can find the explanations for all of the key:value pairs from this document.
You can filter the values with the filter options provided. This shows only the values needed for the chosen platform's achievement-file.

Select an achievement from the table by double-clicking it. This displays it's contents in a new table.
Here you can click on a value you wish to edit to open up the edit-menu.
The edit-pop up menu has four buttons. You can either replace the value in this single specific achievement, or all of the achievements you imported. 
You can also edit the next value or open the same value but, in the next achievement.

When you are happy with the changes you've made, you can choose 'export' to convert the achievements to your desired format.
Choose the save folder and format and click export. You can also save the imported file as a .json-file, for later editing. Loading the .json still in progress.

## List of keys and their explanations

version: Steam. version
game_name: Steam. game name
acmt_num: Steam | MS Store display order/identifier in file for multiple achievements
name_token: Steam. Reference to name
name_id: Achievement ID, identifier
name_en: Name/title in english
name_fi: Name/title in finnish
name_locked: Locked achievement title
base_acmt:  MS store. Is the achievement unlockable in base-game
desc_id: MS store. Description indentifier.
desc_en: Description in english
desc_fi: Description in finnish
desc_token: Steam reference to description.
hidden: Hidden achievement true/false
icon: Icon for achievement
icon_locked: Locked achievement icon
desc_locked: Description for a locked achievement
acmt_xp: Amount of xp/gamerscore/etc. gained by achieving
acmt_stat_tres:  Epic statTresholds.
ag_type: Epic aggregationType 
flavor_txt: Epic. Localized flavor text that can be used by the game in an arbitrary manner. 

## Future/Roadmap


## Contribution

## Credits




## License


