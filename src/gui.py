import tkinter as tk
from tkinter import ttk, Menu
from tkinter import Tk, Text
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo
import config

class AchievementConverterGUI:

    def __init__(self, root, controller):
        
        self.root = root
        self.root.title("Achievement Converter") #window name
        self.controller = controller#give reference to function in main on init
        
        self.root.geometry("1200x600")
        self.root.title("Achievement Converter")

        self.create_buttons()

        self.acmt_table = None
        self.edit_frame = None
        self.current_dict = None

    

    def create_table(self, acmt_dict):
        
        frame = tk.Frame(self.root, width=400, height=300)
        
        scrollbary = ttk.Scrollbar(frame, orient="vertical")
        scrollbarx = ttk.Scrollbar(frame, orient="horizontal")
        scrollbary.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        scrollbarx.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
        
        column_list = tuple(acmt_dict.keys()) #create a tuple of column names from dict keys
        self.table = ttk.Treeview(frame, columns=column_list, show = 'headings') #create table with tuple
        scrollbary.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbary.set)
        scrollbarx.configure(command=self.table.xview)
        self.table.configure(xscrollcommand=scrollbarx.set)
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        frame.pack(fill=tk.BOTH,expand=True, padx=30, pady=30)

        for col in self.table["columns"]: #iterate trough the columns
            self.table.heading(col, text = col) #set column names as headers

        return self.table
    
    #listens to double click on table, send info to edit value function
    def bind_events(self, table):
        table.bind("<Double-1>", lambda event: self.open_acmt(None, event))
    
    def configure_table(self, table):
        table.tag_configure('null_value', background='red') #tag to display red color for null values

    def populate_table(self, table, acmt_list, acmt_dict):
        
        self.current_dict = acmt_dict
        
        for index, item in enumerate(acmt_list):
            row_values = list(item.values()) 
            if (None in row_values): #add tag if acmt has null value
                table.insert('', index='end', iid=str(index), values=list(item.values()), tags=('null_value',))
            else:
                table.insert('', index='end', iid=str(index), values=list(item.values()))
    
    def refresh_table(self, table):
        table.delete(*table.get_children())
        return True
    
    def identify_id(self, event):
        self.tree = event.widget #get widget based on event
        acmt_id = self.tree.identify_row(event.y)  # get row

        return acmt_id

    
    def open_acmt(self, acmt_id = None, event = None): #called when user selects acmt from table
        
        if acmt_id is None:
            acmt_id = self.identify_id(event)
        self.current_acmt_id = acmt_id 
        
        print(acmt_id)
        acmt_dict = self.controller.fetch_acmt_dict(acmt_id)

        col_dict = {'key': 'None', 'value': 'None'} #columns for the table
        
        if self.acmt_table is not None: #create new acmt table
            print("Window is already open!")
            self.refresh_table(self.acmt_table)
        else:
            self.acmt_table = self.create_table(col_dict)
    
        for index, key in enumerate(acmt_dict): #fill values
            self.acmt_table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))

        self.acmt_table.bind("<Double-1>", lambda event: self.edit_value(acmt_id, event)) #send clicked achievement's id and event

        
    def edit_value(self, acmt_id, event=None):
        
        if event != None: #if event was given
            self.row_id = self.identify_id(event) #identify row to find out which key:value pair was clicked
        
        self.acmt_id = acmt_id #set given achievement's id

        self.edit_frame = tk.Toplevel(self.root)
        
        self.current_key = self.acmt_table.set(self.row_id, 'key')  # use row id and column name to find key
        print("this is the current key" + self.current_key)
        
        self.keys_list = list(self.current_dict.keys())         # create a list of all keys from the dictionary
        print(self.current_dict)
        
        self.current_key_index = self.keys_list.index(self.current_key)  # find the key we are currently editing from the list and use it's index
        print("this is the list it's being looked from")
        print(self.keys_list)
        print("this is it's index")
        print(self.current_key_index)
        self.display_edit_value()
        
    
    def display_edit_value(self):

        current_value = self.current_dict[self.current_key] # Get the value for the current key
        
        
        for widget in self.edit_frame.winfo_children():
            widget.destroy()

        # Create widgets for displaying and editing
        field_label = ttk.Label(self.edit_frame, text="Key: " + self.current_key)  # Show the key
        separator = ttk.Separator(self.edit_frame, orient='horizontal')
        edit_label = ttk.Label(self.edit_frame, text="Edit value for this key:")
        
        # Entry field for the value
        self.entry_var = tk.StringVar(value=current_value)
        self.field = ttk.Entry(self.edit_frame, textvariable=self.entry_var)  # Entry box for value editing


        field_label.pack(expand=True)
        separator.pack(fill='x')
        edit_label.pack(expand=True)
        self.field.pack(expand=True)
        self.create_edit_menu_buttons(self.edit_frame)
        
        


    def move_to_next_acmt(self, index):

        print("move to next")
        current_row = self.table.next(index)

        self.table.selection_set(current_row)

        self.refresh_table(self.acmt_table)

        acmt_dict = self.controller.fetch_acmt_dict(current_row)

        self.populate_acmt_table(acmt_dict)
        self.edit_value(current_row)
    
    def move_to_next_value(self):
        
        new_key_index = (self.current_key_index + 1) % len(self.keys_list) #move to next index in acmt_dict
        self.current_key_index = new_key_index #set current index as new key index
        self.current_key = self.keys_list[new_key_index]  # update current key from list
        self.acmt_table.selection_set(new_key_index)
        
        self.display_edit_value() #display widgets to show change to new key
        


    
    def populate_acmt_table(self, acmt_dict):
        print(acmt_dict)
        for index, key in enumerate(acmt_dict):
            print(key)
            self.acmt_table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))
    

 

       


    def create_edit_menu_buttons(self, tree):
        
        edit_frame = tree

        replaceall_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace value in ALL achievements",
            command=lambda:self.handle_submit(1, self.current_key, self.acmt_id)
        )
        replacethis_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace the value in this achievement",
            command=lambda:self.handle_submit(2, self.current_key, self.acmt_id)
        )
        next_acmt_button = ttk.Button(
            edit_frame,
            text="Edit next achievement",
            command=lambda:self.move_to_next_acmt(self.acmt_id)
        )
        next_value_button = ttk.Button(
            edit_frame,
            text="Edit next value",
            command=lambda:self.move_to_next_value()
        )

        replaceall_button.pack(expand=True, padx=10, pady=10)
        replacethis_button.pack(expand=True, padx=10, pady=10)
        next_acmt_button.pack(expand=True, padx=10, pady=10)
        next_value_button.pack(expand=True, padx=10, pady=10)


    
    def create_filter(self, table, filter_names, filter_label):
        lf = ttk.LabelFrame(self.root, text=filter_label)
        lf.pack(side=tk.TOP, expand=True)

        format_var = tk.StringVar()
        formats = filter_names

        for format in formats:
            # create a radio button
            radio = ttk.Radiobutton(lf, text=format, value=format, command=lambda: self.filter_values(format_var, table), variable=format_var)
            radio.pack(side=tk.LEFT, expand=False, padx=5, pady=5)

    def filter_values(self, format_var, table):
        format = format_var.get()
        print(format) #hidelocalisations to work with specific formats
        column_config = {
            'Steam': ('version', 'game_name', 'acmt_num', 'name_id', 'name_en', 'name_fi', 'name_token', 'desc_en', 'desc_fi', 'desc_token', 'hidden', 'icon', 'icon_locked', 'acmt_xp'),
            'MS Store': ('name_id', 'desc_id', 'hidden', 'icon', 'acmt_xp', 'desc_locked', 'base_acmt', 'display_order'),
            'Epic': ('name_id', 'hidden', 'acmt_xp', 'acmt_stat_tres', 'acmt_xp'),
            'All': '#all'
        }

        # Get all available columns
        all_columns = table['columns']

        if format in column_config:
            if column_config[format] == '#all':
                # Show all columns
                table["displaycolumns"] = '#all'
                self.valid_columns = table["displaycolumns"]
            else:
                # Filter columns that exist in all_columns
                self.valid_columns = [col for col in column_config[format] if col in all_columns]
                table["displaycolumns"] = self.valid_columns
        else:
            print("Unknown format")
        
        #for getting acmt_view filtering
        filter_list = column_config[format]
        id = self.current_acmt_id
        print(id)
        new_dict = self.controller.fetch_filtered_dict(filter_list, id)
        self.refresh_table(self.acmt_table)
        self.populate_acmt_table(new_dict)
        self.current_dict = new_dict
        
    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=False)
        
        open_button = ttk.Button( #button to import file
            button_frame,
            text="Import achievement file",
            command=lambda: self.select_file(1) #sends a parameter to select file
        )
        
        export_button = ttk.Button( #button to export file
            button_frame,
            text="Export achievement file",
            command=lambda: self.select_file(2)
        )

        save_button = ttk.Button( #button to save project file
            button_frame,
            text="Save achievement file",
            command=lambda: self.select_file(3)
        )

        exit_button = ttk.Button( #button to exit program
            button_frame,
            text="Exit",
            command=lambda: self.root.quit() #quit program exits the mainloop
        )

        #button placement on grid
        open_button.pack(side=tk.LEFT, expand=False)
        export_button.pack(side=tk.LEFT, expand=False)
        save_button.pack(side=tk.LEFT, expand=False)
        exit_button.pack(side=tk.LEFT, expand=False)
    
    def show_error(self, error_title, error_msg): #shows error pop-up
        showwarning(title=error_title, message=error_msg)

    def handle_submit(self, command, key, index):
        new_value = self.field.get()
        if (command == 1): 
            self.controller.data_handler(command, key, new_value)
        elif(command == 2):
            self.controller.data_handler(command, key, new_value, index)
        self.refresh_table(self.acmt_table)
        acmt_dict = self.controller.fetch_acmt_dict(index)
        self.populate_acmt_table(acmt_dict)
            

    def select_file(self, command): #should these be in main?
        if (command == 1): #prompt to open file for importing
            file_path = fd.askopenfilename(title="Import achievement file")
        elif (command == 2): #prompt to pick directory to export file
            file_path = fd.asksaveasfilename(title="Export project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("VDF files", "*.vdf"), ("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
            #lisäsin tähän VDF tuen
        elif (command == 3): #prompt to save a project file
            file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("JSON", "*.json")])
        
        self.controller.file_handler(file_path, command) #callback function, new path and variable to main
        print(file_path)

