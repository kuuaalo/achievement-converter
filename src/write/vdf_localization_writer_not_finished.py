languages = {
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

#Hard coded example data, but matches blueprint so future data will look like this
blueprint_data = [
    {
        "achievement_id": "AchievementID1",
        "locale": "en-US",
        "locked_title": "Locked Achievement 1",
        "locked_description": "Locked Description of Achievement 1",
        "unlocked_title": "Achievement 1",
        "unlocked_description": "Description of Achievement 1",
    },
    {
        "achievement_id": "AchievementID1",
        "locale": "fi",
        "locked_title": "Lukittu Saavutus 1",
        "locked_description": "Lukittu Saavutus 1:en kuvaus",
        "unlocked_title": "Saavutus 1",
        "unlocked_description": "Saavutus 1:en kuvaus",
    },
    {
        "achievement_id": "AchievementID2",
        "locale": "en-US",
        "locked_title": "Locked Achievement 2",
        "locked_description": "Locked Description of Achievement 2",
        "unlocked_title": "Achievement 2",
        "unlocked_description": "Description of Achievement 2",
    },
    {
        "achievement_id": "AchievementID2",
        "locale": "fi",
        "locked_title": "Lukittu Saavutus 2",
        "locked_description": "Lukittu Saavutus 2:en kuvaus",
        "unlocked_title": "Saavutus 2",
        "unlocked_description": "Saavutus 2:en kuvaus",
    },
    {
        "achievement_id": "AchievementID3",
        "locale": "es-ES",
        "locked_title": "Logro bloqueado 1",
        "locked_description": "Descripción bloqueada del logro 1",
        "unlocked_title": "Logro 1",
        "unlocked_description": "Descripción del logro 1",
    },
    {
        "achievement_id": "AchievementID3",
        "locale": "de",
        "locked_title": "Gesperrte Auszeichnung 1",
        "locked_description": "Gesperrte Beschreibung der Auszeichnung 1",
        "unlocked_title": "Auszeichnung 1",
        "unlocked_description": "Beschreibung der Auszeichnung 1",
    },
    {
        "achievement_id": "AchievementID3",
        "locale": "fr",
        "locked_title": "Récompense verrouillée 1",
        "locked_description": "Description verrouillée de la récompense 1",
        "unlocked_title": "Récompense 1",
        "unlocked_description": "Description de la récompense 1",
    },
]

# fetch the lang and locale
def get_language_from_locale(locale):
    for lang, code in languages.items():
        if code == locale:
            return lang #return the language form
    return locale  # returning code to make sure

# generating language 
def generate_lang_format(blueprint_data):
    output = {}
    for entry in blueprint_data:
        locale = entry["locale"]
        language = get_language_from_locale(locale)  # to language from code
        
        if language not in output: # if its not there yet, do "language" and then "tokens"
            output[language] = {"Tokens": {}}
        
        tokens = output[language]["Tokens"] #then the info
        achievement_id = entry["achievement_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
        
        tokens[f"{achievement_id}_NAME"] = entry["unlocked_title"]
        tokens[f"{achievement_id}_DESC"] = entry["unlocked_description"]
    
    return output

# Formaatti haluttuun tulostusmuotoon
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

# Luo "lang"-muotoinen data vain käytetyille kielille
lang_data = generate_lang_format(blueprint_data)
formatted_output = format_custom_lang(lang_data)

# Tulosta tulos
print(formatted_output)

# Halutessasi tallentaa tiedostoon
with open("lang_output.txt", "w", encoding="utf-8") as file:
    file.write(formatted_output)