import config
from tkinter import filedialog as fd
import tkinter as tk

from gui import AchievementConverterGUI #import gui

from tero.tero import Tero #import all functions from tero, these don't exist yet
from write.write import Write #import all functions from write, these don't exist yet
from read.read import Read #import all functions from read

class AchievementConverter:
    def __init__(self):
        self.acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
        self.acmt_file_path = config.DEFAULT_FILE_PATH #use default path
        self.root = tk.Tk()

        self.tero = Tero(False, False) #init tero and give parameter
        self.read = Read(self.acmt_file_path, self.acmt_platform, self.tero) #should i give null params first?
        self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #init write and give params

        self.gui = AchievementConverterGUI(self.root, self.file_handler) #call gui
         
    def file_handler(self, selected_path, command):
        if(command==1):
                if selected_path != None: #if user changed path use it and it's not null
                    self.acmt_file_path = selected_path
                    self.read = Read(self.acmt_file_path, self.acmt_platform, self.tero) #init read and give params
                    self.read.run()
                    print("import")
                    print(self.acmt_file_path)
        elif(command==2):
                if selected_path != None: #if user changed path use it and it's not null
                    emptypath = selected_path #returns the empty path chosen, does not actually save there INCOMPLETE
                    self.write.run()
                    print("export")
                    print(emptypath)
        elif(command==3): #save as txt to project file (incomplete)
                if selected_path != None: 
                    self.acmt_file_path = selected_path
                    self.acmt_platform = ".txt" #use default format
                    self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #init write and give params
                    self.write.run()
                    print("save")
                    print(self.acmt_file_path)
            
        else:
            print("Error")

    def run(self):
         self.root.mainloop()
        

def main():
    acmt = AchievementConverter()
    acmt.run()


if __name__ == "__main__":
    main()



