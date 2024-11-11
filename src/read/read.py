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
import os
import vdf
import pprint
#from ..\tero import Tero

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
        acmt = self.open_file_debug()

        d = vdf.parse(acmt)
        #dd = vdf.dump(d, pretty=True)
        print("printing d")

        pprint.pp(d)
        v = d.values() #propably too simplistic, will need to test
        #print("printing i.key")
        #pprint.pp(i.key())

        print("printing v")
        print(v)

        k = list(d)[0]
        print("printing k")
        print(k)

        v = d[k]
        print("printing v length")
        print(v.__len__())

        vk = list(v)
        print("printing vk")
        print(vk)

        x = vk[0]
        print(x)

        y = v[x]
        print("printing y")
        print(y)
        print(y.__len__())

        z = y['1']
        print("printing z")
        print(z)
        print("printing z len")
        print(z.__len__())

        zl = list(z)
        print("printing zl")
        print(zl)

        q = z["type"]
        print("printing q")
        print(q)

        a = z["bits"]
        print("printing a")
        print(a)
        print("printing a len")
        print(a.__len__())

        al = list(a)
        print("printing")
        print(al)
        print(al.__len__())

        acmtL = [a['1'], a['2'], a['3']]
        print("printing acmtL")
        pprint.pp(acmtL)

        #print("printing key-value pairs")

        #for kk, vv in i:
            #pprint.pp(f"key: {kk}  value: {vv}")
            #pprint.pp(f"value: {vv}")
            #tero.add_achievement(k, v)

        #acmt_dict = {}
#self.format.parser(acmt, acmt_dict)
        #acmt_x = acmt.split(",")
        #for y in acmt_x:
            #s = y.split(":")
            #acmt_dict[s[0]] = s[1]

        #print(acmt_dict)

        #self.tero.add_achievement(acmt_dict)

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

R = Read(test_file_location, "dummy", "1")
#R.read_file()
R.run()

        #except FileNotFoundError:
            #print(f"File {self.file_name} not found.")
            #return None



#def achievements_to_txt(achievements):
# 4. editing the files
#   pass

# 5. testing the function
#if __name__=="__main__":
    #file_path = "path/to/your/file.xml"
    #result = read_main(file_path)
    #print(result)

