# MIT License
# Copyright (c) [2025] [kuuaalo]
# See LICENSE file for more details.

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

class AchievementConverterGUI:

    def __init__(self, root, controller):

        self.root = root
        self.root.title("Achievement Converter")
        self.controller = controller

        self.root.geometry("1200x600")
        self.root.title("Achievement Converter")

        self.create_buttons()

        self.edit_frame = None 
        
    
    # general function for creating table objects
    def create_table(self, acmt_dict):

        frame = tk.Frame(self.root, width=400, height=300)

        scrollbary = ttk.Scrollbar(frame, orient="vertical")
        scrollbarx = ttk.Scrollbar(frame, orient="horizontal")
        scrollbary.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        scrollbarx.pack(side=tk.BOTTOM, expand=False, fill=tk.X)

        # create a tuple of column names from dict keys
        column_list = tuple(acmt_dict.keys())

        # create table from tuple
        self.table = ttk.Treeview(frame, columns=column_list, show = 'headings')

        # scrollbar setup
        scrollbary.configure(command=self.table.yview) 
        self.table.configure(yscrollcommand=scrollbary.set)
        scrollbarx.configure(command=self.table.xview)
        self.table.configure(xscrollcommand=scrollbarx.set)

        # pack gui items
        self.table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        frame.pack(fill=tk.BOTH,expand=True, padx=30, pady=30)

        #iterate trough column and set names as headers
        for col in self.table["columns"]:
            self.table.heading(col, text = col)

        return self.table
    
    # bind double click
    def bind_events(self, table):
        table.bind("<Double-1>", lambda event: self.controller.open_acmt(event))
    
    # bind tag to display null value achievements
    def configure_table(self, table):
        table.tag_configure('null_value', background='orange')

    # fill main table with items
    def populate_table(self, table, acmt_list):
        print(f"Populating table")
        
        for index, item in enumerate(acmt_list):
            row_values = list(item.values()) 
            #add tag if acmt has null value
            if (None in row_values):
                table.insert('', index='end', iid=str(index), values=list(item.values()), tags=('null_value',))
            else:
                table.insert('', index='end', iid=str(index), values=list(item.values()))
    
    # populate achievement table
    def populate_acmt_table(self, table, acmt_dict):
        for index, key in enumerate(acmt_dict):
            print(key)
            table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))
    
    # empty given table
    def refresh_table(self, table):
        table.delete(*table.get_children())
        return True
    

    def name_table_columns(self, table, columns):
        table["columns"] = columns
        
        #iterate trough columns and set headers
        for col in table["columns"]:
            table.heading(col, text = col)

        return True
    
    # create edit window gui elements
    def display_edit_value(self, current_key, current_dict):
        
        # create frame for editing if it doesn't exist yet
        if not self.edit_frame or not self.edit_frame.winfo_exists():
            self.edit_frame = tk.Toplevel(self.root)
            self.edit_frame.geometry("300x300")
        
        print("got to display value")
        # Get the value to display what user is editing
        current_value = current_dict[current_key] 
        
        # destroy old widgets
        for widget in self.edit_frame.winfo_children():
            widget.destroy()

        # Create widgets for displaying and editing
        field_label = ttk.Label(self.edit_frame, text="Key: " + current_key)
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
    

    def create_edit_menu_buttons(self, tree):
        
        edit_frame = tree
        
        replace_frame = tk.Frame(edit_frame)
        replace_frame.pack(side=tk.TOP, fill='x', expand=True)

        next_frame = tk.Frame(edit_frame)
        next_frame.pack(side=tk.TOP, fill='x', expand=True)
        
        #replace value in this achievement
        replacethis_button = ttk.Button( #button to import file
            replace_frame,
            text="Replace value",
            command=lambda:self.controller.change_value(self.field.get())
        )
        # mass replace value in all achievements
        replaceall_button = ttk.Button(
            replace_frame,
            text="Replace in ALL",
            command=lambda:self.controller.change_all_values(self.field.get())
        )
        next_acmt_button = ttk.Button(
            next_frame,
            text="Edit next achievement",
            command=lambda:self.controller.move_to_next_acmt()
        )
        next_value_button = ttk.Button(
            next_frame,
            text="next-->",
            command=lambda:self.controller.move_to_next_value()
        )
        prev_value_button = ttk.Button(
            next_frame,
            text="<--prev",
            command=lambda:self.controller.move_to_prev_value()
        )
    

        replacethis_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        replaceall_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        prev_value_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        next_value_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
        next_acmt_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10, ipadx=5, ipady=5)
    

    def create_filter(self, filter_names, filter_label):
        lf = ttk.LabelFrame(self.root, text=filter_label)
        lf.pack(side=tk.TOP, expand=True)

        format_var = tk.StringVar()
        formats = filter_names

        for format in formats:
            # create a radio button
            radio = ttk.Radiobutton(lf, text=format, value=format, command=lambda: self.controller.filter_values(format_var), variable=format_var)
            radio.pack(side=tk.LEFT, expand=False, padx=5, pady=5)

    # create main buttons
    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=False)
        
        # button to import file
        open_button = ttk.Button(
            button_frame,
            text="Import achievement file",
            command=lambda: self.controller.import_file()
        )
        # button to export file
        export_button = ttk.Button(
            button_frame,
            text="Export achievement file",
            command=lambda: self.controller.export_file()
        )
        # button to save project file
        save_button = ttk.Button(
            button_frame,
            text="Save achievement file",
            command=lambda: self.controller.save_file()
        )
        # button to save project file
        load_button = ttk.Button(
            button_frame,
            text="Load achievement file",
            command=lambda: self.controller.load_file()
        )
        # button to exit program
        exit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=lambda: self.root.quit()
        )

        #button placement on grid
        open_button.pack(side=tk.LEFT, expand=False)
        export_button.pack(side=tk.LEFT, expand=False)
        save_button.pack(side=tk.LEFT, expand=False)
        load_button.pack(side=tk.LEFT, expand=False)
        exit_button.pack(side=tk.LEFT, expand=False)
    
    # display error pop-up
    def show_error(self, error_title, error_msg):
        showwarning(title=error_title, message=error_msg)

