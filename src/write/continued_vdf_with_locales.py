
main_button = 2


def write_to_vdf(self, achievements):
    nested_data = {
        "game_id": {
            "stats": {}
        }
    }

    for i, achievement in enumerate(achievements, start=1):
        # Määrittele display_data sanakirjaksi, ei listaksi
        display_data = {
            "name": {},
            "description": {},
            "hidden": str(achievement.get("hidden", "false")),
            "icon": achievement.get("icon", ""),
            "icon_gray": achievement.get("icon_locked", ""),
        }


        for localization in achievement.get("localizations", []):
            locale = localization.get("locale")
            if locale:
                display_data["name"][locale] = localization.get("unlocked_title", "")
                display_data["description"][locale] = localization.get("unlocked_description", "")

        achievement_data = {
            "bits": {
                str(i): {
                    "name": achievement.get("name_id", ""),
                    "display": display_data
                }
            },
            "type": "ACHIEVEMENTS"
        }

        # Lisää achievement_data nested_data-rakenteeseen
        nested_data["game_id"]["stats"][str(i)] = achievement_data 

    # Muunna nested_data VDF-muotoon
    vdf_text = vdf.dumps(nested_data, pretty=True)

    # Kirjoita VDF-data tiedostoon
    with open(self.file_name, "w", encoding="utf-8") as f:
        f.write(vdf_text)


    print(f"Data written to {self.file_name} in nested VDF format.")

    

# fetch the lang and locale
def get_language_from_locale(locale):
    for lang, code in languages.items():
        if code == locale:
            return lang #return the language form
    return locale  # returning code to make sure

def generate_lang_format(list_of_localizations):
    output = {}
    for achievement in list_of_localizations:
        achievement_id = achievement["achievement_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
        
        for localization in achievement["localizations"]:
            locale = localization["locale"]
            language = get_language_from_locale(locale)
            
            if language not in output:
                output[language] = {"Tokens": {}}
            
            tokens = output[language]["Tokens"]
            tokens[f"{achievement_id}_NAME"] = localization["unlocked_title"]
            tokens[f"{achievement_id}_DESC"] = localization["unlocked_description"]
    
    return output

# Format the output into the custom "lang" format
def format_custom_lang(data):
    result = '"lang"\n{\n'
    for locale, content in data.items():
        result += f'\t"{locale}"\n\t{{\n'
        result += '\t\t"Tokens"\n\t\t{\n'
        for key, value in content["Tokens"].items():
            result += f'\t\t\t"{key}"\t"{value}"\n'
        result += '\t\t}\n\t}\n'
    result += '}'
    return result

# Generate and format the output
lang_data = generate_lang_format(list_of_localizations)
formatted_output = format_custom_lang(lang_data)

# Print and save the output
print(formatted_output)

with open("lang_output.txt", "w", encoding="utf-8") as file:
    file.write(formatted_output)

 
def write_vdf_localizations(self,localized_data)
    self.get_language_from_locale()
    self.generate_lang_format()
    self.format_custom_lang