
import tkinter as tk
import os

# internal modules
from gui import AchievementConverterGUI #import gui
from process.process import Process # import all functions from process
from write.write import Write # import all functions from write
from read.read import Read # import all functions from read

class AchievementConverter:
    def __init__(self):
        self.root = tk.Tk() # set tkinter as root
        self.process = Process(False, False) # init and give parameters
        self.gui = AchievementConverterGUI(self.root, self) # init gui with root and self
        self.new_table = None
        self.current_dict = None

    def file_handler(self, selected_path, command): # gui calls this to respond to user input
        if(command==1): # import
                acmt_file_path = selected_path
                acmt_platform = self.get_file_extension(selected_path) # get file extension
                self.read = Read(acmt_file_path, acmt_platform, self.process) # init read and give params
                self.read.run() # run read
                acmt_list = self.process.fill_missing_values() # get list of all achievements and keys



                # table creation starts here
                self.acmt_dict = self.fetch_acmt_dict() # get dict for table headers
                self.current_dict = self.acmt_dict
                    
                if self.new_table is None: 
                    self.new_table = self.gui.create_table(self.acmt_dict) # create a new table if there's none
                    self.gui.bind_events(self.new_table) # bind key press events to table
                    self.gui.configure_table(self.new_table) # et some styling
                    formats = ('Steam', 'Epic', 'MS Store', 'All') # values for filter creation
                    self.gui.create_filter(self.new_table, formats, 'formats') # create filter
                    self.gui.populate_table(self.new_table, acmt_list, self.acmt_dict) #first round didn't render any data, added this to populate first import
                else:
                    self.gui.refresh_table(self.new_table) # if table already exists, clear it
                    self.gui.populate_table(self.new_table, acmt_list, self.acmt_dict) # add values to table  


        elif(command==2): # export
                self.acmt_platform = self.get_file_extension(selected_path) # send path to func and get extension
                print(self.acmt_platform)
                self.acmt_file_path = selected_path # set the file path and name
                self.write = Write(self.acmt_file_path, self.acmt_platform, self.process) # pass path and name to write
                self.write.run() # run write
    
        elif(command==3): # save a json with edited values  
                self.acmt_file_path = selected_path
                self.process.save_data(self.acmt_file_path)
        else:
            print("Error: no command given or command unknown.")
    
    def fetch_acmt_dict(self, index = 0):
        acmt_dict = self.process.get_achievement_by_data(index) # get a single achievement and it's values
        self.current_dict = acmt_dict
        return acmt_dict
    
    def fetch_filtered_dict(self, key_list, index = 0): # get a single achievement's specified keys and values
        acmt_dict = self.process.get_achievement_keys_from_dict(key_list, index)
        self.current_dict = acmt_dict
        return acmt_dict
    
    def get_current_dict(self):
        return self.current_dict
         
    def data_handler(self, command, key, new_value, id = None): # sends new values to be added to dict
        if(command==1):
            acmt_list = self.process.add_data_to_all_achievements(key, new_value)
        elif(command==2):
            acmt_list = self.process.update_achievement_data(id, key, new_value)
        
        acmt_dict = self.fetch_acmt_dict() ## added fetch so populate_table knows what to deal with ##

        self.gui.refresh_table(self.new_table) 
        self.gui.populate_table(self.new_table,acmt_list, acmt_dict)  ##  added missing argument here ##
 
    def get_file_extension(self, selected_path): # returns file extension
        return os.path.splitext(selected_path)[1].lower()  

    def run(self): # infinite loop for displaying gui
        self.root.mainloop() 
        

def main():
    acmt = AchievementConverter() #create an instance of the converter
    acmt.run() #run to start


if __name__ == "__main__":
    main()



