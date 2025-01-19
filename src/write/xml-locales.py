import xml.dom.minidom as minidom
from collections import defaultdict

class LocalizationXmlWriter:

    def __init__(self, file_name, data_source):
        self.file_name = file_name
        self.data_source = data_source

    def write_localizations_to_xml(self):
        data = self.data_source.get_localizations()
        if not data:
            print("No localization data to write.")
            return

        doc = minidom.Document()
        root = doc.createElement("Localization")
        doc.appendChild(root)

        dev_locale_elem = doc.createElement("DevDisplayLocale")
        dev_locale_elem.setAttribute("locale", "en-US")
        root.appendChild(dev_locale_elem)

        grouped_achievements = defaultdict(list)
        grouped_locked_desc = defaultdict(list)
        grouped_unlocked_desc = defaultdict(list)

        for row in data:
            name_id = row["name"]  
            text1 = row.get("unlockedTitle", "")
            grouped_achievements[name_id].append({
                "locale": row["locale"],
                "text": text1
            })

            locked_id = "LockedDescriptionId" + row["name"][-1]
            locked_text = row.get("lockedDescription", "")
            grouped_locked_desc[locked_id].append({
                "locale": row["locale"],
                "text": locked_text
            })

            unlock_id = "UnlockedDescriptionId" + row["name"][-1]
            unlock_text = row.get("unlockedDescription", "")
            grouped_unlocked_desc[unlock_id].append({
                "locale": row["locale"],
                "text": unlock_text
            })

        def build_elements(group_dict):
            elements = []
            for id_value, rows_ in group_dict.items():
                ls_elem = doc.createElement("LocalizedString")
                ls_elem.setAttribute("id", id_value)

                for item in rows_:
                    val_elem = doc.createElement("Value")
                    val_elem.setAttribute("locale", item["locale"])

                    text_node = doc.createTextNode(item["text"])
                    val_elem.appendChild(text_node)
                    ls_elem.appendChild(val_elem)

                elements.append(ls_elem)
            return elements

        for elem in build_elements(grouped_achievements):
            root.appendChild(elem)
        for elem in build_elements(grouped_locked_desc):
            root.appendChild(elem)
        for elem in build_elements(grouped_unlocked_desc):
            root.appendChild(elem)

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