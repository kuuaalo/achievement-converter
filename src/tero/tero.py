import time
import read



class Tero:
    def __init__(self, resume=False, achievement_list=False):
      
        if resume:  #opening existing projects
            pass
        else:
            pass

        if achievement_list:
            self.achievement_list = achievement_list
        else:
            self.achievement_list = []
        

#Read starts here

    def add_achievement(self,achievement):  # Takes a dict and passes it where it is needed
        if isinstance(achievement,dict):
            #lisää _0, _1 id jotta achievementin voi löytää
            # mistä tero ymmärtää milloin achievement loppuu 
            self.achievement_list.append(achievement) #adds achievement to achievement_list
            return self.achievement_list #returns all given achievements as list
        else: return False
            
    def add_achievements(self,achievements):#takes a list of achievements  
        if isinstance(achievements,list): 
            self.achievement_list = achievements
            return self.achievement_list #returns the list of achievements for later use
        else: return False

  

#write starts here
     
    def get_achievements(self):#write calls this, and this returns list of dicts
        return self.achievement_list
   
    def get_achievement_by_data(self,data):#should be able to fetch achievement by certain data
        False
    






#functions still in progress start here




   #inner functions

#    def add_data_to_achievement(self,achievement_list,key,new_value): #replace values in spesific achievements with spesific data
#        achievementit indexin mukaan
#        if key in achievement_list:
#            value = achievement_list[key]
#            print(f"Achievement found: {key} - {value}")
#            return {key:value} #returns the value pair if it exists
#        else:
#            print("Achievement not found.")
#            return None
#
    def add_data_to_all_achievements(self,achievement_list,key, new_value): #replace value in all achievements
       for achievement in achievement_list:
         if key in achievement: #checks if it exists
            achievement[key] = new_value
            print(f"Achievement updated: {key} - {new_value}")
        else:
            print(f"Achievement for {key} added with value: {new_value}.")
            return None

    #    def get_achievement(self, index=0):#write calls this, and this returns achievement in dict
#        if len(self.achievement_list) > index:
#            return {"Name":"achievement01","Status":"end"}
#        return None


