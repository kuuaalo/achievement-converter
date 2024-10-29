import tkinter as tk
from tkinter import ttk, Menu
from tkinter import Tk, Text
from tkinter import filedialog as fd


class AchievementConverterGUI:
   
    def __init__(self, root, input):
        
        self.root = root
        
        self.root.title("Achievement Converter")

        self.input = input

        self.selected_path = None #empty variable for file path, should the config be used here?

        #window centering
        window_width = 600 
        window_height = 300

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        center_x = int(screen_width/ 2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') 

        self.create_menu(root)

        self.create_buttons(root)

    def create_menu(self, root):
        #menu creation
        menubar = Menu(root)
        root.config(menu=menubar)

        file_menu = Menu(menubar)

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )


    def create_buttons(self, root):
        open_button = ttk.Button(
            root,
            text="Import achievement file",
            command=lambda: self.select_file(1)
        )
        
        export_button = ttk.Button(
            root,
            text="Export achievement file",
            command=lambda: self.select_file(2)
        )

        save_button = ttk.Button(
            root,
            text="Save achievement file",
            command=lambda: self.select_file(3)
        )

        exit_button = ttk.Button(
            root,
            text="Exit",
            command=lambda: root.quit() #quit program exits the mainloop
        )

        open_button.grid(row=1, column=0, padx=5, pady=5)
        export_button.grid(row=2, column=0, padx=5, pady=5)
        save_button.grid(row=3, column=0, padx=5, pady=5)
        exit_button.grid(row=4, column=1, padx=5, pady=5)
    
    def select_file(self, command):
        if (command == 1): #prompt to open file for importing
            file_path = fd.askopenfilename()
        elif (command == 2): #prompt to pick directory to export file
            file_path = fd.askdirectory(title="Where do you want to export the file")
        elif (command == 3): #prompt to save a project file
            file_path = fd.asksaveasfilename(title="Save project file as", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        if file_path: #if user changed the path
            self.input(file_path, command) #callback function, new path to main




 