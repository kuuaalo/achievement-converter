#readin pitää sisältää osat:
# tiedoston (pathin) valinta ja haku käyttäjältä = choose, get, (mainin homma?)
# tiedoston tunnistaminen = identify (main)
# ottaa vastaan tiedoston
# tiedoston lukeminen = read (kirjasto)
# achievementien erottelu ja jäsentäminen = separate, parse
# tietojen muokkaus = edit
# datan siirtäminen eteenpäin Terolle = funktion määrittely tulee teroon

# readista tulee dictionary
# rivi kerrallaan Terolle (maybe)
# main käyttää readia
# Tero on hyödyllinen idiootti ja main on disabled
# msstore, epicgames, steam

# tähän kerään syntyneitä ajatuksia, ja mahdollisia käytettäviä funktioita ynnä muuta
# read luokalle runko, main perustaa oliot luokista, read luokan määrittely
# set_fileformat
# read.run
# tietojen lisäämistä varten vastaavia kuin set_filename
# read ei tiedä missä Tero on, mainin pitää pystyä kertomaan
# yksi achievement on yksi dict
# achievements on lista dictionaryja
# parserin vuoro, xml, miten saa luettua että siitä voi tehdä jotain > set_achievement
# opettele käyttämään parseria, xml, csv > dict > avain/arvo, tutki pythonin valmiita parsereita
# mitä rauli haluaa: minkälaisen python tietorakenteen olettaa saavansa

import os
import vdf
import pprint
#miten importoidaan tero

test_file_location = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\steamvdf_test.txt"

tero = 1

class Read:

    def __init__(self, file_name, format, tero):

        if file_name:
            self.file_name = file_name #todennäköisesti configista PATHNAME + file_name
            print(self.file_name)
        else:
            print("Using test2.txt")
            return None

        if format:
            self.format = format
        else:
            print("väärin")
            return None

        if tero:
            self.tero = tero
        else:
            print("Error: no tero")
            return None


    def run (self):
        acmt = self.read_file()
        acmt_dict = {}
        #self.format.parser(acmt, acmt_dict)
        acmt_x = acmt.split(",")
        for y in acmt_x:
            s = y.split(":")
            acmt_dict[s[0]] = s[1]

        #print(acmt_dict)

        self.tero.add_achievement(acmt_dict)

        return True

    def run_vdf (self):
        acmt = self.read_file()

        acmt = self.open_file_debug()

        d = vdf.parse(acmt)

        self.steamid = list(d)[0]


        # tämän voi siirtää parametriksi
        j = d[self.steamid]['stats']['1']

        # halutaan joku mainin määrittämä tapa miten saada käyttäjälle näkyville
        if (j['type'] == 'ACHIEVEMENTS'):
            print("type in j is correct")
            pass
        else:
            print("type in j is not correct")
            # self.df("type in j is not correct")
            return False

        m = j['bits']

        ml = list(m)

        ol = []

        for x in ml:
            xv = m[x]
            ol.append(xv)

        print("printing ol")
        pprint.pp(ol)

        # tero.add_achievements(ol)

        return True

# tämä on testifunktio Teroa varten
    def run_fake(self):
        fdict1 = {"version": None, #Steam version in file
                    "game_name": None, #Steam game name in file
                    "acmt_num": None, #display order/ identifier in file for multiple achievements
                    "name_id": "achievement 1",
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
        fdict2 = {"version": None, #Steam version in file
                    "game_name": None, #Steam game name in file
                    "acmt_num": None, #display order/ identifier in file for multiple achievements
                    "name_id": "achievement 2",
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
        flist = [fdict1, fdict2]
        self.tero.add_achievements(flist)
        return True

    def read_file(self, file_name= False ):
        if file_name:
            self.file_name = file_name

        #try:
            #with

        f = open(self.file_name, "r")
        file_content = f.read()
        print(file_content)  # Print the content of the file
        return file_content

    def open_file_debug(self):
        f = open(self.file_name, "r")
        return f

    def register_debug(self, df):
        self.df = df

# R = Read(test_file_location, "dummy", tero)
# R.run_vdf()

        # except FileNotFoundError:
        #     print(f"File {self.file_name} not found.")
        #     return None



#def achievements_to_txt(achievements):
# 4. editing the files
#   pass

# 5. testing the function
#if __name__=="__main__":
    #file_path = "path/to/your/file.xml"
    #result = read_main(file_path)
    #print(result)

