import sys
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Text
from tkinter import filedialog as fd
from tkinter import Menu

platform = None

#Next time, add platform selection. Maybe as a submenu?

class AchievementConverter:

    def __init__(self, root):
        self.root = root
        self.root.title('Achievement Converter')
    
    def select_file():
        filename = fd.askopenfilename()
        print('The file path is: ' + filename)


        
def main():
    root = tk.Tk() 
    #window centering
    window_width = 600 
    window_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width/ 2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') 

    #menu creation
    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar)

    menubar.add_cascade(
        label="File",
        menu=file_menu
    )

    #Buttons

    open_button = ttk.Button(
        root,
        text="Import achievement file",
        command=AchievementConverter.select_file
        )

    exit_button = ttk.Button(
        root,
        text="Exit",
        command=lambda: root.quit()
    )

    open_button.grid(row=3, column=0, padx=5, pady=5)
    exit_button.grid(row=4, column=1, padx=5, pady=5)
    
    root.mainloop() #keep the window displaying 


if __name__ == "__main__":
    main()



