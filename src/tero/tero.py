#import sys
#sys.path.append('C:\\Users\\rauli\\Documents\\GitHub\\achievement-converter\\achievement-converter\\src\\tero')
#import blueprint

class Tero:
    def __init__(self, resume=False, achievement_list=None):
        self.achievement_list = achievement_list if achievement_list is not None else []  
    

#Read starts here

    def add_achievement(self,achievement):  # Takes a dict and passes it where it is needed
        if isinstance(achievement,dict):
            self.achievement_list.append(achievement) #adds achievement to achievement_list
            return self.achievement_list #returns all given achievements as list
        else: return False
            
    def add_achievements(self,achievements):#takes a list of achievements  
        if isinstance(achievements,list): 
            self.achievement_list = achievements
            print("TERO debugprint")
            return self.achievement_list #returns the list of achievements for later use
        else: return False




    
    def fill_missing_values(self):
        # Define blueprint directly inside the method
        blueprint = {
            "version": None, 
            "game_name": None, 
            "acmt_num": None, 
            "name_id": None, 
            "name_en": None, 
            "name_fi": None, 
            "name_locked": None, 
            "name_token": None, 
            "desc_en": None, 
            "desc_fi": None, 
            "desc_token": None, 
            "hidden": None, 
            "icon": None, 
            "icon_locked": None, 
            "desc_locked": None, 
            "acmt_xp": None, 
            "acmt_stat_tres": None, 
            "ag_type": None, 
            "flavor_txt": None, 
            "gamerscore": None,
        }

        # Iterate over the achievement list to fill missing values based on blueprint
        for achievement in self.achievement_list:
            for key, default_value in blueprint.items():
                if key not in achievement:  # If the key is missing from the achievement
                    achievement[key] = default_value if default_value is not None else 0
                elif achievement[key] is None:  # If the value is None, set it to 0 (or default)
                    achievement[key] = 123  # You can change this to `default_value` instead of 123 if needed
        return self.achievement_list  # Return the updated achievement_list
  
#write starts here
    def get_achievements(self):#write calls this, and this returns list of dicts
        return self.achievement_list
   
   #RAULI TÄMÄN LISÄSIN
    def get_achievement_by_data(self, index):#should be able to fetch achievement by certain data
        acmt_dict = self.achievement_list[int(index)] 
        return acmt_dict
 
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
            
            return self.achievement_list #en osannu diilata näitten true/false kanssa
        except IndexError:
            return self.achievement_list
        except Exception as e:
            print(f"Tuntematon virhe: {e}")
        return self.achievement_list 
        
    


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
