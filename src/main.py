import config
import read.vdfparse as vdf
from tkinter import filedialog as fd
import tkinter as tk

from gui import AchievementConverterGUI #import gui

from tero.tero import Tero #import all functions from tero
from write.write import Write #import all functions from write
from read.read import Read #import all functions from read

class AchievementConverter:
    def __init__(self):
        self.acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
        self.acmt_file_path = config.DEFAULT_FILE_PATH #use default path
        self.root = tk.Tk()

        self.tero = Tero(False, False) #init and give parameters
        self.gui = AchievementConverterGUI(self.root, self.file_handler) #call gui give ref to root and file handler

    def file_handler(self, selected_path, command):
        if(command==1): #import
                if selected_path != None: #if user changed path use it and it's not null
                    self.acmt_file_path = selected_path
                    self.read = Read(self.acmt_file_path, self.acmt_platform, self.tero) #init read and give params
                    self.read.run() #run read
                    acmt_list = vdf.value_dict() #get temporary template dict
                    self.gui.create_table(self.root, acmt_list) #send to gui to display values
        elif(command==2): #export INCOMPLETE
                if selected_path != None:
                    emptypath = selected_path #returns the empty path chosen, does not actually save there INCOMPLETE
                    self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #init write in the future pass path
                    self.write.run() #run write.
                    print(emptypath)
        elif(command==3): #save as txt to project file !INCOMPLETE!
                if selected_path != None: 
                    self.acmt_file_path = selected_path
                    self.acmt_platform = ".txt" #txt format
                    self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #init write in the future pass path
                    self.write.run() #run write
        else:
            print("Error")

    def run(self):
        self.root.mainloop() #infinite loop for displaying gui
        

def main():
    acmt = AchievementConverter() #create an instance of the converter, python calls init automatically
    acmt.run() #run to start


if __name__ == "__main__":
    main()



