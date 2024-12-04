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
        #self.selected_path = None #empty variable for file path, should the config be used here?
        
        self.root.geometry("1200x600")
        self.root.title("Achievement Converter")

        self.create_menu() #call function to create menu

        self.create_buttons()
        


    def create_menu(self):
        #menu creation (in progress)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar)

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
    
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


        #listens to double click on table, send info to edit value function
        self.table.bind("<Double-1>", lambda event: self.open_acmt(event, acmt_dict))
        self.table.tag_configure('null_value', background='red') #tag to display red color for null values
        return self.table

    def populate_table(self, table, acmt_list):
        for index, item in enumerate(acmt_list):
            row_values = list(item.values()) 
            if (None in row_values): #add tag if acmt has null value
                table.insert('', index='end', iid=str(index), values=list(item.values()), tags=('null_value',))
            else:
                table.insert('', index='end', iid=str(index), values=list(item.values()))
    
    def refresh_table(self, table):
        table.delete(*table.get_children())
        return True
        
    def edit_value(self, event, acmt_id):

        edit_frame = tk.Toplevel(self.root) # pop-up window 
        tree = event.widget # get widget based on event
        row_id = tree.identify_row(event.y)  # get row
        
        print(row_id)
        key_name = tree.set(row_id, 'key')  # get the clicked value
        value_name = tree.set(row_id, 'value')  # get the clicked value
        
        field_label = ttk.Label(edit_frame, text="Key name is: " + key_name) # display key
        separator = ttk.Separator(edit_frame, orient='horizontal')
        edit_label = ttk.Label(edit_frame, text="Input text to change value for this data.") # display prompt
        entry_var = tk.StringVar()
        self.field = ttk.Entry(edit_frame, textvariable=entry_var) # display an edit box
            
        value_label = ttk.Label(edit_frame, text="The value to change is: " + entry_var.get()) # display value

        
            
            
        field_label.pack(expand=True)
        separator.pack(fill='x')
        value_label.pack(expand=True)
        edit_label.pack(expand = True)
        self.field.pack(expand=True)
            
       
        replaceall_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace value in ALL achievements",
            command=lambda:self.handle_submit(1, key_name)
        )
        replacethis_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace the value in this achievement",
            command=lambda:self.handle_submit(2, key_name, acmt_id)
        )
        replaceall_button.pack(expand=True, padx=10, pady=10)
        replacethis_button.pack(expand=True, padx=10, pady=10)

    
    def open_acmt(self, event, acmt_dict):
        
        tree = event.widget #get widget based on event
        acmt_id = tree.identify_row(event.y)  # get row

        acmt_frame = tk.Toplevel(self.root) # pop-up window 
        
        scrollbary = ttk.Scrollbar(acmt_frame, orient="vertical")
        scrollbarx = ttk.Scrollbar(acmt_frame, orient="horizontal")
        scrollbary.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        scrollbarx.pack(side=tk.BOTTOM, expand=False, fill=tk.X)

        
        table = ttk.Treeview(acmt_frame, columns=('key', 'value'), show = 'headings') # create table with tuple

        scrollbary.configure(command=table.yview)
        table.configure(yscrollcommand=scrollbary.set)
        scrollbarx.configure(command=table.xview)
        table.configure(xscrollcommand=scrollbarx.set)
        table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        for col in table["columns"]: # set column names as headers
            table.heading(col, text = col) 
        
        for index, key in enumerate(acmt_dict):
            table.insert('', index='end', iid=str(index), values=(key, acmt_dict[key]))

        table.bind("<Double-1>", lambda event: self.edit_value(event, acmt_id)) 

        


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

    def handle_submit(self, command, key, index = None):
        new_value = self.field.get()
        print(new_value)
        print(key)
        if (command == 1): 
            self.controller.data_handler(command, key, new_value)
        elif(command == 2):
            self.controller.data_handler(command, key, new_value, index)
            

    def select_file(self, command): #should these be in main?
        if (command == 1): #prompt to open file for importing
            file_path = fd.askopenfilename(title="Import achievement file")
        elif (command == 2): #prompt to pick directory to export file
            file_path = fd.asksaveasfilename(title="Export project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
        elif (command == 3): #prompt to save a project file
            file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=config.DEFAULT_FILE_FORMAT, filetypes=[("Text files", "*.txt")])
        
        self.controller.file_handler(file_path, command) #callback function, new path and variable to main
        print(file_path)

