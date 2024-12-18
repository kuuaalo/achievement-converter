import os
import vdf
import csv
import xml.etree.ElementTree as ET
import pprint
# from tero import tero

# test_file_location = "C:\\Users\\niini\\Documents\\achievement-converter\\files\\msxml_test.xml"

# tero = 1

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

        self.vdf_params_outer = ["undefined", "stats", "1"]
        self.vdf_params_inner = ['bits']

        if tero:
            self.tero = tero
            print("self_tero")
            print(self.tero)
        else:
            print("Error: no tero")
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

        # tämän voi siirtää parametriksi
        # j = d[self.steamid]['stats']['1']
        j = self.vdf_dict_peeling(d, pl)

        # halutaan joku mainin määrittämä tapa miten saada käyttäjälle näkyville
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

        self.tero.add_achievements(ol)

        return True

    def run_csv(self):
    # handles csv files

        acmt = self.file_name
        ol = []

        with open(acmt, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                for row in csv_reader:
                    acmt_dict = {
                        "name_id": row.get("name"),
                        "hidden": row.get("hidden"),
                        "acmt_xp": row.get("user_epic_achievements_xp"),
                        "acmt_stat_tres": row.get("statTresholds"),
                    }
                    ol.append(acmt_dict)
        pprint.pp(ol)
        self.tero.add_achievements(ol)


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

        self.tero.add_achievements(ol)

        return True


        #aet = ET.parse("C:\\Users\\niini\\Documents\\achievement-converter\\files\\msxml_test.xml")


        #print("printing aet")
        #pprint.pp(aet)


        # tag = aet.find("ns:Achievement", namespace)
        # print("printing tag")
        # pprint.pp(tag)

        # for a in aet.findall("ns:Achievement", namespace):
        #     print("printing a")
        #     pprint.pp(a)

        #     for c in a.iter():
        #         print("printing c")
        #         pprint.pp(c)
        #         print("printing c tag")
        #         pprint.pp(c.tag)
        #         print("printing c text")
        #         pprint.pp(c.text)


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
# R.run_xml()

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

