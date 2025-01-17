import csv

class LocalizationWriter:
    def __init__(self, file_name, data_source):
       
        self.file_name = file_name
        self.data_source = data_source

    def write_localizations_to_csv(self):
        
        localizations = self.data_source.get_localizations()

        if not localizations:
            print("No localization data to write.")
            return

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

        with open(self.file_name, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()

            for loc in localizations:
                row = {
                    "name": loc.get("name", ""), 
                    "locale": loc.get("locale", ""),
                    "lockedTitle": loc.get("lockedTitle", ""),
                    "lockedDescription": loc.get("lockedDescription", ""),
                    "unlockedTitle": loc.get("unlockedTitle", ""),
                    "unlockedDescription": loc.get("unlockedDescription", ""),
                    "flavorText": loc.get("flavorText", ""),
                    "lockedIcon": loc.get("lockedIcon", ""),
                    "unlockedIcon": loc.get("unlockedIcon", ""),
                }
                writer.writerow(row)

        print(f"Localization data written to {self.file_name} in CSV format.")


class MockLocalizationSource:
    def get_localizations(self):
        return [
            {
                "name": "AchievementID1",
                "locale": "en-US",
                "lockedTitle": "Locked Achievement 1",
                "lockedDescription": "Locked Description of Achievement 1",
                "unlockedTitle": "Achievement 1",
                "unlockedDescription": "Description of Achievement 1",
                "flavorText": "",
                "lockedIcon": "Achievement_Locked_1.jpg",
                "unlockedIcon": "Achievement_1.jpg",
            },
            {
                "name": "AchievementID1",
                "locale": "fi",
                "lockedTitle": "Lukittu Saavutus 1",
                "lockedDescription": "Lukittu Saavutus 1:en kuvaus",
                "unlockedTitle": "Saavutus 1",
                "unlockedDescription": "Saavutus 1:en kuvaus",
                "flavorText": "",
                "lockedIcon": "Achievement_Locked_1.jpg",
                "unlockedIcon": "Achievement_1.jpg",
            },
            {
                "name": "AchievementID1",
                "locale": "default",
                "lockedTitle": "Locked Achievement 1",
                "lockedDescription": "Locked Description of Achievement 1",
                "unlockedTitle": "Achievement 1",
                "unlockedDescription": "Description of Achievement 1",
                "flavorText": "",
                "lockedIcon": "Achievement_Locked_1.jpg",
                "unlockedIcon": "Achievement_1.jpg",
            },
        ]


if __name__ == "__main__":
    data_source = MockLocalizationSource()
    writer = LocalizationWriter("localization.csv", data_source)
    writer.write_localizations_to_csv()
