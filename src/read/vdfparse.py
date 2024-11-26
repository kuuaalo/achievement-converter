import vdf

# parsing vdf from file or string
#d = vdf.load(open('steamvdf_test.txt')) #used when the vdf file needs to be read
#d = vdf.loads(vdf_text) #used when the file's contents are already saved into program's memory as a string
#d = vdf.parse(open('steamvdf_test.txt')) #parse works on either string/file
#d = vdf.parse(vdf_text) #parse works on either


# dumping dict as vdf to string
#vdf_text = vdf.dumps(d) #take dictionary and make it into a vdf formatted string

#indented_vdf = vdf.dumps(d, pretty=True) #same as above but prettier indentation

# dumping dict as vdf to file
#vdf.dump(d, open('file3.txt','w'), pretty=True) #write vdf to new file

def value_dict():
#väliformaatti dictionary raakile

    acmt_dict = { 
    "version": None, #Steam version in file
    "game_name": None, #Steam game name in file
    "acmt_num": None, #display order/ identifier in file for multiple achievements
    "name_id": None, #Achievement ID, identifier
    "name_en": None, #Name/title in english
    "name_fi": None, #title in finnish. !! More localizations? Add loop that creates new dictionary key name_var !!
    "name_locked": None, #locked acmt title. ! for all localizations? !
    "name_token": None, #ref to steam description
    "desc_en": None, #description in english ! for all localizations? !
    "desc_fi": None, #description in english ! for all localizations? !
    "desc_token": None, #ref to steam description
    "hidden": None, #hidden achievement true/false
    "icon": None, #icon for achievements
    "icon_locked": None, #gray icon for locked achievements
    "desc_locked":None, #description for locked achievements ! for all localizations? !
    "acmt_xp":None, #amount of xp gained by achieving
    "acmt_stat_tres":None, #statTresholds epic achievementDefinitions.csv
    "ag_type":None, #aggregationType epic stats.csv
    "flavor_txt": None, # flavorText epic achievementLocalizations.csv
    }
    data = {
    "id": "123456",
    "version": "2",
    "gamename": "Super Ultimate Awesome Game",
    "stats_type": "ACHIEVEMENTS",
    "achievement_1_id": "AchievementID1",
    "achievement_1_name_english": "Achievement 1",
    "achievement_1_name_finnish": "Saavutus 1",
    "achievement_1_name_token": "NEW_ACHIEVEMENT_1_1_NAME",
    "achievement_1_desc_english": "Description of Achievement 1",
    "achievement_1_desc_finnish": "Saavutus 1:en kuvaus",
    "achievement_1_desc_token": "NEW_ACHIEVEMENT_1_1_DESC",
    "achievement_1_hidden": "0",
    "achievement_1_icon": "Achievement_1.jpg",
    "achievement_1_icon_gray": "Achievement_Locked_1.jpg",
    
    "achievement_2_id": "AchievementID2",
    "achievement_2_name_english": "Achievement 2",
    "achievement_2_name_finnish": "Saavutus 2",
    "achievement_2_name_token": "NEW_ACHIEVEMENT_1_2_NAME",
    "achievement_2_desc_english": "Description of Achievement 2",
    "achievement_2_desc_finnish": "Saavutus 2:en kuvaus",
    "achievement_2_desc_token": "NEW_ACHIEVEMENT_1_2_DESC",
    "achievement_2_hidden": "1",
    "achievement_2_icon": "Achievement_2.jpg",
    "achievement_2_icon_gray": "Achievement_Locked_2.jpg",
    
    "achievement_3_id": "AchievementID3",
    "achievement_3_name_english": "Achievement 3",
    "achievement_3_name_finnish": "Saavutus 3",
    "achievement_3_name_token": "NEW_ACHIEVEMENT_1_3_NAME",
    "achievement_3_desc_english": "Description of Achievement 3",
    "achievement_3_desc_finnish": "Saavutus 3:en kuvaus",
    "achievement_3_desc_token": "NEW_ACHIEVEMENT_1_3_DESC",
    "achievement_3_hidden": "1",
    "achievement_3_icon": "Achievement_3.jpg",
    "achievement_3_icon_gray": "Achievement_Locked_3.jpg",
}


    #d = vdf.parse(open('../../files/steamlocalization_test.vdf')) #parse works on either string/file
    #print(d)
    return data
