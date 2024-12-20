"""
This module provides functionality to write achievement data into different file formats.
Depending on the specified file format, it writes the data to the appropriate 
file format in a structured and formatted way.
"""

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

    def run(self):
        # Execute the writing process based on the specified file format.
        achievements = self.process.get_achievements()
        oikea_lista = self.process.fill_missing_values()

        # Write to XML if format is XML
        if self.file_format == ".xml":
            self.write_to_xml(achievements) 
        # Write to CSV if format is CSV
        elif self.file_format == ".csv":
            self.write_to_csv(achievements) 
        # Write to VDF if format is VDF
        elif self.file_format == ".vdf":
            self.write_to_vdf(achievements)
        # Print error for unsupported formats
        else:
            print(f"Unsupported format: {self.file_format}")  


    def write_to_xml(self, achievements):
        doc = minidom.Document()  # Create a new XML document
        root = doc.createElement('Achievements')  # Create the root element
        doc.appendChild(root)

        for achievement in achievements:
            print("processing achievement")  # debug message
            achievement_element = doc.createElement('Achievement')

            xml_tags_map = {
                "AchievementNameId": "name_id",
                "BaseAchievement": "hidden",
                "DisplayOrder": "acmt_num",
                "LockedDescriptionId": "desc_locked",
                "UnlockedDescriptionId": "desc_en",
                "IsHidden": "hidden",
                "AchievementId": "name_id",
                "IconImageId": "icon"
            }

        # Iterate over the xml_tags_map to create XML elements
            for xml_tag, achievement_key in xml_tags_map.items():
                if achievement_key in achievement and achievement[achievement_key] is not None:
                # Check if we are processing the "UnlockedDescriptionId" key
                    if xml_tag == "UnlockedDescriptionId":
                    # Create the Rewards element and inside it the gamerscore nest
                        rewards_element = doc.createElement("Rewards")
                        gamerscore = doc.createElement("Gamerscore")
                        gamerscore.appendChild(doc.createTextNode(str(achievement.get("gamerscore", 0))))  # Default 0 if not available
                        rewards_element.appendChild(gamerscore)
                        achievement_element.appendChild(rewards_element)  # Append Rewards before UnlockedDescriptionId

                # Add the current XML tag
                    element = doc.createElement(xml_tag)
                    element.appendChild(doc.createTextNode(str(achievement[achievement_key])))
                    achievement_element.appendChild(element)

        # Append the achievement element to the root
            root.appendChild(achievement_element)

    # Convert the document to a pretty-printed XML string
        xml_str = doc.toprettyxml(indent="  ")
        with open(self.file_name, "w") as f:
            f.write(xml_str)  # Write the XML string to the file

        print(f"Data written to {self.file_name} in XML format.")  # Confirm the write operation


    def write_to_csv(self, achievement):
        # Retrieve the list of achievements from the process
        acmt_list = self.process.get_achievements()
        if not acmt_list:
            print("No achievements to write.")
            return

        # This dictionary defines how internal data fields map to CSV column names
        csv_field_map = {
            "name": "name_id",
            "hidden": "hidden",
            "statThresholds": "acmt_stat_tres",
            "user_epic_achievements_xp": "acmt_xp",
        }

        # Extract the CSV column names from the keys of csv_field_map
        fieldnames = list(csv_field_map.keys())

        # Open the CSV file for writing. Using newline='' prevents extra blank lines
        with open(self.file_name, "w", newline='') as f:
            print(self.process) #debugmessage
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for achievement in acmt_list:
                row = {}
                for csv_key, data_key in csv_field_map.items():
                    # Retrieve the value from the achievement dictionary. If the key doesn't exist, use None
                    row[csv_key] = achievement.get(data_key, None)
                writer.writerow(row)

        print(f"Data written to {self.file_name} in CSV format.")

    # Create a dictionary for all achievements
    def write_to_vdf(self, achievements):   
        nested_data = {
            "123456": {                    # This is some kind of game identifier, adjust when informed what and how
                "stats": {}
            }
        }

        for i, achievement in enumerate(achievements, start=1):  # Create the structure for each achievement with a map, this is pretty 
            achievement_data = {
                "bits": {
                    str(i): {
                        "name": achievement.get("name_id", ""),
                        "display": {
                            "name": {
                                "english": achievement.get("name_en", ""),
                                "finnish": achievement.get("name_fi", ""),
                                "token": achievement.get("name_token", ""),
                            },
                            "desc": {
                                "english": achievement.get("desc_en", ""),
                                "finnish": achievement.get("desc_fi", ""),
                                "token": achievement.get("desc_token", ""),
                            },
                            "hidden": str(achievement.get("hidden", "false")),
                            "icon": achievement.get("icon", ""),
                            "icon_gray": achievement.get("icon_locked", ""),
                        }
                    }
                },
                "type": "ACHIEVEMENTS"
            }

            nested_data["123456"]["stats"][str(i)] = achievement_data  # Add the achievement to the stats section
        vdf_text = vdf.dumps(nested_data, pretty=True)     # Convert the dictionary to VDF format
        
        with open(self.file_name, "w") as f:  # Write to the VDF file
            f.write(vdf_text)

        print(f"Data written to {self.file_name} in nested VDF format.")