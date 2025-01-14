"""
Process module provides functionality to modify your data, it organizes achievements to maintain easy usability
with different formats, and provides information and data to other modules. If you need to add more functionality
to the program, this is the best place to do it, as all information passes through this module, and this module communicates with main
a lot. Here data is organized according to blueprints, and then used wherever it is needed.
"""
import json

class Process:

    def __init__(self, resume=False, achievement_list=None):
        if achievement_list is False or achievement_list is None:
            self.achievement_list = []
            print(self.achievement_list)
        else:
            self.achievement_list = achievement_list


    # Takes a dict and adds achievement to achievement_list, then passes list where needed
    def add_achievement(self,achievement):
        if isinstance(achievement,dict):
            self.achievement_list.append(achievement)
            return self.achievement_list
        else: return False

    # Takes a list of achievements and then it can be passed around
    def add_achievements(self,achievements):
        if isinstance(achievements,list):
            self.achievement_list = achievements
            return self.achievement_list
        else: return False

    # Define blueprint for all values, so that write will have something to print
    def fill_missing_values(self):
        blueprint = {
            "version": None,
            "game_name": None,
            "game_id": None,
            "acmt_num": None,
            "name_id": None,
            "name_en": None,
            "name_fi": None,
            "name_locked": None,
            "name_token": None,
            "desc_id":None,
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
            "base_acmt":None,
        }
        # Iterate over the achievement list to fill missing values based on blueprint.
        # This sets None values to 0 to ensure printing of all nests and value pairs
        for achievement in self.achievement_list:
            for key, default_value in blueprint.items():
                if key not in achievement:
                    achievement[key] = default_value if default_value is not None else 0
                elif achievement[key] is None:
                    achievement[key] = 0
        return self.achievement_list


    # write calls this, and this returns list of dicts
    def get_achievements(self):
        return self.achievement_list


   # Fetch achievement by certain data
    def get_achievement_by_data(self, index):
        acmt_dict = self.achievement_list[int(index)]
        return acmt_dict


    # Returns a dictionary of the given keys in achievement
    def get_achievement_keys_from_dict(self, key_list, index):
        acmt_dict = self.achievement_list[int(index)]
        new_dict = {}
        for key in acmt_dict:
            if key in key_list:
                new_dict[key] = acmt_dict[key]
        return new_dict


    # Replace value in all achievements. Checks if it exists, adds if not
    def add_data_to_all_achievements(self,key,new_value):
        for achievement in self.achievement_list:
            if key in achievement:
                achievement[key] = new_value
            else:
                achievement[key]= new_value
        return self.achievement_list

    # Replace one value in achievement
    def update_achievement_data(self, achievement_id, key, new_value):
            achievement = self.achievement_list[int(achievement_id)]
            if key in achievement:
                old_value = achievement[key]
                achievement[key] = new_value
            else:
                achievement[key] = new_value

            return self.achievement_list


    # Saves data to selected file path as JSON
    def save_data(self,file_path):
        with open(file_path, 'w') as f:
            json.dump(self.achievement_list, f)
        print(f"Data saved to {file_path}")
        return True


    # To continue existing project, load JSON data from selected path
    def load_data(self,file_path):
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)
        print(f"Data saved to {file_path}")
        self.achievement_list = loaded_data ##Added this for now, maybe use resume in the future
        return loaded_data