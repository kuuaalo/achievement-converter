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

list_of_localizations = [
    {
        "achievement_id": "AchievementID1",
        "localizations": [
            {
                "locale": "fr",
                "locked_title": "Récompense verrouillée 1",
                "locked_description": "Description verrouillée de la récompense 1",
                "unlocked_title": "Récompense 1",
                "unlocked_description": "Description de la récompense 1"
            },
            {
                "locale": "es-ES",
                "locked_title": "Logro bloqueado 1",
                "locked_description": "Descripción bloqueada del logro 1",
                "unlocked_title": "Logro 1",
                "unlocked_description": "Descripción del logro 1"
            }
        ]
    },
    {
        "achievement_id": "AchievementID2",
        "localizations": [
            {
                "locale": "en-US",
                "locked_title": "Locked Achievement 2",
                "locked_description": "Locked Description of Achievement 2",
                "unlocked_title": "Achievement 2",
                "unlocked_description": "Description of Achievement 2"
            }
        ]
    }
]

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