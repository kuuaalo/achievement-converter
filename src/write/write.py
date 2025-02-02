"""
This module provides functionality to write achievement data into different file formats.
Depending on the specified file format, it writes the data to the appropriate 
file format in a structured and formatted way.
"""
from collections import defaultdict
import xml.dom.minidom as minidom
import csv
import vdf

class Write:
    def __init__(self, file_name, file_format, process):
        
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
        self.languages = {
            "arabic": "ar",
            "danish": "da",
            "dutch": "nl",
            "finnish": "fi",
            "french": "fr",
            "german": "de",
            "italian": "it",
            "japanese": "ja",
            "korean": "ko",
            "koreana": "ko",
            "norwegian": "no",
            "polish": "pl",
            "brazilian": "pt-BR",
            "russian": "ru",
            "schinese": "zh-Hans",
            "latam": "es-MX",
            "spanish": "es-ES",
            "swedish": "sv",
            "thai": "th",
            "tchinese": "zh-Hant",
            "turkish": "tr",
            "english": "en-US"
        }

    def run(self):
        # Execute the writing process based on the specified file format.
        achievements = self.process.get_all_data() # modified this to call merged data, so this should get achievement data AND localization data in one dictionary
        oikea_lista = self.process.fill_missing_values()

#        localizations = self.process.get_localizations()
#        localized_data = self.merge_achievements_and_localizations(achievements,localizations)

        # Write to XML if format is XML
        if self.file_format == ".xml":
            self.write_to_xml(achievements) 
        # Write to CSV if format is CSV
        elif self.file_format == ".csv":
            self.write_to_csv(achievements)
            self.write_locales_to_csv(achievements)
        # Write to VDF if format is VDF
        elif self.file_format == ".vdf":
            self.write_to_vdf(achievements)
            self.write_locales_to_vdf(achievements)
        # Print error for unsupported formats
        else:
            print(f"Unsupported format: {self.file_format}")  
















    def write_to_xml(self, achievements):
        # Create the XML document
        doc = minidom.Document()
        root = doc.createElement('Achievements2017')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/achievements2017/1")
        doc.appendChild(root)

        for i, achievement in enumerate(achievements, start=1):
            print(f"Processing achievement {i}")  # Debug message

            achievement_element = doc.createElement('Achievement')

            # Map XML tags to achievement data keys
            xml_tags_map = {
                "AchievementNameId": "name_id",
                "BaseAchievement": "base_acmt",
                "DisplayOrder": "acmt_num",
                "LockedDescriptionId": "desc_locked",
                "UnlockedDescriptionId": "desc_token",
                "IsHidden": "hidden",
                "AchievementId": str(i),  # Achievement ID perustuu indeksiin
                "IconImageId": "icon"
            }

            # Iterate over the xml_tags_map to create XML elements
            for xml_tag, key in xml_tags_map.items():
                element = doc.createElement(xml_tag)

                # Special handling for certain tags
                if xml_tag == "UnlockedDescriptionId":
                    # Rewards block before UnlockedDescriptionId
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
                    element.appendChild(doc.createTextNode(key))  # Kovakoodattu ID
                else:
                    element.appendChild(doc.createTextNode(str(achievement.get(key, ""))))  # Haetaan oikeasta avaimesta

                # Append element to Achievement
                achievement_element.appendChild(element)

            # Append the achievement to the root
            root.appendChild(achievement_element)

        # Write the XML document to a file
        xml_str = doc.toprettyxml(indent="  ")
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(xml_str)

        print(f"XML successfully written to {self.file_name}.")
















    # Writes achievements in CSV format
    def write_to_csv(self, achievements):
        # Retrieve the list of achievements from the process
        #acmt_list = self.process.get_achievements()
        #if not acmt_list:
        #    print("No achievements to write.")
        #    return

        # This dictionary defines how internal data fields map to CSV column names
        csv_field_map = {
            "name_id": "name",
            "hidden": "hidden",
            "acmt_stat_tres": "statThresholds",
            "acmt_xp": "user_epic_achievements_xp",
        }

        # Extract the CSV column names from the keys of csv_field_map
        fieldnames = list(csv_field_map.keys())

        # Open the CSV file for writing. Using newline='' prevents extra blank lines
        with open(self.file_name, "w", newline='', encoding="utf-8") as f:
            print(self.process) #debugmessage
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for achievement in achievements:
                row = {}
                for csv_key, data_key in csv_field_map.items():
                    # Retrieve the value from the achievement dictionary. If the key doesn't exist, use None
                    row[csv_key] = achievement.get(data_key, None)
                writer.writerow(row)
                 

        print(f"Data written to {self.file_name} in CSV format.")

    def write_locales_to_csv(self, achievements):
        """
        Writes localization data to a CSV file.

        This function extracts localization information from the given achievement data
        and saves it into a separate CSV file with appropriate field names.
        """    
        # Generate the file name for the localization CSV
        locales_file_name = self.file_name.replace(".csv", "_locales.csv")

        # Define column names for the CSV file
        fieldnames = [
            "name",
            "locale",
            "lockedTitle",
            "lockedDescription",
            "unlockedTitle",
            "unlockedDescription",
            "flavorText",
            "lockedIcon",
            "unlockedIcon"
        ]

        # Open the localization CSV file for writing
        with open(locales_file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # Initialize CSV writer
            writer.writeheader()  # Write the column headers

            # Loop through each achievement and extract localization details
            for achievement in achievements:
                row = {
                    "name": achievement.get("name", ""),
                    "locale": achievement.get("locale", "default"),
                    "lockedTitle": achievement.get("lockedTitle", ""),
                    "lockedDescription": achievement.get("lockedDescription", ""),
                    "unlockedTitle": achievement.get("unlockedTitle", ""),
                    "unlockedDescription": achievement.get("unlockedDescription", ""),
                    "flavorText": achievement.get("flavorText", ""),
                    "lockedIcon": achievement.get("lockedIcon", ""),
                    "unlockedIcon": achievement.get("unlockedIcon", "")
                }
                writer.writerow(row)  # Write extracted data as a row in the CSV file

        # Print confirmation message
        print(f"Localization data successfully written to {locales_file_name} in CSV format.")










    def write_to_vdf(self, achievements):
        # Aloitetaan VDF-tiedoston rakenne
        result = '"123456"\n{\n'
        result += '\t"stats"\n\t{\n'
        result += '\t\t"1"\n\t\t{\n'
        result += '\t\t\t"bits"\n\t\t\t{\n'

        for i, achievement in enumerate(achievements, start=1):
            result += f'\t\t\t\t"{i}"\n\t\t\t\t{{\n'
            result += f'\t\t\t\t\t"name"\t"{achievement["name_id"]}"\n'
            result += '\t\t\t\t\t"display"\n\t\t\t\t\t{\n'

            # "name" -käännökset
            result += '\t\t\t\t\t\t"name"\n\t\t\t\t\t\t{\n'
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "unlockedTitle" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["unlockedTitle"]}"\n'
            result += f'\t\t\t\t\t\t\t"token"\t"{achievement.get("name_token", "")}"\n'
            result += '\t\t\t\t\t\t}\n'

            # "desc" -käännökset
            result += '\t\t\t\t\t\t"desc"\n\t\t\t\t\t\t{\n'
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict) and "unlockedDescription" in lang_data:
                    language = self.get_language_from_locale(locale)
                    result += f'\t\t\t\t\t\t\t"{language}"\t"{lang_data["unlockedDescription"]}"\n'
            result += f'\t\t\t\t\t\t\t"token"\t"{achievement.get("desc_token", "")}"\n'
            result += '\t\t\t\t\t\t}\n'

            # Muut saavutuksen tiedot
            result += f'\t\t\t\t\t\t"hidden"\t"{achievement.get("hidden", "0")}"\n'
            result += f'\t\t\t\t\t\t"icon"\t"{achievement.get("icon", "")}"\n'
            result += f'\t\t\t\t\t\t"icon_gray"\t"{achievement.get("icon_gray", "")}"\n'

            result += '\t\t\t\t\t}\n'  # display-pääte
            result += '\t\t\t\t}\n'  # Saavutusnoden pääte

        result += '\t\t\t}\n'  # bits-osuuden pääte
        result += '\t\t\t"type"\t"ACHIEVEMENTS"\n'
        result += '\t\t}\n'  # stats-osuuden pääte
        result += '\t}\n'  # stats-puu pääte
        result += '\t"version"\t"2"\n'
        result += '\t"gamename"\t"Super Ultimate Awesome Game"\n'
        result += '}\n'  # Koko rakenteen pääte

        # Kirjoitetaan VDF-tiedosto
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"VDF successfully written to {self.file_name}.")

############### Lokalisaatio
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
                achievement_id = entry["name_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
                tokens[f"{achievement_id}_NAME"] = content.get("unlockedTitle", "")
                tokens[f"{achievement_id}_DESC"] = content.get("unlockedDescription", "")

        return output

    def write_locales_to_vdf(self, merged_data):
        """
        Write localized achievement data to a VDF file.
        """
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
                tokens[f"{achievement_id}_NAME"] = content.get("unlockedTitle", "")
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