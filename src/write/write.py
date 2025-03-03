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
            self.write_localizations_to_xml(achievements) 
            self.write_to_xml(achievements)
            
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
        doc = minidom.Document()
        root = doc.createElement('AchievementsXXXX')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/achievements2017/1")
        doc.appendChild(root)

        for i, achievement in enumerate(achievements, start=1):
            if not achievements:
                self.gui.show_error("Error", "No data provided for XML file")
                return

            achievement_element = doc.createElement('Achievement')

            # 🔹 Nyt käytetään lokalisaation generoimia ID:tä
            xml_tags_map = {
                "AchievementNameId": "name_id",
                "BaseAchievement": "base_acmt",
                "DisplayOrder": "acmt_num",
                "LockedDescriptionId": "LockedDescriptionId",  # 🔹 Käyttää lokalisaation ID:tä
                "UnlockedDescriptionId": "UnlockedDescriptionId",  # 🔹 Sama täällä
                "IsHidden": "hidden",
                "AchievementId": str(i),
                "IconImageId": "icon"
            }

            for xml_tag, key in xml_tags_map.items():
                element = doc.createElement(xml_tag)

                if xml_tag == "UnlockedDescriptionId":
                    rewards_element = doc.createElement("Rewards")
                    gamerscore = doc.createElement("Gamerscore")
                    gamerscore.appendChild(doc.createTextNode(str(achievement.get("acmt_xp", "0"))))
                    rewards_element.appendChild(gamerscore)
                    achievement_element.appendChild(rewards_element)

                if xml_tag == "BaseAchievement":
                    element.appendChild(doc.createTextNode(str(achievement.get(key, "true")).lower()))
                elif xml_tag == "IsHidden":
                    element.appendChild(doc.createTextNode("true" if achievement.get(key, False) else "false"))
                elif xml_tag == "AchievementId":
                    element.appendChild(doc.createTextNode(str(i)))
                else:
                    # 🔹 Nyt haetaan oikein generoidut ID:t
                    element.appendChild(doc.createTextNode(str(achievement.get(key, ""))))

                achievement_element.appendChild(element)
            root.appendChild(achievement_element)

        xml_str = doc.toprettyxml(indent="  ")
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(xml_str)

        print(f"XML successfully written to {self.file_name}.")



 

    
    def write_localizations_to_xml(self, achievements):
        output_filename = self.file_name.replace(".xml", "_localized.xml")

        doc = minidom.Document()
        root = doc.createElement('Localization')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/localization/1")
        doc.appendChild(root)

        dev_locale = doc.createElement('DevDisplayLocale')
        dev_locale.setAttribute('locale', 'en-US')
        root.appendChild(dev_locale)

        achievement_strings = []
        locked_description_strings = []
        unlocked_description_strings = []

        for achievement in achievements:
            achievement_id = achievement.get("name_id", "")

            # 🔹 Generoidaan oikeat ID:t ja tallennetaan ne sanakirjaan
            locked_desc_id = f"LockedDescription{achievement_id[11:]}"
            unlocked_desc_id = f"UnlockedDescription{achievement_id[11:]}"
            achievement["LockedDescriptionId"] = locked_desc_id
            achievement["UnlockedDescriptionId"] = unlocked_desc_id

            localized_name = doc.createElement('LocalizedString')
            localized_name.setAttribute('id', achievement_id)

            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "name" in lang_data and locale != "default":
                    value_elem = doc.createElement('Value')
                    value_elem.setAttribute('locale', locale)
                    value_elem.appendChild(doc.createTextNode(lang_data["name"]))
                    localized_name.appendChild(value_elem)

            achievement_strings.append(localized_name)

            for desc_type, desc_id in [("lockedDescription", locked_desc_id), ("unlockedDescription", unlocked_desc_id)]:
                localized_desc = doc.createElement('LocalizedString')
                localized_desc.setAttribute('id', desc_id)

                for locale, lang_data in achievement.items():
                    if isinstance(lang_data, dict) and desc_type in lang_data and locale != "default":
                        value_elem = doc.createElement('Value')
                        value_elem.setAttribute('locale', locale)
                        value_elem.appendChild(doc.createTextNode(lang_data[desc_type]))
                        localized_desc.appendChild(value_elem)

                if localized_desc.childNodes:
                    if desc_type == "lockedDescription":
                        locked_description_strings.append(localized_desc)
                    else:
                        unlocked_description_strings.append(localized_desc)

        for entry in achievement_strings + locked_description_strings + unlocked_description_strings:
            root.appendChild(entry)

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
        if not achievements:
            self.gui.show_error("Error", "No data provided for VDF file")
            return

        # Oletusarvot, jos kenttiä ei ole määritelty
        game_id = achievements[0].get("game_id", "None")
        version = achievements[0].get("version", "None")
        game_name = achievements[0].get("game_name", "None")

        result = f'"{game_id}"\n{{\n'
        result += '\t"stats"\n\t{\n'
        result += '\t\t"1"\n\t\t{\n'  # Päälohko saavutuksille
        result += '\t\t\t"bits"\n\t\t\t{\n'  # Kaikki saavutukset yhteen "bits"-lohkoon

        # Loopataan kaikki saavutukset
        for i, achievement in enumerate(achievements, start=1):
            result += f'\t\t\t\t"{i}"\n\t\t\t\t{{\n'
            result += f'\t\t\t\t\t"name"\t"{achievement["name_id"]}"\n'

            # "display" translations
            result += '\t\t\t\t\t"display"\n\t\t\t\t\t{\n'
            result += f'\t\t\t\t\t\t"name"\n\t\t\t\t\t\t{{\n'

            # Luetaan kaikki mahdolliset kieliversiot "name" kentästä
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "name" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["name"]}"\n'

            # Lisää token kenttä
            achievement_token_id = f"NEW_ACHIEVEMENT_1_{i}"
            result += f'\t\t\t\t\t\t\t"token"\t"{achievement_token_id}_NAME"\n'
            result += f'\t\t\t\t\t\t}}\n'  # Suljetaan "name"

            # "desc" translations
            result += f'\t\t\t\t\t\t"desc"\n\t\t\t\t\t\t{{\n'
            # Luetaan kaikki mahdolliset kieliversiot "unlockedDescription" kentästä
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "unlockedDescription" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["unlockedDescription"]}"\n'

            result += f'\t\t\t\t\t\t\t"token"\t"{achievement_token_id}_DESC"\n'
            result += f'\t\t\t\t\t\t}}\n'  # Suljetaan "desc"

            # Lisätään "hidden", "icon", ja "icon_gray"
            result += f'\t\t\t\t\t\t"hidden"\t"{str(achievement.get("hidden", "false")).lower()}"\n'  # "hidden" pitäisi olla merkkijono
            result += f'\t\t\t\t\t\t"icon"\t"{achievement.get("icon", "")}"\n'
            result += f'\t\t\t\t\t\t"icon_gray"\t"{achievement.get("icon_gray", "")}"\n'

            result += '\t\t\t\t\t}\n'  # Suljetaan yksittäinen saavutustieto
            result += '\t\t\t\t}\n'  # Suljetaan saavutustieto

        result += '\t\t\t}\n'  # Suljetaan "bits"

        

        # Lisätään "type", "version" ja "gamename"
        result += '\t\t\t"type"\t"ACHIEVEMENTS"\n'
        result += '\t\t}\n'  # Suljetaan "stats"
        result += '\t}\n'  # Suljetaan koko tiedosto
        result += f'\t"version"\t"{version}"\n'
        result += f'\t"gamename"\t"{game_name}"\n'
        result += '}\n'  # Suljetaan päälohko

        # Kirjoitetaan VDF-tiedosto
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