        # Fetch the language name from locale code
    def get_language_from_locale(self, locale):
        for lang, code in self.languages.items():
            if code == locale:
                return lang
        return locale  # Return code if no match

    # Generate language format data
    def generate_lang_format(self, merged_data):
        output = {}
        for entry in merged_data:
            for locale, content in entry.items():
                if locale not in self.languages.values():
                    continue  # Skip if not a recognized locale

                # Get language name and initialize structure
                language = self.get_language_from_locale(locale)
                if language not in output:
                    output[language] = {"Tokens": {}}

                # Add tokens to the language
                tokens = output[language]["Tokens"]
                achievement_id = entry["name_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
                tokens[f"{achievement_id}_NAME"] = content.get("unlockedTitle", "")
                tokens[f"{achievement_id}_DESC"] = content.get("unlockedDescription", "")

        return output

    def write_to_vdf(self, merged_data):
        # Initialize an empty dictionary to hold the language-specific data
        output = {}

        # Iterate through the merged data
        for entry in merged_data:
            for locale, content in entry.items():
                # Skip if the locale is not a recognized language code
                if locale not in self.languages.values():
                    continue

                # Get the language from the locale
                language = self.get_language_from_locale(locale)
                
                # Initialize language structure if not already present
                if language not in output:
                    output[language] = {"Tokens": {}}

                # Add tokens for each achievement
                tokens = output[language]["Tokens"]
                achievement_id = entry["name_id"].replace("AchievementID", "NEW_ACHIEVEMENT_1_")
                tokens[f"{achievement_id}_NAME"] = content.get("unlockedTitle", "")
                tokens[f"{achievement_id}_DESC"] = content.get("unlockedDescription", "")

        # Start formatting the data into VDF style
        result = '"lang"\n{\n'

        for language, content in output.items():
            result += f'\t"{language}"\n\t{{\n'
            result += '\t\t"Tokens"\n\t\t{\n'

            for key, value in content["Tokens"].items():
                result += f'\t\t\t"{key}"\t"{value}"\n'

            result += '\t\t}\n\t}\n'

        result += '}'

        # Write the formatted VDF output to the specified file
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(result)

        print(f"Formatted language data written to {self.file_name}")