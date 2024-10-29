import config
from tkinter import filedialog as fd
import tkinter as tk

from gui import AchievementConverterGUI #import gui

from tero.tero import Tero #import all functions from tero, these don't exist yet
from write.write import Write #import all functions from write, these don't exist yet
from read.read import Read #import all functions from read


def file_handler(selected_path):
    
    if selected_path != None: #if user changed path use it and it's not null
        acmt_file_path = selected_path
        acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
        tero = Tero(False, False)
        read = Read(acmt_file_path, acmt_platform, tero) #init read and give params
        write = Write(acmt_file_path, acmt_platform,tero) #init write and give params
        read.run()
        write.run()
    print(acmt_file_path)

def main():
    acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
    acmt_file_path = config.DEFAULT_FILE_PATH #use default path
    root = tk.Tk()
    
    tero = Tero(False, False) #init tero and give parameter
    read = Read(acmt_file_path, acmt_platform, tero) #init read and give params
    write = Write(acmt_file_path, acmt_platform, tero) #init write and give params

    acmt_gui = AchievementConverterGUI(root, file_handler) #call gui

    root.mainloop()


if __name__ == "__main__":
    main()



