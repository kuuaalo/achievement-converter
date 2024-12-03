import xml.dom.minidom as minidom
import csv
import vdf
# from tero import tero
import read.vdfparse as vdf2

class Write:
    def __init__(self, file_name, file_format, tero):
        if file_name:
            self.file_name = file_name
        else:
            print("Wrong file name")
            return

        if file_format:
            self.file_format = file_format.lower()  # Set the file format to lowercase
        else:
            print("Wrong format from write")  # Print error if file format is invalid
            return
        self.tero=tero

    def run(self):
        achievements = self.tero.get_achievements()
        print("write debugmessage no:1")
    
        #achievements = vdf2.value_dict() 
        
        if self.file_format == ".xml":
            self.write_to_xml(achievements) # Write to XML if format is XML
        elif self.file_format == ".csv":
            self.write_to_csv(achievements) # Write to CSV if format is CSV
        elif self.file_format == ".txt":
            #self.write_to_txt(achievements) # write to TXT if formar is TXT
            self.write_to_vdf(achievements)
        elif self.file_format == ".vdf":
            self.write_to_vdf(achievements) # Write to VDF if format is VDF
        else:
            print(f"Unsupported format: {self.file_format}")  # Print error for unsupported formats





    def write_to_xml(self, achievements): # File now goes through the function, and makes an xml file. It still doesn't work and only prints one line. The test version in a separate file worked perfectly.
        doc = minidom.Document()  # Create a new XML document
        root = doc.createElement('Achievements')  # Create the root element
        doc.appendChild(root)

        for achievement in achievements:
            print("processing achievement")#debug.no1
            achievement_element = doc.createElement('Achievement')
    
            xml_tags_map= {
                "AchievementNameId": "name_id",
                "BaseAchievement": "hidden",
                "DisplayOrder": "acmt_num",
                "LockedDescriptionId": "desc_locked",
                "UnlockedDescriptionId": "desc_en",
                "IsHidden": "hidden",
               "AchievementId": "name_id",
                "IconImageId": "icon"
}
            for xml_tag, achievement_key in xml_tags_map.items():
                if achievement_key in achievement and achievement[achievement_key] is not None:
  # Add the current XML tag
                    element = doc.createElement(xml_tag)
                    element.appendChild(doc.createTextNode(str(achievement[achievement_key])))
                    
                    achievement_element.appendChild(element)
        # Before adding the 'UnlockedDescriptionId', insert 'Rewards' with gamerscore nest
                    if "UnlockedDescriptionId" in xml_tags_map.values():
            # Create the Rewards element and inside it the gamerscore nest
                        rewards_element = doc.createElement("Rewards")
                        gamerscore = doc.createElement("Gamerscore")
                        gamerscore.appendChild(doc.createTextNode(str(achievement.get("gamerscore", 0)))) #FOR NOW, CREATES A FORCED VALUE HERE
                        rewards_element.appendChild(gamerscore)
                        achievement_element.appendChild(rewards_element)  # Append Rewards before UnlockedDescriptionId
      


                    root.appendChild(achievement_element) #Adds achievement to main element

        xml_str = doc.toprettyxml(indent="  ")  # Convert the document to a pretty-printed XML string
        with open(self.file_name, "w") as f:
            f.write(xml_str)  # Write the XML string to the file

        print(f"Data written to {self.file_name} in XML format.")  # Confirm the write operation

    def write_to_csv(self, achievements):
        # Using DictWriter to write to a CSV file
        with open(self.file_name, "w", newline='') as f:  # Open the file for writing with newline handling
            print(self.tero)#debugmessage
            writer = csv.DictWriter(f, fieldnames=[])  # Define field names for the CSV
            writer.writeheader()
            writer.writerows(achievements)  # Write all rows from the achievements list

        print(f"Data written to {self.file_name} in CSV format.")  # Confirm the write operation

    def write_to_vdf(self, achievements):
        # Create a nested structure for the achievements in VDF format
        nested_data = {"GameInfo": achievements}

        # Convert the dictionary to VDF format
        vdf_text = vdf.dumps(nested_data, pretty=True)

        with open(self.file_name_vdf, "w") as f:
            f.write(vdf_text)

        print(f"Data written to {self.file_name_vdf} in nested VDF format.")

# This method writes the achievements to a plain text file
    def write_to_txt(self, achievements):
        # Write the achievements in a readable plain text format
        with open(self.file_name_txt, "w") as f:
            # First, write game-level information (id, version, etc.)
            f.write(f"Game Information:\n")
            f.write(f"ID: {achievements['id']}\n")
            f.write(f"Version: {achievements['version']}\n")
            f.write(f"Game Name: {achievements['gamename']}\n")
            f.write(f"Stats Type: {achievements['stats_type']}\n")
            f.write("\n")

            # Write achievements inside the "Achievements" block
            f.write("Achievements:\n")
            for achievement_id, details in achievements["Achievements"].items():
                f.write(f"Achievement ID: {achievement_id}\n")
                for subkey, subvalue in details.items():
                    f.write(f"  {subkey}: {subvalue}\n")
                f.write("\n")

        print(f"Data written to {self.file_name_txt} in plain text format.")

    