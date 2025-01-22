achievements = [
    {
        'name': 'Achievement 1',
        'name_finnish': 'Saavutus 1',
        'token_name': 'achievement1',
        'description': 'Description of Achievement 1',
        'description_finnish': 'Saavutus 1:en kuvaus',
        'token_desc': 'achievement1_desc',
        'hidden': 'TRUE',
        'icon': 'icon1',
        'icon_gray': 'icon1_gray'
    },
    {
        'name': 'Achievement 2',
        'name_finnish': 'Saavutus 2',
        'token_name': 'achievement2',
        'description': 'Description of Achievement 2',
        'description_finnish': 'Saavutus 2:en kuvaus',
        'token_desc': 'achievement2_desc',
        'hidden': 'FALSE',
        'icon': 'icon2',
        'icon_gray': 'icon2_gray'
    },
    {
        'name': 'Achievement 3',
        'name_finnish': 'Saavutus 3',
        'token_name': 'achievement3',
        'description': 'Description of Achievement 3',
        'description_finnish': 'Saavutus 3:en kuvaus',
        'token_desc': 'achievement3_desc',
        'hidden': 'TRUE',
        'icon': 'icon3',
        'icon_gray': 'icon3_gray'
    }
]

def write_to_vdf(achievements):
    # Start formatting the data into the desired VDF structure
    result = '"123456"\n{\n'
    result += '\t"stats"\n\t{\n'

    # Assuming achievements is a list of dictionaries with necessary data
    for i, achievement in enumerate(achievements, start=1):
        result += f'\t\t"{i}"\n\t\t{{\n'

        result += '\t\t\t"bits"\n\t\t\t{\n'

        result += f'\t\t\t\t"1"\n\t\t\t\t{{\n'  # Assuming there is only one bit per achievement

        result += f'\t\t\t\t\t"name"\t"AchievementID{i}"\n'
        
        # Create the "display" section with translations for name
        result += '\t\t\t\t\t"display"\n\t\t\t\t\t{\n'
        result += f'\t\t\t\t\t\t"name"\n\t\t\t\t\t\t{{\n'
        result += f'\t\t\t\t\t\t\t"english"\t"{achievement["name"]}"\n'
        result += f'\t\t\t\t\t\t\t"finnish"\t"{achievement["name_finnish"]}"\n'  # Example for Finnish translation
        result += f'\t\t\t\t\t\t\t"token"\t"{achievement["token_name"]}"\n'
        result += '\t\t\t\t\t\t}\n'  # End of name translations

        result += f'\t\t\t\t\t\t"desc"\n\t\t\t\t\t\t{{\n'
        result += f'\t\t\t\t\t\t\t"english"\t"{achievement["description"]}"\n'
        result += f'\t\t\t\t\t\t\t"finnish"\t"{achievement["description_finnish"]}"\n'  # Example for Finnish translation
        result += f'\t\t\t\t\t\t\t"token"\t"{achievement["token_desc"]}"\n'
        result += '\t\t\t\t\t\t}\n'  # End of desc translations

        result += f'\t\t\t\t\t"hidden"\t"{achievement["hidden"]}"\n'
        result += f'\t\t\t\t\t"icon"\t"{achievement["icon"]}"\n'
        result += f'\t\t\t\t\t"icon_gray"\t"{achievement["icon_gray"]}"\n'

        result += '\t\t\t\t}\n'  # End of bit 1
        result += '\t\t\t}\n'  # End of bits section
        result += '\t\t}\n'  # End of achievement entry

    result += '\t}\n'  # End of stats section
    result += '\t"type"\t"ACHIEVEMENTS"\n'
    result += '\t"version"\t"2"\n'
    result += '\t"gamename"\t"Super Ultimate Awesome Game"\n'
    result += '}\n'  # End of the main VDF block

    # Write the VDF formatted data to the file
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(result)

    print(f"Formatted achievement data written to {file_name}")
