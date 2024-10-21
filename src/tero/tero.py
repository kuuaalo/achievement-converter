import time
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
    def find_achievement(): #will find achievement with given values
        
        False

#Read starts here
    def add_achievement(self,achievement):  # no need to iterate, just takes the dict and passes it where it is needed
        if isinstance(achievement,dict): 
            self.achievement_list.append(achievement)
            return self.achievement_list
        else: return False
            
    def add_achievements(self,achievements):# no need to iterate, just takes the list of dicts and passes it where it is needed
        if isinstance(achievements,list): 
            self.achievement_list = achievements
            return self.achievement_list
        else: return False

    def add_data_to_achievement(self,achievement,data): #might be able to manipulate data in achievement
        True

#write starts here
    def get_achievement(self):#write calls this, and this returns achievement in dict
        return {"Name":"achievement01","Status":"end"}
        
    def get_achievements(self):#write calls this, and this returns list of dicts
        return self.achievement_list
    #[{"Name":"achievement02","Status":"end"}]

    def get_achievement_by_data(self,data):#should be able to fetch achievement by certain data
        False
    
    def get_next_achievement(self):#Not sure why needed, get_achievement can just iterate thru?
        return {"Name":"achievement03","Status":"end"}

   
