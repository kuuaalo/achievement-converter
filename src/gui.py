import tkinter as tk
from tkinter import ttk, Menu
from tkinter import Tk, Text
from tkinter import filedialog as fd


class AchievementConverterGUI:
   
    def __init__(self, root, file_handler):
        
        self.root = root
        self.root.title("Achievement Converter") #window name
        self.file_handler = file_handler #give reference to function in main on init
        self.selected_path = None #empty variable for file path, should the config be used here?

       
        #window sizing
        window_width = 600 
        window_height = 300

        #window centering
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width/ 2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') 

        self.create_menu(self.root) #call function to create menu

        self.create_buttons(self.root)

        

    def create_menu(self, root):
        #menu creation (in progress)
        menubar = Menu(root)
        root.config(menu=menubar)

        file_menu = Menu(menubar)

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )


    def create_buttons(self, root):
        open_button = ttk.Button( #button to import file
            root,
            text="Import achievement file",
            command=lambda: self.select_file(1) #sends a parameter to select file
        )
        
        export_button = ttk.Button( #button to export file
            root,
            text="Export achievement file",
            command=lambda: self.select_file(2)
        )

        save_button = ttk.Button( #button to save project file
            root,
            text="Save achievement file",
            command=lambda: self.select_file(3)
        )

        exit_button = ttk.Button( #button to exit program
            root,
            text="Exit",
            command=lambda: root.quit() #quit program exits the mainloop
        )

        #button placement on grid
        open_button.grid(row=1, column=0, padx=5, pady=5)
        export_button.grid(row=2, column=0, padx=5, pady=5)
        save_button.grid(row=3, column=0, padx=5, pady=5)
        exit_button.grid(row=1, column=2, padx=5, pady=5)
    
    def create_table(self, root, acmt_list):
        frame = tk.Frame(root)
        frame.grid(row=0, column=0, sticky='nsew')
        column_list = tuple(acmt_list.keys()) #create a tuple of column names from dict keys
        table = ttk.Treeview(frame, columns = column_list, show = 'headings') #create table with tuple
     
        for col in table["columns"]: #iterate trough the columns
            table.heading(col, text = col) #set column names as headers
    
        table.grid(row=0, column=0, sticky='nsew')

        #in progress! scrollbar broken
        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
        scrollbar.grid(row=1, column=0, sticky='nsew')
        table.configure(xscroll=scrollbar.set)

        root.grid_rowconfigure(0, weight=1) #how do these work?
        root.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        

    
    def select_file(self, command): #should these be in main?
        if (command == 1): #prompt to open file for importing
            file_path = fd.askopenfilename()
        elif (command == 2): #prompt to pick directory to export file
            file_path = fd.askdirectory(title="Where do you want to export the file")
        elif (command == 3): #prompt to save a project file
            file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        self.file_handler(file_path, command) #callback function, new path and variable to main




 