import tkinter as tk
from tkinter import ttk, Menu
from tkinter import Tk, Text
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class AchievementConverterGUI:

    def __init__(self, root, file_handler):
        
        self.root = root
        self.root.title("Achievement Converter") #window name
        self.file_handler = file_handler #give reference to function in main on init
        self.selected_path = None #empty variable for file path, should the config be used here?
        


        self.root.geometry("1200x600")
        self.root.title("Achievement Converter")

        self.create_menu() #call function to create menu

        #self.create_table()

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
    
    def create_table(self, acmt_list):
        self.acmt_list = acmt_list
        frame = tk.Frame(self.root, width=400, height=300)
        scrollbary = ttk.Scrollbar(frame, orient="vertical")
        scrollbarx = ttk.Scrollbar(frame, orient="horizontal")
        scrollbary.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        scrollbarx.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
        
        test_dict = self.acmt_list[0]
        column_list = tuple(test_dict.keys()) #create a tuple of column names from dict keys
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
        self.table.bind("<Double-1>", lambda event: self.edit_value(event))
        self.table.tag_configure('null_value', background='red') #tag to display red color for null values

    def populate_table(self):
        for item in self.acmt_list:
            row_values = list(item.values()) 
            if (None in row_values): #add tag if acmt has null value
                self.table.insert('', index='end', values=list(item.values()), tags=('null_value',))
            else:
                self.table.insert('', index='end', values=list(item.values()))
        
    def edit_value(self, event):
        #selected_item = self.table.selection() #select achievement based on row
        edit_frame = tk.Frame(self.root)
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        row_id = tree.identify_row(event.y)  # Get row
        column_id = tree.identify_column(event.x)  # Get column
        if row_id and column_id: # CONTINUE HERE. GET COLUMN NAME AND CELL VALUE
            print(row_id)
            print(column_id)
            title = tree.set(row_id)  # Get cell value
            value = tree.set(row_id, column_id)  # Get cell value
            #print(value)
            field_label = ttk.Label(edit_frame, text=title)
            value_label = ttk.Label(edit_frame, text=value)
            field_label.pack(side=tk.LEFT, expand=False)
            value_label.pack(side = tk.LEFT,expand=False)
            
        

        replaceall_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace value in all achievements",
            #command=self.file_handler(key, var, 4)
            command=lambda:self.tero.add_data_to_achievement(field_vars) #TERO KUTSU TÄHÄN
        )
        replacethis_button = ttk.Button( #button to import file
            edit_frame,
            text="Replace value in this achievement",
            command=lambda:self.tero.add_data_to_all_achievements(field_vars) #TOINEN TERO KUTSU TÄHÄN
        )
        replaceall_button.pack(side = tk.LEFT, expand=False, padx=30, pady=30)

        #field_vars = {} #dict to store new values
        #test_dict2 = self.acmt_list[0] #KORJAA. ei käytä oikeita valueita!!
        
        #for index, key in enumerate(test_dict2):
            #field_frame = tk.Frame(edit_frame)
            #field_string = tk.StringVar()
            #field_vars[key] = field_string
            #value = test_dict2[key]

            #field_label = ttk.Label(field_frame, text=key)
            #value_label = ttk.Label(field_frame, text=value)
            #field = ttk.Entry(field_frame)
            
            #field_label.pack(side=tk.LEFT, expand=False)
            #value_label.pack(side = tk.LEFT,expand=False)
            #field.pack(side = tk.LEFT,expand=False)
            #field_frame.pack(side = tk.TOP, expand=False, padx=10, pady=10)
    
        edit_frame.pack(side = tk.LEFT, expand=False, padx=30, pady=30)
        # print(field_vars)


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

    
    
  
        


    def select_file(self, command): #should these be in main?
        if (command == 1): #prompt to open file for importing
            file_path = fd.askopenfilename()
        elif (command == 2): #prompt to pick directory to export file
            file_path = fd.asksaveasfilename(title="Save project file as", filetypes=[("Text files", "*.txt"),("Epic", "*.csv"),("Steam rawdata", "*.txt"),("MS Store", "*.xml"), ("All Files", "*.*")])
        elif (command == 3): #prompt to save a project file
            file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        self.file_handler(file_path, command) #callback function, new path and variable to main
        print(file_path)

