import config
import tkinter as tk
import os

from gui import AchievementConverterGUI #import gui

from tero.tero import Tero #import all functions from tero
from write.write import Write #import all functions from write
from read.read import Read #import all functions from read

class AchievementConverter:
    def __init__(self):
        #self.acmt_platform = config.DEFAULT_FILE_FORMAT #use default format
        self.root = tk.Tk()

        self.tero = Tero(False, False) #init and give parameters
        
        self.gui = AchievementConverterGUI(self.root, self) #call gui give ref to root and file handler

    def file_handler(self, selected_path, command):
        if(command==1): #import
                if selected_path != None: #if user changed path use it and it's not null
                    acmt_file_path = selected_path
                    acmt_platform = self.get_file_extension(selected_path) #send path to func and get extension
                    self.read = Read(acmt_file_path, acmt_platform, self.tero) #init read and give params, does it need platform?
                    self.read.run() #run read
                    #acmt_list = self.tero.get_achievements() #get list of all achievements
                    acmt_list = self.tero.fill_missing_values()
                    acmt_dict = self.fetch_acmt_dict()
                    
                    
                    self.new_table = self.gui.create_table(acmt_dict)
                    
                    self.gui.bind_events(self.new_table)
                    self.gui.configure_table(self.new_table)
                    self.gui.populate_table(self.new_table, acmt_list) #send to gui to display values

                    formats = ('Steam', 'Epic', 'MS Store', 'All')
                    options = ('HideLocalisations', 'English', 'Finnish', 'ShowLocalisations')
                    self.gui.create_filter(self.new_table, formats, 'formats')
                    self.gui.create_filter(self.new_table, options, 'options')

        elif(command==2): #export
                if selected_path != None:
                    self.acmt_platform = self.get_file_extension(selected_path) #send path to func and get extension
                    print(self.acmt_platform)
                    self.acmt_file_path = selected_path #set the file path and name
                    self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #pass path and name to write
                    self.write.run() #run write
        elif(command==3): #save as txt to project file !INCOMPLETE!
                if selected_path != None: 
                    self.acmt_file_path = selected_path
                    self.acmt_platform = ".txt" #txt format
                    self.write = Write(self.acmt_file_path, self.acmt_platform, self.tero) #init write in the future pass path
                    self.write.run() #run write
        else:
            print("Error: no command given or command unknown.")
    
    def fetch_acmt_dict(self, index = 0):
        acmt_dict = self.tero.get_achievement_by_data(index) #get a single achievement and it's values
        return acmt_dict
         
    def data_handler(self, command, key, new_value, id = None):
        if(command==1):
            acmt_list = self.tero.add_data_to_all_achievements(key, new_value)
        elif(command==2):
            acmt_list = self.tero.update_achievement_data(id, key, new_value)
        
        self.gui.refresh_table(self.new_table) 
        self.gui.populate_table(self.new_table, acmt_list)

    def get_file_extension(self, selected_path):
        return os.path.splitext(selected_path)[1].lower()  # returns file extension

    def run(self):
        self.root.mainloop() #infinite loop for displaying gui
        

def main():
    acmt = AchievementConverter() #create an instance of the converter, python calls init automatically
    acmt.run() #run to start


if __name__ == "__main__":
    main()



