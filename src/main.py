import config
from tkinter import filedialog as fd

from gui import AchievementConverterGUI #import gui

from tero.tero import Tero #import all functions from tero, these don't exist yet
from write.write import Write #import all functions from write, these don't exist yet
from read.read import * #import all functions from read


        
def main():
    acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
    acmt_file_path = config.DEFAULT_FILE_PATH #use default path

    selected_path = AchievementConverterGUI.run_gui() #call gui to get path

    if selected_path != None: #if user changed path use it and it's not null
        acmt_file_path = selected_path 
    print(acmt_file_path)
    tero = Tero(False, False) #init tero and give parameter
    write = Write(acmt_file_path, acmt_platform, tero) #init write and give params
    #read = Read(acmt_file_path, acmt_platform, tero) #init read and give params

    #tero.run() #call the run functions
    #write.run()
    #read.run()

if __name__ == "__main__":
    main()



