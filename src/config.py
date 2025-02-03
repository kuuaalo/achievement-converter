# config.py
DEFAULT_FILE_PATH = "..\\test.txt"
DEFAULT_FILE_FORMAT = ".json"
ACMT_DICT = {
    "version": None, #Steam version in file
    "game_name": None, #Steam game name in file
    "game_id": None, #Steam game id in html
    "acmt_num": None, #Steam/MS display order/ identifier in file for multiple achievements
    "name_id": None, #Achievement ID, identifier
    "name_locked": None, #locked acmt title. ! for all localizations? !
    "name_token": None, #ref to steam description
    "desc_id":None, #MS store specific
    "desc_token": None, #ref to steam description
    "hidden": None, #hidden achievement true/false
    "icon": None, #icon for achievements
    "icon_locked": None, #gray icon for locked achievements 
    "desc_locked":None, #description for locked achievements ! for all localizations? !
    "acmt_xp":None, #amount of xp gained by achieving
    "acmt_stat_tres":None, #Epic statTresholds achievementDefinitions.csv 
    "ag_type":None, #Epic aggregationType tats.csv
    "flavor_txt": None, # Epic flavorText  achievementLocalizations.csv
    "base_acmt": None, #MS store specific
}
# filter names
FILTER_FORMATS = ('Steam', 'Epic', 'MS Store', 'All')
# filter values
FILTER_CONFIG = {
            'Steam': ('version','game_name','acmt_num',
                      'name_id','name_token',
                        'desc_token','hidden','icon',
                      'icon_locked','acmt_xp'),
            'MS Store': ('name_id','desc_id','hidden',
                        'icon','acmt_xp','desc_locked',
                        'base_acmt','display_order'),
            'Epic': ('name_id', 'hidden','acmt_xp',
                     'acmt_stat_tres','acmt_xp'),
            'All': ('version','game_name','acmt_num',
                    'name_id','name_token','desc_token',
                    'hidden','icon','icon_locked',
                    'acmt_xp','desc_id','desc_locked',
                    'base_acmt','display_order','acmt_stat_tres')
            }
# achievement table headers
COLUMN_HEADERS = {'key': 'None', 'value': 'None'}