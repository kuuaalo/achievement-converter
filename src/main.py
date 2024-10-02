import configparser

from tkinter import filedialog as fd

from gui import AchievementConverterGUI as gui #import gui

from tero.tero import Tero as tero #import all functions from tero, these don't exist yet


#from read.read import * #import all functions from read
#from write.write import * #import all functions from write

acmt_platform = None #global function with no value
acmt_file_path = None 



class AchievementConverter:

    def select_file():
        global acmt_file_path
        acmt_file_path = fd.askopenfilename()
        print('The file path is: ' + acmt_file_path)
    
    #def acmt_import():
        #tero_function(acmt_platform) #send platform to tero
        #read_file(acmt_file_path) #send file to read

    #tero calls this
    #def acmt_write(acmt_data): #takes list/array whatever as parameter
       # write_function(acmt_data) #Sends data to write

        
def main():
    tero.response_moi() #test function call
    gui.run_gui() #call gui
    


if __name__ == "__main__":
    main()



