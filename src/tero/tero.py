#import sys
#sys.path.insert(0,r"C:\Users\rauli\Documents\GitHub\achievement-converter\achievement-converter\src\read")
#from read import Read
#import read



class Tero:
    def __init__(self, resume=False, achievement_list=None):
      
        if achievement_list is not None:
            self.achievement_list = achievement_list  
        else:
            self.achievement_list = []
            

#Read starts here

    def add_achievement(self,achievement):  # Takes a dict and passes it where it is needed
        if isinstance(achievement,dict):
            self.achievement_list.append(achievement) #adds achievement to achievement_list
            return self.achievement_list #returns all given achievements as list
        else: return False
            
    def add_achievements(self,achievements):#takes a list of achievements  
        if isinstance(achievements,list): 
            self.achievement_list = achievements
            print("debugprint")
            return self.achievement_list #returns the list of achievements for later use
        else: return False


  
#write starts here
    key = "game_name"
    new_value = "perkele"
     
    def get_achievements(self):#write calls this, and this returns list of dicts
        return self.achievement_list
   
    def get_achievement_by_data(self,data):#should be able to fetch achievement by certain data
        False
    
    def add_data_to_all_achievements(self,key,new_value): #replace value in all achievements
        for achievement in self.achievement_list:
            if key in achievement: #checks if it exists
                achievement[key] = new_value
            else:
                achievement[key]= new_value #adds it if it doesnt exist
        return self.achievement_list    
  
    def update_achievement_data(self, achievement_id, key, new_value):
        try:
            achievement = self.achievement_list[int(achievement_id)] #!!rauli added int to convert index from string 
            if key in achievement:
                old_value = achievement[key]
                achievement[key] = new_value
            else:
                achievement[key] = new_value
            return True
        except IndexError:
            return False
        except Exception as e:
            print(f"Tuntematon virhe: {e}")
        return False



#tällaisia asioita tarvitaan:
#selected_id = 2,3,5,7,8  # GUI:n kautta saatu ID
#key_to_update = "acmt_xp"  # GUI:n kautta valittu key
#new_value = 100  # Uusi arvo käyttäjältä
















#tero.update_achievement_data(achievement_list, selected_id, key_to_update, new_value)






#functions still in progress start 
#millaisena main antaa valuet?



   #inner functions



#Kaksi funktiota, tee muutos yhteen, tee muutos kaikkiin





    #    def get_achievement(self, index=0):#write calls this, and this returns achievement in dict
#        if len(self.achievement_list) > index:
#            return {"Name":"achievement01","Status":"end"}
#        return None




# R = Read(test_file_location, self)
# R.run_fakef()
#filename tarvitsee korvata omalla
