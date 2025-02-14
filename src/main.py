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
        # single achievement display table
        self.acmt_table = None
        # selected achievement's id
        self.selected_acmt_id = None


    # import achievement file
    def import_file(self):
        # open filedialog and save paths
        file_path = fd.askopenfilename(title="Import achievement file")
        locale_file_path = fd.askopenfilename(title="Import localization file")
        # get file extension
        acmt_platform = self.get_file_extension(file_path)
        # init read and give params
        self.read = Read(file_path, locale_file_path, acmt_platform, self.process, self.gui)
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
        file_path = fd.asksaveasfilename(title="Export achievement file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("VDF files", "*.vdf"), ("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
        # send path to get extension
        acmt_platform = self.get_file_extension(file_path)
        # pass path, name and model to write
        self.write = Write(file_path, acmt_platform, self.process, self.gui)
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
        if table_keys == False:
            self.gui.show_error("No data provided", "The file provided is empty, corrupt or Achievement Converter can't read it.")
        else:
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
                self.refresh_all()

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
        col_dict = config.COLUMN_HEADERS
        
        if self.acmt_table is not None: 
            # clear old table
            self.gui.refresh_table(self.acmt_table)
        else:
            # make new table
            self.acmt_table = self.gui.create_table(col_dict)
            self.gui.configure_table(self.acmt_table)
        
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
  
        # get achievement's id for editing
        self.acmt_table.bind("<Double-1>", lambda event: self.edit_value(self.register_id(event)))

    # called when user selects cell from achievement table
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
        self.process.update_achievement_data(id, self.current_key, new_value)
        self.acmt_list = self.process.get_filtered_list(self.keys_list)

        # update main table
        #self.gui.refresh_table(self.main_table)
        #self.gui.populate_table(self.main_table, acmt_list)

        # update achievement table
        #self.gui.refresh_table(self.acmt_table)
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, id)
        #self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
        self.refresh_all()
    
    # gui calls to update value in all achievements
    def change_all_values(self, new_value):
        #change values in data
        self.process.add_data_to_all_achievements(self.current_key, new_value)
        acmt_list = self.process.get_filtered_list(self.keys_list)
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
        # move to next index in acmt_dict
        index = (int(self.selected_acmt_id) + 1) % len(self.acmt_list)
        self.selected_acmt_id = index
        print(index)

        # update achievement table
        self.gui.refresh_table(self.acmt_table)
        self.current_filter = self.process.get_achievement_keys_from_dict(self.keys_list, self.selected_acmt_id)
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)
        
        self.edit_value(self.row_id)
    
    
    def move_to_next_value(self):
        print("move to next value")
        new_key_index = (self.current_key_index + 1) % len(self.current_filter)
        self.edit_value(new_key_index)
    
    def move_to_prev_value(self):
        print("move to next value")
        new_key_index = (self.current_key_index - 1) % len(self.keys_list)
        self.edit_value(new_key_index)
   
    #filtering logic for achievement data
    def filter_values(self, format_var):
        # get format variable from widget
        format = format_var.get()

        # get filter values from config
        filter_config = config.FILTER_CONFIG
        id = self.selected_acmt_id

        # get list of allowed values from filter
        self.keys_list = filter_config[format]
        new_headers = self.process.get_achievement_keys_from_dict(self.keys_list, id)
        self.current_filter = new_headers
        self.acmt_list = self.process.get_filtered_list(self.keys_list)
        self.refresh_all()

    

    # return given path's file extension
    def get_file_extension(self, selected_path):
        return os.path.splitext(selected_path)[1].lower()
    
    def refresh_all(self):
        self.keys_list = list(self.current_filter.keys())

        self.gui.refresh_table(self.main_table)
        self.gui.name_table_columns(self.main_table, self.keys_list)
        self.gui.populate_table(self.main_table, self.acmt_list)
        
        self.gui.refresh_table(self.acmt_table)
        self.gui.populate_acmt_table(self.acmt_table, self.current_filter)

   
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



