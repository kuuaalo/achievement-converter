import json
import config
from gui import showerror

class Process:

    def __init__(self, resume=False, achievement_list=None):
        if achievement_list is False or achievement_list is None:
            self.achievement_list = []
            self.localizations_list = []
            self.localizations_data = {}
        else:
            self.achievement_list = achievement_list

    # Takes a dict and adds achievement to achievement_list, then passes list where needed
    def add_achievement(self, achievement):
        if isinstance(achievement, dict):
            self.achievement_list.append(achievement)
            return self.achievement_list
        else:
            return False

    # Takes a list of achievements and then it can be passed around
    def add_achievements(self, achievements):
        if isinstance(achievements, list):
            self.achievement_list = achievements
            return self.achievement_list
        else:
            return False


    def add_localizations(self, ID, LOCALE, list_value_pairs):
        if ID not in self.localizations_data:
            self.localizations_data[ID] = {}
        self.localizations_data[ID][LOCALE] = list_value_pairs
        print("KULLIPERSE" ,self.localizations_data)
        return self.localizations_data

    def add_vdf_localizations(self,localization_data):
        localizations_data = localization_data
        print(localizations_data)
        print("KULLIPERSE" ,self.localizations_data)
        return self.localizations_data

    def get_localizations(self):
        return self.localizations_data




    # Define blueprint for all values
    def fill_missing_values(self):
        blueprint = config.ACMT_DICT #get blueprint from config-file
        for achievement in self.achievement_list:
            for key, default_value in blueprint.items():
                if key not in achievement:
                    achievement[key] = default_value # if default_value is not None else 0
                #elif achievement[key] is None:
                    #achievement[key] = 0
        return self.achievement_list

    # Merge achievements and localizations
    def merge(self,achievement_list, localizations_data):
    # Blueprint for all fields we expect
        blueprint = config.ACMT_DICT 
        
        merged_achievements = []

        for achievement in self.achievement_list:
            name_id = achievement.get("name_id")
            
            # Create a new dictionary with default values based on the blueprint
            merged_achievement = blueprint.copy()  # Using blueprint to copy default values

            # Merge achievement-specific data (e.g., 'name_id', 'acmt_num', 'icon', etc.)
            for key in achievement:
                if key in merged_achievement:
                    merged_achievement[key] = achievement[key]

            # If localization data exists for this achievement, merge it
            if name_id in self.localizations_data:
                localization_data = self.localizations_data[name_id]
                for locale, local_data in localization_data.items():
                    if locale not in merged_achievement:
                        merged_achievement[locale] = {}
                        if isinstance(local_data, dict):
                            print("ifinstance toimii")
                            print(f"local_data is a dictionary: {local_data}")
    

                            # Merge localized values (e.g., name_en, name_fi, etc.)
                            merged_achievement[locale]["name"] = local_data.get("name", "")
                            merged_achievement[locale]["lockedTitle"] = local_data.get("lockedTitle", "")
                            merged_achievement[locale]["lockedDescription"] = local_data.get("lockedDesc", "")
                            merged_achievement[locale]["unlockedTitle"] = local_data.get("unlocked", "")
                            merged_achievement[locale]["unlockedDescription"] = local_data.get("unlockedDesc", "")
                        else:
                            # Hoida tilanne, jossa local_data ei ole sanakirja
                            print(f"local_data is not a dictionary: {local_data}")

            # Add the merged achievement to the final list
            
            merged_achievements.append(merged_achievement)
  
        return merged_achievements

    def get_achievements(self,achievement_list,localizations_data):
        # Merges the achievements and localizations if not done already
        return self.merge()
    
    # Function to fetch all data
    def get_all_data(self):
        merged_data = self.merge(self.achievement_list, self.localizations_data)
    # Check if the merge has happened and list has values
        if not merged_data: 
            self.gui.show_error("Error", "No data in merger")
            return []
        print("testiMERGE123")
        print(merged_data)  
        return merged_data

    # Returns a dictionary of achievement data by index
    def get_achievement_by_data(self, index = 0):
        while True:
            try:
                print("get achievement by data")
                print(self.achievement_list)
                acmt_dict = self.achievement_list[int(index)]
                return acmt_dict

            except IndexError:
                print("No file data")
                return False



    # Returns a filtered dictionary of values in achievement
    def get_achievement_keys_from_dict(self, key_list, index):
        acmt_dict = self.achievement_list[int(index)]
        filter_dict = {}
        for key in acmt_dict:
            if key in key_list:
                filter_dict[key] = acmt_dict[key]
        return filter_dict

    # Returns a filtered list of all achievements
    def get_filtered_list(self, key_list):
        filter_list = []
        for index, achievement in enumerate(self.achievement_list):
            filtered_dict = self.get_achievement_keys_from_dict(key_list, index)
            filter_list.append(filtered_dict)

        return filter_list

    # Function to return locale codes for main
    def get_locales(self):
        locales = set()
        for name_id, localization in self.localizations_data.items():
            locales.update(localization.keys())
        print(locales)
        return "{" + ", ".join(locales) + "}"
    
    # Function to return list of locales
    def get_locale_list(self):
        locales = []
        localizations = self.localizations_data['AchievementID1']
        for item in localizations:
            print(item)

            locales.append(item)
        return locales


    # Replace value in all achievements. Checks if it exists, adds if not
    def add_data_to_all_achievements(self, key, new_value):
        for achievement in self.achievement_list:
            if key in achievement:
                achievement[key] = new_value
            else:
                achievement[key] = new_value
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
    def save_data(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.achievement_list, f)
        print(f"Data saved to {file_path}")
        return True

    # To continue existing project, load JSON data from selected path
    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)
        print(f"Data loaded from {file_path}")
        self.achievement_list = loaded_data
        return loaded_data