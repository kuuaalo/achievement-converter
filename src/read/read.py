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
from config import LANGUAGES
from gui import showerror as debug


class Read:

#     def __init__(self, file_name, format, process):
# # old version
#         if file_name:
#             self.file_name = file_name
#             print(self.file_name)
#             # self.file_name = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\epiccsv_test.csv"
#             # self.localization_filename = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\epiclocalization_test.csv"
#         else:
#             print("Using test2.txt")
#             return None

#         if format:
#             self.format = format
#         else:
#             print("väärin")
#             return None

# #proper place for these is propably blueprint. at the moment they can be changed here.
#         self.vdf_params_outer = ["undefined", "stats", "1"]
#         self.vdf_params_inner = ['bits']

#         if process:
#             self.process = process
#             print("self_process")
#             print(self.process)
#         else:
#             print("Error: no process")
#             return None


    def __init__(self, file_name, file_name2, format, process, gui):
#version work in progress
        if file_name:
            self.file_name = file_name
            print(self.file_name)

        else:
            print("no achievement file given.")
            return None

        if file_name2:
            self.localization_filename = file_name2
            print(self.localization_filename)

        else:
            print("no localization file given.")
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
        else:
            print("Error: no process")
            return None

        if gui:
            self.debug = gui.show_error
        else:
            print("no gui given")
            return None



    def run (self):
    # switcher for run
    # decides which format is being used

        if self.format == ".txt" or  self.format == ".vdf":
            self.run_vdf()

        elif self.format == ".xml":
            self.run_xml()

        elif self.format == ".csv":
            self.run_csv()
        else:
            self.debug("fatal error", "import format not recognized")
            self.debug("data: ", self.format)
            return False

        return True

    def vdf_dict_peeling (self, d = {}, l = []):
    # function for peeling off unused layers from the vdf input file
        if d == {}:
            return False

        if l == []:
            return d

        curd = d

        # this for does the actual "peeling" off the layers 1 by 1
        for x in l:
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

        # vdf files contain info about the file 'type'. using this to make a "sanity-check"
        if (j['type'] == 'ACHIEVEMENTS'):
            self.debug("reading vdf file: ", "typecheck passed")
            pass
        else:
            self.debug("reading vdf file: ", "typecheck not passed")
            return False

        actual_acmt = self.vdf_dict_peeling(j, self.vdf_params_inner)
        outl = []
        localization_data = []

        for x in list(actual_acmt):
            z = {}
            y = actual_acmt[x]
            z["name_id"] = y["name"]
            z["name_token"] = y["display"]["name"]["token"]
            z["desc_token"] = y["display"]["desc"]["token"]
            z["hidden"] = y["display"]["hidden"]
            z["icon"] = y["display"]["icon"]
            z["icon_locked"] = y["display"]["icon_gray"]
            outl.append(z)

            # Ddd localization text (value) for each language (key)
            for lang_key, lang_value in y["display"]["name"].items():
                if lang_key != "token":  #exclude token part
                    lang_code_map = LANGUAGES
                    lang_code = lang_code_map.get(lang_key, lang_key)

                    localization_details = {
                        "lockedTitle": f"Locked {lang_value}",
                        "lockedDesc": f"Locked Description of {lang_value}",
                        "unlockedTitle": lang_value,
                        "unlockedDesc": y["display"]["desc"].get(lang_key, "")
                    }

                    # Call add_localizations for each language entry
                    self.process.add_localizations(z["name_id"], lang_code, localization_details)

        print(localization_data)  # This prints out the localization data as test
        self.process.add_achievements(outl)

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

        self.process.add_achievements(ol)

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
                    "unlockedDesc": row.get("unlockedDescription"),
                    "flavor": row.get("flavorText"),
                    "lockedIcon": row.get("lockedIcon"),
                    "unlockedIcon": row.get("unlockedIcon")
                }
                lol.append(locals_dict)
                ID = locals_dict.pop("name_id")
                LOCALE = locals_dict.pop("locale")
                self.process.add_localizations(ID, LOCALE, locals_dict)

            #ID = lol.pop("name_id")
            #LOCALE = lol.pop("locale")
            #self.process.add_localizations(ID, LOCALE, lol)

        return True

    def run_xml(self):
    # handles xml files
    # in localizations.xml tag devdisplaylocale is ignored

        acmt = self.file_name
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

        self.process.add_achievements(ol)

        localz = self.localization_filename
        ol = []
        with open(localz, "r", encoding="utf-8") as f:
            lat = ET.parse(f)
            namespace = {'ns': "http://config.mgt.xboxlive.com/schema/localization/1"}
            for a in lat.findall("ns:LocalizedString", namespace):
                localz_dict = {
                "name_id": None,
                "locale_en": None,
                "locale_fi": None
                }
                valuetext = None
                ID = None
                LOCALE = None
                localz_dict["name_id"] = a.get("id")
                ID = a.get("id")
                for b in a.findall("ns:Value", namespace):
                    t = b.text
                    u = b.get("locale")
                    LOCALE = u

                    known_localez = ["fi", "en"] #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    for L in known_localez:
                        if L in u:
                            localz_dict["locale_" + L] = t
                            valuetext = t

                    temp_dict = {ID:valuetext}

                    valuetext_dict = {LOCALE: temp_dict}

                    print("locale ja id")
                    pprint.pp(LOCALE)
                    pprint.pp(ID)
                    print("value")
                    pprint.pp(valuetext_dict)

                    self.process.add_localizations(ID, LOCALE, valuetext_dict)

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
# test_filename = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\msxml_test.xml"
# test_filename2 = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\mslocalization_test.xml"
# R = Read(test_filename, test_filename2, "dummy")
# R.run_xml()