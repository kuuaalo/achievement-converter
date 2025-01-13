"""
This module provides functionality to read achievement data from different file formats.
It strips and converts the data from given files to a list of dictionaries.
It then sends a list of dictionarys to the process.py module.
"""

import os
import vdf
import csv
import xml.etree.ElementTree as ET
import pprint

class Read:

    def __init__(self, file_name, format, process):

        if file_name:
            self.file_name = file_name
            print(self.file_name)
            self.file_name = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\epiccsv_test.csv"
            self.localization_filename = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\epiclocalization_test.csv"
        else:
            print("Using test2.txt")
            return None

        if format:
            self.format = format
        else:
            print("väärin")
            return None

        self.vdf_params_outer = ["undefined", "stats", "1"]
        self.vdf_params_inner = ['bits']

        if process:
            self.process = process
            print("self_process")
            print(self.process)
        else:
            print("Error: no process")
            return None


    def run (self):
    # switcher for run
    # decides which format is being used

        if self.format == ".txt":
            self.run_vdf()

        elif self.format == ".xml":
            self.run_xml()

        elif self.format == ".csv":
            self.run_csv()

        else:
            print("format not recognized: ")
            print(self.format)
            return False

        return True

    def vdf_dict_peeling (self, d = {}, l = []):
        if d == {}:
            return False

        if l == []:
            return d

        curd = d

        for x in l:
            #tarvii assertin
            curd = curd[x]

        return curd


    def run_vdf (self):
    # handles vdf files

        acmt = self.open_file_debug()

        d = vdf.parse(acmt)

        self.steamid = list(d)[0]

        pl = self.vdf_params_outer

        pl[0] = self.steamid

        j = self.vdf_dict_peeling(d, pl)

        if (j['type'] == 'ACHIEVEMENTS'):
            print("type in j is correct")
            pass
        else:
            print("type in j is not correct")
            # self.df("type in j is not correct")
            return False

        # m = j['bits']
        m = self.vdf_dict_peeling(j, self.vdf_params_inner)

        ml = list(m)

        ol = []

        #this is hardcoded, might need to refactor it to more generic
        for x in ml:
            z = {}
            y = m[x]
            z["name_id"] = y["name"]
            z["name_en"] = y["display"]["name"]["english"]
            z["name_fi"] = y["display"]["name"]["finnish"]
            z["name_token"] = y["display"]["name"]["token"]
            z["desc_en"] = y["display"]["desc"]["english"]
            z["desc_fi"] = y["display"]["desc"]["finnish"]
            z["desc_token"] = y["display"]["desc"]["token"]
            z["hidden"] = y["display"]["hidden"]
            z["icon"] = y["display"]["icon"]
            z["icon_locked"] = y["display"]["icon_gray"]
            ol.append(z)

        print("printing ol")
        pprint.pp(ol)

        self.process.add_achievements(ol)

        return True

    def run_csv(self):
    # Handles parsing of CSV files and processes achievements data.
        #reading main file
        acmt = self.file_name
        ol = []
        with open(acmt, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                acmt_dict = {
                    "name_id": row.get("name"),
                    "hidden": row.get("hidden"),
                    "acmt_xp": row.get("user_epic_achievements_xp"),
                    "acmt_stat_tres": row.get("statTresholds"),
                }
                ol.append(acmt_dict)
        pprint.pp(ol)
        # self.process.add_achievements(ol)

        #reading localization file
        locals = self.localization_filename
        lol = []
        with open(locals, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                locals_dict = {
                    "name_id": row.get("name"),
                    "locale": row.get("locale"),
                    "lockedTitle": row.get("lockedTitle"),
                    "lockedDesc": row.get("lockedDescription"),
                    "unlocked": row.get("unlockedTitle"),
                    "unlockeddesc": row.get("unlockedDescription"),
                    "flavor": row.get("flavorText"),
                }
                lol.append(locals_dict)
        pprint.pp(lol)
        for a in lol:
            ID = a["name_id"]
            LOCALE = a["locale"]
            xl = []
            for x in a:
                if x == "name_id":
                    continue
                if x == "locale":
                    continue
                xl.append((x, a[x]))
            print("printing xl")
            pprint.pp(xl)


            # self.process.add_localizations(a[ID], a[LOCALE], "list_of_valuepairs")
            pprint.pp("printing localization items")
            pprint.pp(a)

# name,locale,lockedTitle,lockedDescription,unlockedTitle,unlockedDescription,flavorText,lockedIcon,unlockedIcon


    def run_xml(self):
    # handles xml files

        acmt = self.file_name
        print("printing acmt")
        print(acmt)
        ol = []
        with open(acmt, "r", encoding="utf-8") as f:
            aet = ET.parse(f)
        namespace = {'ns': "http://config.mgt.xboxlive.com/schema/achievements2017/1"}
        for a in aet.findall("ns:Achievement", namespace):
            acmt_dict = {
            "name_id": None,
            "desc_id":None,
            "hidden": None,
            "icon": None,
            "desc_locked": None,
            "acmt_xp": None,
            "base_acmt": None,
            "acmt_num":None,
            }

            acmt_dict["name_id"] = a.find("ns:AchievementNameId", namespace).text if a.find("ns:AchievementNameId", namespace) is not None else None
            acmt_dict["desc_id"] = a.find("ns:UnlockedDescriptionId", namespace).text if a.find("ns:UnlockedDescriptionId", namespace) is not None else None
            acmt_dict["hidden"] = a.find("ns:IsHidden", namespace).text if a.find("ns:IsHidden", namespace) is not None else None
            acmt_dict["icon"] = a.find("ns:IconImageId", namespace).text if a.find("ns:IconImageId", namespace) is not None else None
            acmt_dict["desc_locked"] = a.find("ns:LockedDescriptionId", namespace).text if a.find("ns:LockedDescriptionId", namespace) is not None else None
            acmt_dict["acmt_xp"] = a.find("ns:Gamerscore", namespace).text if a.find("ns:Gamerscore", namespace) is not None else None
            acmt_dict["base_acmt"] = a.find("ns:BaseAchievement", namespace).text if a.find("ns:BaseAchievement", namespace) is not None else None
            acmt_dict["acmt_num"] = a.find("ns:DisplayOrder", namespace).text if a.find("ns:DisplayOrder", namespace) is not None else None
            ol.append(acmt_dict)
        # Print or process each achievement dictionary
        print("Parsed achievement:")
        pprint.pp(ol)

        self.process.add_achievements(ol)

        return True


    def read_file(self, file_name= False ):
        if file_name:
            self.file_name = file_name

        f = open(self.file_name, "r")
        file_content = f.read()
        print(file_content)  # Print the content of the file
        return file_content

    def open_file_debug(self):
        f = open(self.file_name, "r")
        return f

    def register_debug(self, df):
        self.df = df

# functions to test read by itself:
test_filename= "C:\\Users\\niini\\Documents\\achievement-converter\\files\\epiccsv_test.csv"
R = Read(test_filename, "dummy", None)
R.run_csv()