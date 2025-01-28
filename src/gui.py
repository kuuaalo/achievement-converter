import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

class AchievementConverterGUI:

    def __init__(self, root, controller):
        
        self.root = root
        self.root.title("Achievement Converter") #window name
        self.controller = controller#give reference to function in main on init
        
        self.root.geometry("1200x600")
        self.root.title("Achievement Converter")

        self.create_buttons()

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
        #table.bind("<Double-1>", lambda event: self.open_acmt(None, event))
        table.bind("<Double-1>", lambda event: self.controller.register_id(event))
        table.bind("<Double-1>", lambda event: self.controller.open_acmt(event), add='+')
    
    def configure_table(self, table):
        table.tag_configure('null_value', background='red') #tag to display red color for null values !!fix!!

    def populate_table(self, table, acmt_list):
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
    
        
    
    def display_edit_value(self, current_key, current_dict):
        
        if not self.edit_frame or not self.edit_frame.winfo_exists():
            self.edit_frame = tk.Toplevel(self.root) # create frame for editing
            self.edit_frame.geometry("300x300")
        
        print("got to display value")
        current_value = current_dict[current_key] # Get the value for the current key

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
    

    
    def create_filter(self, filter_names, filter_label): #create a filter
        lf = ttk.LabelFrame(self.root, text=filter_label)
        lf.pack(side=tk.TOP, expand=True)

        format_var = tk.StringVar()
        formats = filter_names

        for format in formats:
            # create a radio button
            radio = ttk.Radiobutton(lf, text=format, value=format, command=lambda: self.controller.filter_values(format_var), variable=format_var) #command=lambda: self.filter_values(format_var, table), variable=format_var)
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


  

