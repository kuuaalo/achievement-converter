import xml.dom.minidom as minidom

class LocalizationXmlWriter:

    def __init__(self, file_name, data_source):
        
        self.file_name = file_name
        self.data_source = data_source

    def write_localizations_to_xml(self):

        localizations = self.data_source.get_localizations()
        if not localizations:
            print("No localization data to write.")
            return

        doc = minidom.Document()
        root = doc.createElement("Localization")
        doc.appendChild(root)

        dev_locale_elem = doc.createElement("DevDisplayLocale")
        dev_locale_elem.setAttribute("locale", "en-US")
        root.appendChild(dev_locale_elem)

        for loc in localizations:
            
            localized_string_elem = doc.createElement("LocalizedString")
            localized_string_elem.setAttribute("id", loc["name"])
            
            value_elem = doc.createElement("Value")
            value_elem.setAttribute("locale", loc["locale"])

            value_elem.setAttribute("lockedTitle", loc.get("lockedTitle", ""))
            value_elem.setAttribute("lockedDescription", loc.get("lockedDescription", ""))
            value_elem.setAttribute("unlockedTitle", loc.get("unlockedTitle", ""))
            value_elem.setAttribute("unlockedDescription", loc.get("unlockedDescription", ""))
            value_elem.setAttribute("flavorText", loc.get("flavorText", ""))
            value_elem.setAttribute("lockedIcon", loc.get("lockedIcon", ""))
            value_elem.setAttribute("unlockedIcon", loc.get("unlockedIcon", ""))

            localized_string_elem.appendChild(value_elem)
            root.appendChild(localized_string_elem)

        xml_bytes = doc.toprettyxml(indent="  ", encoding="utf-8")

        with open(self.file_name, "wb") as f:
            f.write(xml_bytes)

        print(f"Localization data written to {self.file_name} in XML format.")


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
    
    writer = LocalizationXmlWriter("localizations.xml", data_source)
    writer.write_localizations_to_xml()
