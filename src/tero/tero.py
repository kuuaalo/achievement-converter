import time
class Tero:

    def __init__(self, resume=False, achievement_list=False):
      
        if resume:  #resumen käyttö
            pass
        else:
            pass

        if achievement_list:
            self.achievement_list = achievement_list
        else:
            self.achievement_list = []
        
    def response_moi():
        timestamp = time.time()
        print("Moi, olen Tero")
        print(timestamp)

#sisäiset funktiot
    def find_achievement():
        #osaa löytää ehdoilla tietyn achievementin
        False

#readin puoli
    def add_achievement(self,achievement):
        if isinstance(achievement,dict): return True
        else: return False
            
    def add_achievements(self,achievements):
        if isinstance(achievements,list): return True
        else: return False

    def add_data_to_achievement(self,achievement,data):
        True

#writen puoli
    def get_achievement(self):
        return {"Name":"achievement01","Status":"end"}
        
    def get_achievements(self):
        return [{"Name":"achievement02","Status":"end"}]

    def get_achievement_by_data(self,data):
        False
    
    def get_next_achievement(self):
        
        return {"Name":"achievement03","Status":"end"}
