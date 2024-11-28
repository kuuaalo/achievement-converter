# Import the document class for creating XML documents
from xml.dom.minidom import Document

# Define a dictionary to store XML tags and their corresponding achievement keys
xml_tags = {
    "AchievementNameId": "name_id",
    "BaseAchievement": "hidden",
    "DisplayOrder": "acmt_num",
    "LockedDescriptionId": "desc_locked",
    "UnlockedDescriptionId": "desc_en",
    "IsHidden": "hidden",
    "AchievementId": "name_id",
    "IconImageId": "icon"
}

# Create a sample achievement dictionary for testing
achievements = [{
    "name_id": "Achievement_01",
    "hidden": "False",
    "acmt_num": "1",
    "desc_locked": "This is locked",
    "desc_en": "Unlocked description",
    "icon": "icon123.png",
    "gamerscore": "0"
},
{
    "name_id": "Achievement_02",
    "hidden": "true",
    "acmt_num": "1",
    "desc_locked": "This is locked",
    "desc_en": "Locked description",
    "icon": "icon123.png",
    "gamerscore": "1"
},
{
    "name_id": "Achievement_04",
    "hidden": "false",
    "acmt_num": "1",
    "desc_locked": "This is locked",
    "desc_en": "Unlocked description",
    "icon": "icon123.png",
    "gamerscore": "1"
}]

# Create a new XML document
doc = Document()

# Create the root element 'Achievement' for the XML document
root = doc.createElement('Achievement')  
doc.appendChild(root)

for achievement in achievements:
    # Create the 'Achievement' element for each achievement
    achievement_element = doc.createElement('Achievement')


# Loop through each key-value pair in the xml_tags dictionary
    for xml_tag, achievement_key in xml_tags.items():
        if achievement_key in achievement and achievement[achievement_key] is not None:
        # Before adding the 'UnlockedDescriptionId', insert 'Rewards' with gamerscore nest
            if xml_tag == "UnlockedDescriptionId":
            # Create the Rewards element
                rewards_element = doc.createElement("Rewards")
                gamerscore = doc.createElement("Gamerscore")
                gamerscore.appendChild(doc.createTextNode(str(achievement["gamerscore"])))
                rewards_element.appendChild(gamerscore)
                achievement_element.appendChild(rewards_element)  # Append Rewards before UnlockedDescriptionId

        # Add the current XML tag
            element = doc.createElement(xml_tag)
            element.appendChild(doc.createTextNode(str(achievement[achievement_key])))
            achievement_element.appendChild(element)

        root.appendChild(achievement_element)

# Save the XML structure to a file named 'achievements.xml'
with open("achievements.xml", "w", encoding="utf-8") as f:
    f.write(doc.toprettyxml(indent="  "))

print("XML file 'achievements.xml' created successfully.")
