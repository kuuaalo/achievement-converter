import tkinter as tk
from tkinter import filedialog as fd
import os
import config

# internal modules
from gui import AchievementConverterGUI
from process.process import Process
from write.write import Write
from read.read import Read

class AchievementConverter:
    def __init__(self):
        # set tkinter as root
        self.root = tk.Tk()
        # init model and give parameters
        self.process = Process(False, False)
        # init gui with root and self
        self.gui = AchievementConverterGUI(self.root, self)
        # main achievement display table
        self.main_table = None
        # dictionary in use for headers
        self.current_dict = None
        # selected achievement's id
        self.selected_acmt_id = None

        self.current_key_index = None

        self.current_key = None

        self.acmt_table = None

    # import achievement file
    def import_file(self):
        # open filedialog and save paths
        file_path = fd.askopenfilename(title="Import achievement file")
        locale_file_path = fd.askopenfilename(title="Import localization file")
        # get file extension
        acmt_platform = self.get_file_extension(file_path)
        # init read and give params
        self.read = Read(file_path, locale_file_path, acmt_platform, self.process)
        self.read.run()
        #create table to display data
        self.create_table()
    
    # load project file
    def load_file(self):
        file_path = fd.askopenfilename(title="Load project file", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("JSON", "*.json")])
        self.process.load_data(file_path)
        self.create_table()
    
    # export achievement file
    def export_file(self):
        file_path = fd.asksaveasfilename(title="Export project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("VDF files", "*.vdf"), ("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
        # send path to get extension
        acmt_platform = self.get_file_extension(file_path)
        # pass path, name and model to write
        self.write = Write(file_path, acmt_platform, self.process)
        self.write.run()

    # save project file as json
    def save_file(self):
        file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("JSON", "*.json")])
        self.process.save_data(file_path)

    def create_table(self):
        # get list of all achievements and keys
        acmt_list = self.process.fill_missing_values()
        
        # get dict for table headers
        self.table_keys = self.fetch_acmt_dict()
        # save current headers in use for filtering purposes
        self.current_dict = self.table_keys

        if self.main_table is None:
            self.main_table = self.gui.create_table(self.table_keys)
            # bind key press events to table
            self.gui.bind_events(self.main_table)
            self.gui.configure_table(self.main_table)
            # values for filter creation
            formats = ('Steam', 'Epic', 'MS Store', 'All')
            self.gui.create_filter(self.main_table, formats, 'formats')
            self.gui.populate_table(self.main_table, acmt_list, self.table_keys)
        else:
            # if table already exists, clear it
            self.gui.refresh_table(self.main_table)
            self.gui.populate_table(self.main_table, acmt_list, self.table_keys)

    # register currently open achievement's id
    def register_id(self, event):
        #get widget based on event
        self.tree = event.widget
        # get row and use it as id
        acmt_id = self.tree.identify_row(event.y)
        #save id
        self.selected_acmt_id = acmt_id


    # get a single achievement and it's values
    def fetch_acmt_dict(self, index = 0):
        acmt_dict = self.process.get_achievement_by_data(index)
        self.current_dict = acmt_dict
        return acmt_dict
    
    # used by gui to display correct values
    def get_current_dict(self):
        return self.current_dict

    # gui button calls this to update value
    def change_value(self, new_value):
        id = self.selected_acmt_id
        acmt_list = self.process.update_achievement_data(id, self.current_key, new_value)
        acmt_dict = self.get_current_dict()

        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table,acmt_list, acmt_dict)

        self.gui.refresh_table(self.acmt_table)
        acmt_dict = self.fetch_acmt_dict(id)
        self.gui.populate_acmt_table(self.acmt_table, acmt_dict)
    
    # gui button calls this update value in all achievements
    def change_all_values(self, new_value):
        acmt_list = self.process.add_data_to_all_achievements(self.current_key, new_value)
        acmt_dict = self.get_current_dict()
        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table,acmt_list, acmt_dict)

        self.gui.refresh_table(self.acmt_table)
        acmt_dict = self.fetch_acmt_dict()
        self.gui.populate_acmt_table(self.acmt_table, acmt_dict)
    
    #filtering logic for achievement data
    def filter_values(self, format_var):
        # get format variable from widget
        format = format_var.get()

        #all the possible keys in a filter
        column_config = {
            'Steam': ('version', 'game_name', 'acmt_num',
                      'name_id', 'name_en', 'name_fi',
                      'name_token', 'desc_en', 'desc_fi',
                      'desc_token', 'hidden', 'icon',
                      'icon_locked', 'acmt_xp'),
            'MS Store': ('name_id', 'desc_id', 'hidden',
                        'icon', 'acmt_xp', 'desc_locked',
                        'base_acmt', 'display_order'),
            'Epic': ('name_id', 'hidden', 'acmt_xp',
                     'acmt_stat_tres', 'acmt_xp'),
            'All': ('version', 'game_name', 'acmt_num',
                    'name_id', 'name_en', 'name_fi',
                    'name_token', 'desc_en', 'desc_fi',
                    'desc_token', 'hidden', 'icon',
                    'icon_locked', 'acmt_xp','desc_id',
                    'desc_locked', 'base_acmt', 'display_order',
                    'acmt_stat_tres')
        }
        # get list of allowed values from filter
        key_list = column_config[format]
        new_headers = self.process.get_achievement_keys_from_dict(key_list, 0)
        current_list = self.process.get_filtered_list(key_list)
        column_list = list(new_headers.keys())
        #clear main table and fill it again
        self.gui.refresh_table(self.main_table)
        self.gui.name_table_columns(self.main_table, column_list)
        self.gui.populate_table(self.main_table, current_list, new_headers)

        # single achievement table filtering
        id = self.selected_acmt_id
        new_dict = self.process.get_achievement_keys_from_dict(key_list, id)
        self.gui.refresh_table(self.acmt_table)
        self.gui.populate_acmt_table(self.acmt_table, new_dict)
        # create edit window
    
    def edit_value(self, acmt_id, event=None):
        
        if event != None: #if event was given
            self.row_id = self.gui.identify_id(event) #identify row to find out which key:value pair was clicked
        
        self.acmt_id = acmt_id #set given achievement's id

        
        self.current_key = self.acmt_table.set(self.row_id, 'key')  # use row id and column name to find key
        
        self.keys_list = list(self.current_dict.keys()) # create a list of all keys from the dictionary
        
        self.current_key_index = self.keys_list.index(self.current_key)  # find the key we are currently editing from the list and use it's index
       
        self.gui.display_edit_value(self.current_key) # function to create labels etc widgets
    
    
    def move_to_next_acmt(self): 

        print("move to next")
        index = self.selected_acmt_id
        current_row = self.main_table.next(index)

        self.main_table.selection_set(current_row)

        self.gui.refresh_table(self.acmt_table)
        acmt_dict = self.fetch_acmt_dict(current_row)

        self.gui.populate_acmt_table(self.acmt_table, acmt_dict)
        self.edit_value(current_row)
    
    def move_to_next_value(self):
        
        new_key_index = (self.current_key_index + 1) % len(self.keys_list) #move to next index in acmt_dict
        self.current_key_index = new_key_index # set current index as new key index
        self.current_key = self.keys_list[new_key_index]  # update current key from list
        self.acmt_table.selection_set(new_key_index) # move the selection to next value too
        
        self.gui.display_edit_value(self.current_key ) # display widgets to show change to new key
    
    def open_acmt(self, acmt_id = None, event = None): # called when user selects acmt from table
        print("got to open acmt")
        print(event)
        if acmt_id is None:
            acmt_id = self.gui.identify_id(event) # identify id if it was not given 
        
        acmt_dict = self.fetch_acmt_dict(acmt_id) # get a dictionary of specified achievement's keys and values

        col_dict = {'key': 'None', 'value': 'None'} # columns for the table 
        
        if self.acmt_table is not None: 
            self.gui.refresh_table(self.acmt_table) # clear old table
        else:
            self.acmt_table = self.gui.create_table(col_dict) # create new acmt table RENAME SAME NAME FUNCTION
            
        for index, key in enumerate(acmt_dict): # fill values
            self.acmt_table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key])) #make a separate function for this!
        
        self.acmt_table.bind("<Double-1>", lambda event: self.edit_value(acmt_id, event)) # send clicked achievement's id and event
    

    # return given path's file extension
    def get_file_extension(self, selected_path):
        return os.path.splitext(selected_path)[1].lower()
   
    def run(self):
        # infinite loop for displaying gui
        self.root.mainloop()


def main():
    #create an instance of the converter
    acmt = AchievementConverter()
    #run to start
    acmt.run()


if __name__ == "__main__":
    main()



