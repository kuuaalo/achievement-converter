import json





class Tero:

    def __init__(self, resume=False, achievement_list=None):
        if achievement_list is False or achievement_list is None:
            self.achievement_list = []
            print(self.achievement_list)
        else: 
            self.achievement_list = achievement_list
            


    def add_achievement(self,achievement):                      # Takes a dict and passes it where it is needed
        if isinstance(achievement,dict):
            self.achievement_list.append(achievement)           # Adds achievement to achievement_list
            return self.achievement_list                        # Returns all given achievements as list
        else: return False
            

    def add_achievements(self,achievements):                    # Takes a list of achievements  
        if isinstance(achievements,list): 
            self.achievement_list = achievements
            return self.achievement_list                        # Returns the list of achievements for later use
        else: return False

    
    def fill_missing_values(self):
       
        blueprint = {                                           # Define blueprint for all values, so that write fill have something to print
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

        
        for achievement in self.achievement_list:               # Iterate over the achievement list to fill missing values based on blueprint
            for key, default_value in blueprint.items():
                if key not in achievement:                      # If the key is missing from the achievement
                    achievement[key] = default_value if default_value is not None else 0
                elif achievement[key] is None:                   # If the value is None, set it to 0 (or default)
                    achievement[key] = 0                         
        return self.achievement_list                             # Return the updated achievement_list
  

    def get_achievements(self):                                  # write calls this, and this returns list of dicts
        return self.achievement_list
   
   
    def get_achievement_by_data(self, index):
        print("testi >:(")  # Debug-tulostus                    #should be able to fetch achievement by certain data
        acmt_dict = self.achievement_list[int(index)] 
        return acmt_dict



    def add_data_to_all_achievements(self,key,new_value):        #replace value in all achievements
        for achievement in self.achievement_list: 
            if key in achievement:                               #checks if it exists
                achievement[key] = new_value
            else:
                achievement[key]= new_value                      #adds it if it doesnt exist
        return self.achievement_list    
  
    def update_achievement_data(self, achievement_id, key, new_value):
#        try:
            achievement = self.achievement_list[int(achievement_id)] #!!rauli added int to convert index from string 
            if key in achievement:
                old_value = achievement[key]
                achievement[key] = new_value
            else:
                achievement[key] = new_value
            
            return self.achievement_list                           #en osannu diilata näitten true/false kanssa
#        except IndexError:
#            return self.achievement_list
#        except Exception as e:
#            print(f"Tuntematon virhe: {e}")
#        return self.achievement_list 
        
    

    def save_data(self): #Writes data to disk as JSON if necessary, and next one loads it
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return True

    def load_data(self):
        loaded_data = json.load(f)
        return True