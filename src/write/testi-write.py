import sys
import os
import vdf
import json

# Add path to access vdfparse module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'read'))

from vdfparse import value_dict  # Assuming this module parses the VDF file and returns a dictionary.

class Write:
    # The constructor initializes the file names and file format
    def __init__(self, file_name_vdf, file_name_txt, file_format):
        # If no file names are provided, default names are used
        self.file_name_vdf = file_name_vdf if file_name_vdf else "output.vdf"
        self.file_name_txt = file_name_txt if file_name_txt else "output.txt"
        self.file_format = file_format.lower() if file_format else ".vdf"

    def run(self):
        # Load the achievement data
        achievements = self.load_achievements()

        # Write both VDF and TXT files
        if self.file_format == ".vdf":
            self.write_to_vdf(achievements)
            self.write_to_txt(achievements)
        else:
            print(f"Unsupported format: {self.file_format}")

    # This method loads the example achievement data
    def load_achievements(self):
        # Here we include the game information and achievements data
        return {
            "id": "123456",
            "version": "2",
            "gamename": "Super Ultimate Awesome Game",
            "stats_type": "ACHIEVEMENTS",
            
            "Achievements": {
            "achievement_1_id": {
            "name_english": "Achievement 1",
            "name_finnish": "Saavutus 1",
            "name_token": "NEW_ACHIEVEMENT_1_1_NAME",
            "desc_english": "Description of Achievement 1",
            "desc_finnish": "Saavutus 1:en kuvaus",
            "desc_token": "NEW_ACHIEVEMENT_1_1_DESC",
            "hidden": "0",
            "icon": "Achievement_1.jpg",
            "icon_gray": "Achievement_Locked_1.jpg"
            },
            "achievement_2_id": {
            "name_english": "Achievement 2",
            "name_finnish": "Saavutus 2",
            "name_token": "NEW_ACHIEVEMENT_1_2_NAME",
            "desc_english": "Description of Achievement 2",
            "desc_finnish": "Saavutus 2:en kuvaus",
            "desc_token": "NEW_ACHIEVEMENT_1_2_DESC",
            "hidden": "1",
            "icon": "Achievement_2.jpg",
            "icon_gray": "Achievement_Locked_2.jpg"
            },
            "achievement_3_id": {
            "name_english": "Achievement 3",
            "name_finnish": "Saavutus 3",
            "name_token": "NEW_ACHIEVEMENT_1_3_NAME",
            "desc_english": "Description of Achievement 3",
            "desc_finnish": "Saavutus 3:en kuvaus",
            "desc_token": "NEW_ACHIEVEMENT_1_3_DESC",
            "hidden": "1",
            "icon": "Achievement_3.jpg",
            "icon_gray": "Achievement_Locked_3.jpg"
            }
        }
    }

    # This method writes the achievements to a VDF file
    def write_to_vdf(self, achievements):
        # Create a nested structure for the achievements in VDF format
        nested_data = {"GameInfo": achievements}

        # Convert the dictionary to VDF format
        vdf_text = vdf.dumps(nested_data, pretty=True)

        # Write the VDF data to the file
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

# Run the program to generate both VDF and TXT files
if __name__ == "__main__":
    # Start the program, which will create both VDF and TXT files
    writer = Write("achievements.vdf", "achievements.txt", ".vdf")
    writer.run()
