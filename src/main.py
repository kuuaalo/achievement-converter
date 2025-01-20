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
            #self.locale_table = self.gui.create_table(self.table_keys)
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

    #filtering logic for achievement data
    def filter_values(self, format_var, table):
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
        self.gui.refresh_table(table)
        self.gui.populate_acmt_table(table, new_dict)

    # get a single achievement and it's values
    def fetch_acmt_dict(self, index = 0):
        acmt_dict = self.process.get_achievement_by_data(index)
        self.current_dict = acmt_dict
        return acmt_dict
    
    # used bu gui to display correct values
    def get_current_dict(self):
        return self.current_dict

    # send new values to be added to dict
    def data_handler(self, command, key, new_value, id = None):
        if(command==1):
            acmt_list = self.process.add_data_to_all_achievements(key, new_value)
        elif(command==2):
            acmt_list = self.process.update_achievement_data(id, key, new_value)

        #acmt_dict = self.fetch_acmt_dict()
        acmt_dict = self.get_current_dict()

        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table,acmt_list, acmt_dict)

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



