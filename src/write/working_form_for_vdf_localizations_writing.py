
    def write_localizations_to_xml(self, achievements):
        """
        Writes localization data to an XML file, where each language has its corresponding
        achievement strings (locked/unlocked titles and descriptions).
        """
        # Create the XML document
        doc = minidom.Document()
        root = doc.createElement('Localization')
        root.setAttribute("xmlns", "http://config.mgt.xboxlive.com/schema/localization/1")
        doc.appendChild(root)

        # Add the DevDisplayLocale element
        dev_locale = doc.createElement('DevDisplayLocale')
        dev_locale.setAttribute('locale', 'en-US')
        root.appendChild(dev_locale)

        # Iterate over all achievements
        for achievement in achievements:
            achievement_id = achievement.get("name_id", "")  # Unique identifier for the achievement
            
            # Loop through all languages and create the appropriate LocalizedString for each
            for locale, lang_data in achievement.items():
                if isinstance(lang_data, dict):  # Only process language data
                    # Add locked title
                    if "lockedTitle" in lang_data:
                        localized_string = doc.createElement('LocalizedString')
                        localized_string.setAttribute('id', f"LockedDescriptionId{achievement_id[-1]}")  # e.g., "LockedDescriptionId1"
                        locked_title = doc.createElement('Value')
                        locked_title.setAttribute('locale', locale)
                        locked_title.appendChild(doc.createTextNode(lang_data["lockedTitle"]))
                        localized_string.appendChild(locked_title)
                        root.appendChild(localized_string)
                    
                    # Add locked description
                    if "lockedDescription" in lang_data:
                        localized_string = doc.createElement('LocalizedString')
                        localized_string.setAttribute('id', f"LockedDescriptionId{achievement_id[-1]}")  # e.g., "LockedDescriptionId1"
                        locked_desc = doc.createElement('Value')
                        locked_desc.setAttribute('locale', locale)
                        locked_desc.appendChild(doc.createTextNode(lang_data["lockedDescription"]))
                        localized_string.appendChild(locked_desc)
                        root.appendChild(localized_string)

                    # Add unlocked title
                    if "unlockedTitle" in lang_data:
                        localized_string = doc.createElement('LocalizedString')
                        localized_string.setAttribute('id', f"UnlockedDescriptionId{achievement_id[-1]}")  # e.g., "UnlockedDescriptionId1"
                        unlocked_title = doc.createElement('Value')
                        unlocked_title.setAttribute('locale', locale)
                        unlocked_title.appendChild(doc.createTextNode(lang_data["unlockedTitle"]))
                        localized_string.appendChild(unlocked_title)
                        root.appendChild(localized_string)

                    # Add unlocked description
                    if "unlockedDescription" in lang_data:
                        localized_string = doc.createElement('LocalizedString')
                        localized_string.setAttribute('id', f"UnlockedDescriptionId{achievement_id[-1]}")  # e.g., "UnlockedDescriptionId1"
                        unlocked_desc = doc.createElement('Value')
                        unlocked_desc.setAttribute('locale', locale)
                        unlocked_desc.appendChild(doc.createTextNode(lang_data["unlockedDescription"]))
                        localized_string.appendChild(unlocked_desc)
                        root.appendChild(localized_string)

        # Write to XML file (localizations will be saved with '_localed.xml' suffix)
        localizations_file_name = self.file_name.replace(".xml", "_localed.xml")
        localized_xml_str = doc.toprettyxml(indent="  ")

        with open(localizations_file_name, "w", encoding="utf-8") as f:
            f.write(localized_xml_str)

        print(f"Localization XML written to {localizations_file_name}.")
