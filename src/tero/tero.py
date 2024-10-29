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
        
    def response_moi(self):
        timestamp = time.time()
        print("Moi, olen Tero")
        print(timestamp)

#inner functions
#################################
#    def find_achievement(self,achievement_list): #will find achievement with given values
#        key = input("Enter the key for the achievement you want to find:") #takes input for what you want to find
#        if key in achievement_list:
#            value = achievement_list[key]
#            print(f"Achievement found: {key} - {value}")
#            return {key:value} #returns the value pair if it exists
#        else:
#            print("Achievement not found.")
#            return None
#
#    def add_data_to_achievement(self,achievement_list,key): #Will able to manipulate data in achievement
#        new_value = input("Enter new value for the achievement:") #takes the new value as input
#        if key in achievement_list: #checks if it exists
#            achievement_list[key] = new_value
#            print(f"Achievement found: {key} - {new_value}")
#        else:
#            print(f"No achievement with key '{key}' found.")
#            return None
###################################
        


#Read starts here
###################################
    def add_achievement(self,achievement):  # no need to iterate, just takes the dict and passes it where it is needed
        if isinstance(achievement,dict): 
            self.achievement_list.append(achievement) #adds achievement to achievement_list
            return self.achievement_list #returns all given achievements as list
        else: return False
            
    def add_achievements(self,achievements):#takes a list of achievements and passes them on as a list 
        if isinstance(achievements,list): #
            self.achievement_list = achievements
            return self.achievement_list
        else: return False
####################################
  

#write starts here
#    def get_achievement(self, index=0):#write calls this, and this returns achievement in dict
#        if len(self.achievement_list) > index:
#            return {"Name":"achievement01","Status":"end"}
#        return None
    
    def get_achievements(self):#write calls this, and this returns list of dicts
        return self.achievement_list
   

    def get_achievement_by_data(self,data):#should be able to fetch achievement by certain data
        False
    
   # def get_next_achievement(self):#Not sure why needed, get_achievement can just iterate thru?
   #     return {"Name":"achievement03","Status":"end"}
    
   # def run(self,achivement):

   
