import tkinter as tk
from tkinter import ttk, Menu
from tkinter import Tk, Text
from tkinter import filedialog as fd


class AchievementConverterGUI:
   
    def __init__(self, root):

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
            #command=select_file #broken
        )

        exit_button = ttk.Button(
            root,
            text="Exit",
            command=lambda: root.quit() #quit program
        )

        open_button.grid(row=3, column=0, padx=5, pady=5)
        exit_button.grid(row=4, column=1, padx=5, pady=5)
    

    
    
    def run_gui():
        root = tk.Tk() #tkinter
        app = AchievementConverterGUI(root)
        root.mainloop() #keep the window displaying
        pass