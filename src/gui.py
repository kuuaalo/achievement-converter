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

        self.acmt_table = None #single achievement display table
        self.edit_frame = None 
        

    def create_table(self, acmt_dict): #general function for creating table objects
        
        frame = tk.Frame(self.root, width=400, height=300)
        
        scrollbary = ttk.Scrollbar(frame, orient="vertical")
        scrollbarx = ttk.Scrollbar(frame, orient="horizontal")
        scrollbary.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        scrollbarx.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
        
        column_list = tuple(acmt_dict.keys()) #create a tuple of column names from dict keys
        print("making table") ###################debug stuff #########################
        self.table = ttk.Treeview(frame, columns=column_list, show = 'headings') #create table from tuple
        
        #scrollbar setup
        scrollbary.configure(command=self.table.yview) 
        self.table.configure(yscrollcommand=scrollbary.set)
        scrollbarx.configure(command=self.table.xview)
        self.table.configure(xscrollcommand=scrollbarx.set)
        
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        frame.pack(fill=tk.BOTH,expand=True, padx=30, pady=30)

        for col in self.table["columns"]: #iterate trough the columns
            self.table.heading(col, text = col) #set column names as headers
        
        return self.table
    
    
    def bind_events(self, table):
        table.bind("<Double-1>", lambda event: self.open_acmt(None, event))
        table.bind("<Double-1>", lambda event: self.controller.register_id(event), add='+')
    
    def configure_table(self, table):
        table.tag_configure('null_value', background='red') #tag to display red color for null values !!fix!!

    def populate_table(self, table, acmt_list, acmt_dict):
        print(f"Populating table")
        
        for index, item in enumerate(acmt_list): #insert items to table !!remove enumerate?!
            row_values = list(item.values()) 
            if (None in row_values): #add tag if acmt has null value
                table.insert('', index='end', iid=str(index), values=list(item.values()), tags=('null_value',))
            else:
                table.insert('', index='end', iid=str(index), values=list(item.values()))
    
    def populate_acmt_table(self, table, acmt_dict): #populate achievement table !!try to combine to other populate in the future!!
        self.acmt_table = table
        for index, key in enumerate(acmt_dict):
            print(key)
            table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))
    
    def refresh_table(self, table): #empty given table
        table.delete(*table.get_children())
        return True
    
    def name_table_columns(self, table, columns): #empty given table
        table["columns"] = columns

        for col in table["columns"]: #iterate trough the columns
            table.heading(col, text = col) #set column names as headers

        return True
    
    def identify_id(self, event): #POSSIBLY OBSOLETE. REMOVE
        self.tree = event.widget #get widget based on event
        acmt_id = self.tree.identify_row(event.y)  # get row

        return acmt_id

    
    def open_acmt(self, acmt_id = None, event = None): # called when user selects acmt from table
        
        if acmt_id is None:
            acmt_id = self.identify_id(event) # identify id if it was not given 
        
        acmt_dict = self.controller.fetch_acmt_dict(acmt_id) # get a dictionary of specified achievement's keys and values

        col_dict = {'key': 'None', 'value': 'None'} # columns for the table 
        
        if self.acmt_table is not None: 
            self.refresh_table(self.acmt_table) # clear old table
        else:
            self.acmt_table = self.create_table(col_dict) # create new acmt table
            
        for index, key in enumerate(acmt_dict): # fill values
            self.acmt_table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))
        
        acmt_list = self.controller.get_locale_dict()
        print(acmt_list)
        self.acmt_table.insert('', index='end', values=('locales', acmt_list)) # hardcoded for first acmt
        #self.acmt_table.bind("<Double-1>", lambda event: self.edit_value(acmt_id, event)) # send clicked achievement's id and event
        self.acmt_table.bind("<Double-1>", lambda event: self.controller.edit_value(acmt_id, self.acmt_table, event)) # send clicked achievement's id and event

    # create edit window
    def edit_value(self, acmt_id, event=None):
        
        if event != None: #if event was given
            self.row_id = self.identify_id(event) #identify row to find out which key:value pair was clicked
        
        self.acmt_id = acmt_id #set given achievement's id

        self.edit_frame = tk.Toplevel(self.root) # create frame for editing
        
        self.current_key = self.acmt_table.set(self.row_id, 'key')  # use row id and column name to find key
        
        current_dict = self.controller.get_current_dict() #stupid fix. improve later with callback / observer
        
        self.keys_list = list(current_dict.keys()) # create a list of all keys from the dictionary
        
        self.current_key_index = self.keys_list.index(self.current_key)  # find the key we are currently editing from the list and use it's index
       
        self.display_edit_value() # function to create labels etc widgets

    
    def display_edit_value(self, current_key):
        self.edit_frame = tk.Toplevel(self.root) # create frame for editing
        
        current_dict = self.controller.get_current_dict() #stupid fix. improve later with callback / observer
        print("got to display value")
        current_value = current_dict[current_key] # Get the value for the current key
        print(current_key)
        print(current_value)
        self.edit_frame.geometry("300x300")
        
        for widget in self.edit_frame.winfo_children(): #destroy old widgets just in case
            widget.destroy()

        # Create widgets for displaying and editing
        field_label = ttk.Label(self.edit_frame, text="Key: " + current_key)  # Show the key
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
        
    
    def move_to_next_value(self):
        
        new_key_index = (self.current_key_index + 1) % len(self.keys_list) #move to next index in acmt_dict
        self.current_key_index = new_key_index # set current index as new key index
        self.current_key = self.keys_list[new_key_index]  # update current key from list
        self.acmt_table.selection_set(new_key_index) # move the selection to next value too
        
        self.display_edit_value() # display widgets to show change to new key
    

    def create_edit_menu_buttons(self, tree):
        
        edit_frame = tree
        
        replace_frame = tk.Frame(edit_frame)
        replace_frame.pack(side=tk.TOP, fill='x', expand=True)

        next_frame = tk.Frame(edit_frame)
        next_frame.pack(side=tk.TOP, fill='x', expand=True)
        
        replacethis_button = ttk.Button( #button to import file
            replace_frame,
            text="Replace value",
            #command=lambda:self.handle_submit(2, self.current_key, self.acmt_id)
            command=lambda:self.controller.change_value(self.current_key, self.acmt_id, self.acmt_table, self.field.get())
        )
        replaceall_button = ttk.Button( #button to import file
            replace_frame,
            text="Replace in ALL",
            #command=lambda:self.handle_submit(1, self.current_key, self.acmt_id)
            command=lambda:self.controller.change_all_values(self.current_key, self.acmt_table, self.field.get())
        )
        next_acmt_button = ttk.Button(
            next_frame,
            text="Edit next achievement",
            #command=lambda:self.move_to_next_acmt(self.acmt_id)
            command=lambda:self.controller.move_to_next_acmt(self.acmt_table)
        )
        next_value_button = ttk.Button(
            next_frame,
            text="Edit next value",
            command=lambda:self.move_to_next_value()
        )
    

        replacethis_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        replaceall_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)

        next_acmt_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        next_value_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
    

    
    def create_filter(self, table, filter_names, filter_label): #create a filter
        lf = ttk.LabelFrame(self.root, text=filter_label)
        lf.pack(side=tk.TOP, expand=True)

        format_var = tk.StringVar()
        formats = filter_names

        for format in formats:
            # create a radio button
            radio = ttk.Radiobutton(lf, text=format, value=format, command=lambda: self.controller.filter_values(format_var, self.acmt_table), variable=format_var) #command=lambda: self.filter_values(format_var, table), variable=format_var)
            radio.pack(side=tk.LEFT, expand=False, padx=5, pady=5)

        
    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=False)
        
        open_button = ttk.Button( #button to import file
            button_frame,
            text="Import achievement file",
            command=lambda: self.controller.import_file()
        )
        
        export_button = ttk.Button( #button to export file
            button_frame,
            text="Export achievement file",
            command=lambda: self.controller.export_file()
        )

        save_button = ttk.Button( #button to save project file
            button_frame,
            text="Save achievement file",
            command=lambda: self.controller.save_file()
        )

        load_button = ttk.Button( #button to save project file
            button_frame,
            text="Load achievement file",
            command=lambda: self.controller.load_file()
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
        load_button.pack(side=tk.LEFT, expand=False)
        exit_button.pack(side=tk.LEFT, expand=False)
    
    def show_error(self, error_title, error_msg): #shows error pop-up
        showwarning(title=error_title, message=error_msg)


  

