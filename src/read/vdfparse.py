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

d = vdf.parse(open('../../files/steamlocalization_test.vdf')) #parse works on either string/file
print(d)
