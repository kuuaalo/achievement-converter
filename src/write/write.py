"""
This module provides functionality to write achievement data into different file formats.
Depending on the specified file format, it writes the data to the appropriate 
file format in a structured and formatted way.
"""
from collections import defaultdict
import xml.dom.minidom as minidom
import csv
import vdf
import config
from gui import showerror
from config import LANGUAGES 

class Write:
    def __init__(self, file_name, file_format, process, gui) :
        
        if file_name:
            self.file_name = file_name
        else:
            print("Wrong file name")
            return

        # Set the file format to lowercase
        if file_format:
            self.file_format = file_format.lower()  
        # Print error if file format is invalid
        else:
            print("Wrong format from write")  
            return
        self.process=process
        self.gui = gui
        self.languages = LANGUAGES

    def run(self):
        # Execute the writing process based on the specified file format.
        
        #achievements is merged data of all achievements and their mathces in locales
        achievements = self.process.get_all_data() 
        oikea_lista = self.process.fill_missing_values()

        # Write to XML if format is XML
        if self.file_format == ".xml":
            self.write_to_xml(achievements)
            self.write_localizations_to_xml(achievements) 
        # Write to CSV if format is CSV
        elif self.file_format == ".csv":
            self.write_to_csv(achievements)
            self.write_locales_to_csv(achievements)
            self.write_stats_to_csv(achievements)
        # Write to VDF if format is VDF
        elif self.file_format == ".vdf":
            self.write_to_vdf(achievements)
            self.write_locales_to_vdf(achievements)
        # Print error for unsupported formats
        else:
            self.gui.show_error("Error", f"Unsupported format: {self.file_format}")
            




    def write_to_xml(self, achievements):
        # Create the XML document
        doc = minidom.Document()
        root = doc.createElement('Achievements2017')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/achievements2017/1")
        doc.appendChild(root)

        for i, achievement in enumerate(achievements, start=1):
            if not achievements:
                self.gui.show_error("Error", "No data provided for XML file")
                return


            # Debug: Print the achievement data to check if descriptions exist
            #print(f"Achievement {i} data: {achievement}")

            achievement_element = doc.createElement('Achievement')

            # Map XML tags to achievement data keys
            xml_tags_map = {
                "AchievementNameId": "name_id",
                "BaseAchievement": "base_acmt",
                "DisplayOrder": "acmt_num",
                "LockedDescriptionId": "desc_locked",
                "UnlockedDescriptionId": "desc_token",
                "IsHidden": "hidden",
                "AchievementId": str(i),  # Achievement ID based on index
                "IconImageId": "icon"
            }

            # Iterate over the xml_tags_map to create XML elements
            for xml_tag, key in xml_tags_map.items():
                element = doc.createElement(xml_tag)

                # Special handling for certain tags
                if xml_tag == "UnlockedDescriptionId":
                    # Create Rewards block before UnlockedDescriptionId
                    rewards_element = doc.createElement("Rewards")
                    gamerscore = doc.createElement("Gamerscore")
                    gamerscore.appendChild(doc.createTextNode(str(achievement.get("acmt_xp", "0"))))
                    rewards_element.appendChild(gamerscore)
                    achievement_element.appendChild(rewards_element)

                # Handle BaseAchievement and IsHidden as booleans
                if xml_tag == "BaseAchievement":
                    element.appendChild(doc.createTextNode(str(achievement.get(key, "true")).lower()))
                elif xml_tag == "IsHidden":
                    element.appendChild(doc.createTextNode("true" if achievement.get(key, False) else "false"))
                elif xml_tag == "AchievementId":
                    element.appendChild(doc.createTextNode(str(i))) 
                else:
                    element.appendChild(doc.createTextNode(str(achievement.get(key, ""))))  

                # Append element to Achievement
                achievement_element.appendChild(element)

            # Now add unlockedDescription and lockedDescription from specific languages
            unlocked_desc = achievement.get('en-US', {}).get('unlockedDescription', '')
            locked_desc = achievement.get('en-US', {}).get('lockedDescription', '')

            # Debug: Check if descriptions exist
            print(f"Unlocked description: {unlocked_desc}, Locked description: {locked_desc}")

            if unlocked_desc:  # Add UnlockedDescription if exists
                unlocked_description_element = doc.createElement('UnlockedDescription')
                unlocked_description_element.appendChild(doc.createTextNode(unlocked_desc))
                achievement_element.appendChild(unlocked_description_element)

            if locked_desc:  # Add LockedDescription if exists
                locked_description_element = doc.createElement('LockedDescription')
                locked_description_element.appendChild(doc.createTextNode(locked_desc))
                achievement_element.appendChild(locked_description_element)

            # Append the achievement to the root
            root.appendChild(achievement_element)

        # Write the XML document to a file
        xml_str = doc.toprettyxml(indent="  ")
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(xml_str)

        print(f"XML successfully written to {self.file_name}.")



 

    
    def write_localizations_to_xml(self, achievements):
        # Update the file name by replacing .xml with _localized.xml
        output_filename = self.file_name.replace(".xml", "_localized.xml")

        # Create the XML document
        doc = minidom.Document()
        root = doc.createElement('Localization')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/localization/1")
        doc.appendChild(root)

        # Add DevDisplayLocale element
        dev_locale = doc.createElement('DevDisplayLocale')
        dev_locale.setAttribute('locale', 'en-US')  # This is hardcoded for "en-US" as per the example
        root.appendChild(dev_locale)

        # Lists to store the different types of LocalizedString elements
        achievement_strings = []
        locked_description_strings = []
        unlocked_description_strings = []

        # Iterate over the achievements to create LocalizedString elements
        for achievement in achievements:
            achievement_id = achievement.get("name_id", "")  # Unique identifier for the achievement

            # Create LocalizedString element for achievement name 
            localized_name = doc.createElement('LocalizedString')
            localized_name.setAttribute('id', achievement_id)

            # Add name translations for each locale (skip 'default')
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "name" in lang_data:
                    if locale != "default":  # Skip the 'default' locale
                        value_elem = doc.createElement('Value')
                        value_elem.setAttribute('locale', locale)
                        value_elem.appendChild(doc.createTextNode(lang_data["name"]))
                        localized_name.appendChild(value_elem)

            achievement_strings.append(localized_name)  # Store the achievement name entry

            # Handle LockedDescription and UnlockedDescription (these should be separate entries)
            for desc_type in ["lockedDescription", "unlockedDescription"]:
                # Generate unique ID for the description (LockedDescriptionId1, UnlockedDescriptionId1, etc.)
                desc_id = f"{desc_type.capitalize()}{achievement_id[11:]}"  # Extracting the number part from the name_id
                
                localized_desc = doc.createElement('LocalizedString')
                localized_desc.setAttribute('id', desc_id)

                # Add description translations, skipping 'default'
                for locale, lang_data in achievement.items():
                    if isinstance(lang_data, dict) and desc_type in lang_data:
                        if locale != "default":  # Skip the 'default' locale
                            value_elem = doc.createElement('Value')
                            value_elem.setAttribute('locale', locale)
                            value_elem.appendChild(doc.createTextNode(lang_data[desc_type]))
                            localized_desc.appendChild(value_elem)

                # Only add descriptions if they contain at least one translation
                if localized_desc.childNodes:
                    if desc_type == "lockedDescription":
                        locked_description_strings.append(localized_desc)  # Store locked description entry
                    else:
                        unlocked_description_strings.append(localized_desc)  # Store unlocked description entry

        # Now append the entries in the desired order: Achievements -> Locked Descriptions -> Unlocked Descriptions
        for entry in achievement_strings + locked_description_strings + unlocked_description_strings:
            root.appendChild(entry)

        # Write the XML document to a file with the updated filename
        xml_str = doc.toprettyxml(indent="  ")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(xml_str)

        print(f"Localization XML successfully written to {output_filename}.")








    def write_to_csv(self, achievements):
        if not achievements:
            self.gui.show_error("Error", "No data provided for CSV file")
            return

        # CSV:n sarakkeet
        csv_field_map = {
            "name": "name",
            "hidden": "hidden",
            "statThresholds": "acmt_stat_tres",
            "user_epic_achievements_xp": "acmt_xp",
        }

        fieldnames = list(csv_field_map.keys())

        # Kirjoitetaan CSV-tiedosto
        with open(self.file_name, "w", newline='', encoding="utf-8") as f:
            print(self.process)  # Debug message
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for achievement in achievements:
                row = {}

                
                achievement_name = achievement.get("en-US", {}).get("name")

                for csv_key, data_key in csv_field_map.items():
                    if csv_key == "name":
                        row[csv_key] = achievement_name  
                    else:
                        row[csv_key] = achievement.get(data_key, "") 

                writer.writerow(row)

        print(f"Data written to {self.file_name} in CSV format.")

    

    def write_locales_to_csv(self, achievements):
        """
        Writes localization data to a CSV file.
        This function extracts localization information from the given achievement data
        and saves it into a separate CSV file with appropriate field names.
        """    
        locales_file_name = self.file_name.replace(".csv", "_locales.csv")
        print("Data to be written to CSV:", achievements)

        # Define column names for the CSV file
        fieldnames = [
            "achievement_id", 
            "locale",          
            "lockedTitle",     
            "lockedDescription",  
            "unlockedTitle",   
            "unlockedDescription", 
            "flavorText"
        ]

        # Open the localization CSV file for writing
        with open(locales_file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # Initialize CSV writer
            writer.writeheader()  # Write the column headers

            # Loop through each achievement and extract localization details
            for achievement in achievements:
            

                # Loop through each lang code in the achievement 
                for lang_code, locale_data in achievement.items():
                    # Check if the key is a valid language code (e.g., 'en-US', 'fi', etc.)
                    if isinstance(locale_data, dict):
                        row = {
                            "achievement_id": achievement.get("name_id", ""),  # Achievement ID
                            "locale": lang_code,  # Locale (using the language code from the keys)
                            "lockedTitle": locale_data.get("lockedTitle", ""), 
                            "lockedDescription": locale_data.get("lockedDescription", ""), 
                            "unlockedTitle": locale_data.get("unlockedTitle", ""), 
                            "unlockedDescription": locale_data.get("unlockedDescription", ""),
                            "flavorText": locale_data.get("flavor_txt", "")  # Using "flavor_txt" key
                        }
                        # Write the row to the CSV
                        writer.writerow(row)

        # Print confirmation message
        print(f"Localization data successfully written to {locales_file_name} in CSV format.")


    def write_stats_to_csv(self, achievements):
        """
        Writes stats data to a CSV file.
        """
        stats_file_name = self.file_name.replace(".csv", "_stats.csv")

        # Define column names for the CSV file
        fieldnames = [
            "name",
            "aggregationType"
        ]

        # Open the stats CSV file for writing
        with open(stats_file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for achievement in achievements:
                row = {
                    "name": achievement.get("name", ""),
                    "aggregationType": achievement.get("aggregationType", "")
                }
                writer.writerow(row)

        print(f"Stats data written to {stats_file_name} in CSV format.")








       
    def write_to_vdf(self, achievements):
    # Tarkista, että achievements on olemassa ja ei ole tyhjä
        if not achievements:
            self.gui.show_error("Error", "No data provided for VDF file")
            return

        game_id= achievements[0].get("game_id", "None")
        result = f'"{game_id}"\n{{\n'
        result += '\t"stats"\n\t{\n'
        result += '\t\t"1"\n\t\t{\n'
        result += '\t\t\t"bits"\n\t\t\t{\n'

        for i, achievement in enumerate(achievements, start=1):
            result += f'\t\t\t\t"{i}"\n\t\t\t\t{{\n'
            
            # Use eng name if available, if not use ID
            name_value = achievement["en-US"]["name"] if "en-US" in achievement and "name" in achievement["en-US"] else achievement["name_id"]
            achievement_id = f"NEW_ACHIEVEMENT_1_{i}"
            result += f'\t\t\t\t\t"name"\t"{name_value}"\n'

            # "name" - translations
            result += '\t\t\t\t\t\t"name"\n\t\t\t\t\t\t{\n'
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "unlockedTitle" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["name"]}"\n'
            result += f'\t\t\t\t\t\t\t"token"\t"{achievement_id}_NAME"\n'  # Use token
            result += '\t\t\t\t\t\t}\n'

            # "desc" -translations
            result += '\t\t\t\t\t\t"desc"\n\t\t\t\t\t\t{\n'
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "unlockedDescription" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["unlockedDescription"]}"\n'
            result += f'\t\t\t\t\t\t\t"token"\t"{achievement_id}_DESC"\n'  # Use token
            result += '\t\t\t\t\t\t}\n'

            # Other info translations
            result += f'\t\t\t\t\t\t"hidden"\t"{achievement.get("hidden", "0")}"\n'
            result += f'\t\t\t\t\t\t"icon"\t"{achievement.get("icon", "")}"\n'
            result += f'\t\t\t\t\t\t"icon_gray"\t"{achievement.get("icon_gray", "")}"\n'

            result += '\t\t\t\t\t}\n'  # display-ending
            result += '\t\t\t\t}\n'  # achievement node ending

        result += '\t\t\t}\n'  # bits-ending
        result += '\t\t\t"type"\t"ACHIEVEMENTS"\n'
        result += '\t\t}\n'  # stats-ending
        result += '\t}\n'  # stats-END
        result += f'\t"version"\t"{achievement.get("version", "")}"\n'
        result += f'\t"gamename"\t"{achievement.get("game_name", "")}"\n'
        result += '}\n'  # STRUCTURE END

        # Write VDF file
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"VDF successfully written to {self.file_name}.")


    # Fetch the language name from locale code
    def get_language_from_locale(self, locale):
        for lang, code in self.languages.items():
            if code == locale:
                return lang
        return locale  # Return code if no match

    # Generate language format data
    def generate_lang_format(self, merged_data):
        output = {}
        for entry in merged_data:
            for locale, content in entry.items():
                if locale not in self.languages.values():
                    continue  # Skip if not a recognized locale

                # Get language name and initialize structure
                language = self.get_language_from_locale(locale)
                if language not in output:
                    output[language] = {"Tokens": {}}

                # Add tokens to the language
                tokens = output[language]["Tokens"]
                achievement_id = entry["name_title"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
                tokens[f"{achievement_id}_NAME"] = content.get("name_title", "")
                tokens[f"{achievement_id}_DESC"] = content.get("unlockedDescription", "")

        return output



    def write_locales_to_vdf(self, merged_data):
     
        # Initialize an empty dictionary to hold the language-specific data
        output = defaultdict(lambda: {"Tokens": {}})

        # Iterate through the merged data
        for entry in merged_data:
            for locale, content in entry.items():
                # Skip if the locale is not a recognized language code
                if locale not in self.languages.values():
                    continue

                # Get the language from the locale
                language = self.get_language_from_locale(locale)

                # Add tokens for each achievement
                tokens = output[language]["Tokens"]
                achievement_id = entry["name_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
                tokens[f"{achievement_id}_NAME"] = content.get("name", "")
                tokens[f"{achievement_id}_DESC"] = content.get("unlockedDescription", "")

        # Start formatting the data into VDF style
        result = '"lang"\n{\n'

        for language, content in output.items():
            result += f'\t"{language}"\n\t{{\n'
            result += '\t\t"Tokens"\n\t\t{\n'

            for key, value in content["Tokens"].items():
                result += f'\t\t\t"{key}"\t"{value}"\n'

            result += '\t\t}\n\t}\n'

        result += '}'

        # Write the localized VDF file
        new_file_name = self.file_name.replace(".vdf", "_localed.vdf")
        with open(new_file_name, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"Localized VDF successfully written to {new_file_name}.")