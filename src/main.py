
import tkinter as tk
import os

# internal modules
from gui import AchievementConverterGUI #import gui
from process.process import Process # import all functions from process
from write.write import Write # import all functions from write
from read.read import Read # import all functions from read
from tkinter import filedialog as fd
import config

class AchievementConverter:
    def __init__(self):
        self.root = tk.Tk() # set tkinter as root
        self.process = Process(False, False) # init and give parameters
        self.gui = AchievementConverterGUI(self.root, self) # init gui with root and self
        self.main_table = None
        self.current_dict = None
        self.selected_acmt_id = None #init the id so when filtering is called, it has something

    # import achievement file
    def import_file(self):
        # open filedialog and save path
        acmt_file_path = fd.askopenfilename(title="Import achievement file")
        locale_file_path = fd.askopenfilename(title="Import localization file")

        # get file extension
        acmt_platform = self.get_file_extension(acmt_file_path)
        # init read and give params
        self.read = Read(acmt_file_path, locale_file_path, acmt_platform, self.process)
        self.read.run()
        # get list of all achievements and keys
        acmt_list = self.process.fill_missing_values()

        # table creation starts here
        self.table_keys = self.fetch_acmt_dict() # get dict for table headers
        self.current_dict = self.table_keys

        if self.main_table is None:
            self.main_table = self.gui.create_table(self.table_keys) # create a new table if there's none
            self.gui.bind_events(self.main_table) # bind key press events to table
            self.gui.configure_table(self.main_table) # et some styling
            formats = ('Steam', 'Epic', 'MS Store', 'All') # values for filter creation
            self.gui.create_filter(self.main_table, formats, 'formats') # create filter
            self.gui.populate_table(self.main_table, acmt_list, self.table_keys) #first round didn't render any data, added this to populate first import
        else:
            self.gui.refresh_table(self.main_table) # if table already exists, clear it
            self.gui.populate_table(self.main_table, acmt_list, self.table_keys) # add values to table

    # export achievement file
    def export_file(self):
        file_path = fd.asksaveasfilename(title="Export project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("VDF files", "*.vdf"), ("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
        self.acmt_platform = self.get_file_extension(file_path) # send path to func and get extension
        print(self.acmt_platform)
        self.acmt_file_path = file_path # set the file path and name
        self.write = Write(self.acmt_file_path, self.acmt_platform, self.process) # pass path and name to write
        self.write.run() # run write

    # save project file as json
    def save_file(self):
        file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("JSON", "*.json")])
        self.acmt_file_path = file_path
        self.process.save_data(self.acmt_file_path)

    # load project file
    def load_file(self):
        file_path = fd.askopenfilename(title="Load project file", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("JSON", "*.json")])
        self.acmt_file_path = file_path
        self.process.load_data(self.acmt_file_path)

        # get list of all achievements and keys
        acmt_list = self.process.fill_missing_values()

        # table creation starts here
        self.acmt_dict = self.fetch_acmt_dict() # get dict for table headers
        self.current_dict = self.acmt_dict

        if self.main_table is None:
            self.main_table = self.gui.create_table(self.acmt_dict) # create a new table if there's none
            self.gui.bind_events(self.main_table) # bind key press events to table
            self.gui.configure_table(self.main_table) # et some styling
            formats = ('Steam', 'Epic', 'MS Store', 'All') # values for filter creation
            self.gui.create_filter(self.main_table, formats, 'formats') # create filter
            self.gui.populate_table(self.main_table, acmt_list, self.acmt_dict) #first round didn't render any data, added this to populate first import
        else:
            self.gui.refresh_table(self.main_table) # if table already exists, clear it
            self.gui.populate_table(self.main_table, acmt_list, self.acmt_dict) # add values to table

    def register_id(self, event):
        self.tree = event.widget #get widget based on event
        acmt_id = self.tree.identify_row(event.y)  # get row
        print(acmt_id)
        self.selected_acmt_id = acmt_id

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

        key_list = column_config[format]

        new_headers = self.process.get_achievement_keys_from_dict(key_list, 0)

        current_list = self.process.get_filtered_list(key_list)
        column_list = list(new_headers.keys())

        self.gui.refresh_table(self.main_table)
        self.gui.name_table_columns(self.main_table, column_list)
        self.gui.populate_table(self.main_table, current_list, new_headers)


        # for getting acmt_view filtering

        id = self.selected_acmt_id
        print(id)
        new_dict = self.process.get_achievement_keys_from_dict(key_list, id)
        self.gui.refresh_table(table)
        self.gui.populate_acmt_table(table, new_dict)

    # get a single achievement and it's values
    def fetch_acmt_dict(self, index = 0):
        acmt_dict = self.process.get_achievement_by_data(index)
        self.current_dict = acmt_dict
        return acmt_dict

    def get_current_dict(self):
        return self.current_dict


    # send new values to be added to dict
    def data_handler(self, command, key, new_value, id = None):
        if(command==1):
            acmt_list = self.process.add_data_to_all_achievements(key, new_value)
        elif(command==2):
            acmt_list = self.process.update_achievement_data(id, key, new_value)

        acmt_dict = self.fetch_acmt_dict()

        self.gui.refresh_table(self.main_table)
        self.gui.populate_table(self.main_table,acmt_list, acmt_dict)


    def get_file_extension(self, selected_path):
        return os.path.splitext(selected_path)[1].lower()

    def run(self): # infinite loop for displaying gui
        self.root.mainloop()


def main():
    acmt = AchievementConverter() #create an instance of the converter
    acmt.run() #run to start


if __name__ == "__main__":
    main()



