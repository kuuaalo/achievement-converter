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
        self.current_filter= None
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
        
        self.acmt_list = self.process.fill_missing_values()
        
        # get dict for table headers
        table_keys = self.process.get_achievement_by_data()
        # save current headers in use for filtering purposes
        self.current_filter= table_keys


        if self.main_table is None:
            self.main_table = self.gui.create_table(table_keys)
            # bind key press events to table
            self.gui.bind_events(self.main_table)
            self.gui.configure_table(self.main_table)
            # values for filter creation
            formats = config.FILTER_FORMATS
            self.gui.create_filter(formats, 'formats')
            self.gui.populate_table(self.main_table, self.acmt_list)
        else:
            # if table already exists, clear it
            self.gui.refresh_table(self.main_table)
            self.gui.populate_table(self.main_table, self.acmt_list)

    # register currently id based on event
    def register_id(self, event):
        #get widget based on event
        self.tree = event.widget
        # get row and use it as id
        acmt_id = self.tree.identify_row(event.y)
        #save id
        return acmt_id

    
    # called when user selects cell from main table
    def open_acmt(self, event):
        print("got to open acmt")
        self.selected_acmt_id = self.register_id(event)
        acmt_id = self.selected_acmt_id
        
        self.current_filter = self.process.get_achievement_by_data(acmt_id)
        col_dict = {'key': 'None', 'value': 'None'} # columns for the table 
        
        if self.acmt_table is not None: 
            self.gui.refresh_table(self.acmt_table) # clear old table
        else:
            self.acmt_table = self.gui.create_table(col_dict) # create new acmt table RENAME SAME NAME FUNCTION
            
        for index, key in enumerate(self.current_filter): # fill values
            self.acmt_table.insert('', index='end', iid=str(index), values=(key, self.current_filter[key])) #make a separate function for this!
        
        
        self.acmt_table.bind("<Double-1>", lambda event: self.edit_value(self.register_id(event))) # send clicked achievement's id and event
        self.acmt_table.bind("<Double-1>", lambda event: self.register_id(event), add='+')

        
    def edit_value(self, row_id):
        
        self.row_id = row_id
        
        # use row id and column name to find key
        self.current_key = self.acmt_table.set(self.row_id, 'key') 
        
        # create a list of all keys from the dictionary
        self.keys_list = list(self.current_filter.keys())
        
        # find the key we are currently editing from the list and use it's index
        self.current_key_index = self.keys_list.index(self.current_key) 
        
        self.main_table.selection_set(self.selected_acmt_id)
        self.acmt_table.selection_set(self.row_id)

        # function to create labels etc widgets
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, self.selected_acmt_id)
        self.gui.display_edit_value(self.current_key, self.current_filter)


    # gui calls to update single achievement value
    def change_value(self, new_value):
        # change values in data
        id = self.selected_acmt_id
        # returns updated list 
        acmt_list = self.process.update_achievement_data(id, self.current_key, new_value)

        # update main table
        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table, acmt_list)

        # update achievement table
        self.gui.refresh_table(self.acmt_table)
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, id)
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
    
    # gui calls to update value in all achievements
    def change_all_values(self, new_value):
        #change values in data
        acmt_list = self.process.add_data_to_all_achievements(self.current_key, new_value)
        
        #update main table
        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table,acmt_list)

        # update achievement table
        self.gui.refresh_table(self.acmt_table)
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, self.selected_acmt_id)
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
    
    # display editable value in next achievement
    def move_to_next_acmt(self): 

        print("move to next")
        index = (int(self.selected_acmt_id) + 1) % len(self.acmt_list) #move to next index in acmt_dict
        self.selected_acmt_id = index
        print(index)

        # update achievement table
        self.gui.refresh_table(self.acmt_table)
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, index)
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
        
        self.edit_value(self.row_id)
    
    
    def move_to_next_value(self):
        print("move to next value")
        new_key_index = (self.current_key_index + 1) % len(self.current_filter) #move to next index in acmt_dict
        self.edit_value(new_key_index)
    
    def move_to_prev_value(self):
        print("move to next value")
        new_key_index = (self.current_key_index - 1) % len(self.keys_list) #move to next index in acmt_dict
        self.edit_value(new_key_index)
   
    #filtering logic for achievement data
    def filter_values(self, format_var):
        # get format variable from widget
        format = format_var.get()

        #all the possible keys in a filter
        filter_config = {
            'Steam': ('version','game_name','acmt_num',
                      'name_id','name_token',
                        'desc_token','hidden','icon',
                      'icon_locked','acmt_xp'),
            'MS Store': ('name_id','desc_id','hidden',
                        'icon','acmt_xp','desc_locked',
                        'base_acmt','display_order'),
            'Epic': ('name_id', 'hidden','acmt_xp',
                     'acmt_stat_tres','acmt_xp'),
            'All': ('version','game_name','acmt_num',
                    'name_id','name_token','desc_token',
                    'hidden','icon','icon_locked',
                    'acmt_xp','desc_id','desc_locked',
                    'base_acmt','display_order','acmt_stat_tres')
                    
        }

        # get list of allowed values from filter
        self.keys_list = filter_config[format]
        new_headers = self.process.get_achievement_keys_from_dict(self.keys_list, 0)
        current_list = self.process.get_filtered_list(self.keys_list)
        column_list = list(new_headers.keys())
        #clear main table and fill it again
        self.gui.refresh_table(self.main_table)
        self.gui.name_table_columns(self.main_table, column_list)
        self.gui.populate_table(self.main_table, current_list)

        # single achievement table filtering
        id = self.selected_acmt_id
        new_dict = self.process.get_achievement_keys_from_dict(self.keys_list, id)
        self.current_filter = new_dict
        self.gui.refresh_table(self.acmt_table)
        self.gui.populate_acmt_table(self.acmt_table, new_dict)
        # create edit window
    

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



