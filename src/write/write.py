import xml.dom.minidom as minidom
import csv 
from tero import Tero

class Write:
    def __init__(self, file_name, file_format):
        if file_name:
            self.file_name = file_name  
        else:
            print("Wrong file name")
            return

        if file_format:
            self.file_format = file_format.lower()  # Set the file format to lowercase
        else:
            print("Wrong format")  # Print error if file format is invalid
            return

    def run(self):
        achievement_list = self.tero.get_achievements()
        
        # Sample data for achievements.
        # achievements = [
        #    {"Name": "Achievement1", "Status": "Completed"},
        #    {"Name": "Achievement2", "Status": "In Progress"},
        #    {"Name": "Achievement3", "Status": "Failed"}
        #]

        if self.file_format == "xml":
            self.write_to_xml(achievements)  # Write to XML if format is XML
        elif self.file_format == "csv":
            self.write_to_csv(achievements)  # Write to CSV if format is CSV
        else:
            print(f"Unsupported format: {self.file_format}")  # Print error for unsupported formats

    def write_to_xml(self, achievements):
        doc = minidom.Document()  # Create a new XML document
        root = doc.createElement('Achievements')  # Create the root element
        doc.appendChild(root)  # Append the root element to the document

        for achievement in achievements:
            ach_elem = doc.createElement('Achievement')  # Create an Achievement element

            name_elem = doc.createElement('Name')  # Create a Name element
            name_elem.appendChild(doc.createTextNode(achievement['Name']))
            ach_elem.appendChild(name_elem)  # Append the Name element to Achievement

            status_elem = doc.createElement('Status')  # Create a Status element
            status_elem.appendChild(doc.createTextNode(achievement['Status']))
            ach_elem.appendChild(status_elem)  # Append the Status element to Achievement

            root.appendChild(ach_elem)  # Append the Achievement element to the root

        xml_str = doc.toprettyxml(indent="  ")  # Convert the document to a pretty-printed XML string
        with open(self.file_name, "w") as f: 
            f.write(xml_str)  # Write the XML string to the file

        print(f"Data written to {self.file_name} in XML format.")  # Confirm the write operation

    def write_to_csv(self, achievements):
        # Using DictWriter to write to a CSV file
        with open(self.file_name, "w", newline='') as f:  # Open the file for writing with newline handling
            writer = csv.DictWriter(f, fieldnames=["Name", "Status"])  # Define field names for the CSV
            writer.writeheader()  # Write the header row
            writer.writerows(achievements)  # Write all rows from the achievements list

        print(f"Data written to {self.file_name} in CSV format.")  # Confirm the write operation

# Testing the Write class
if __name__ == "__main__":
    file_name = "achievements.csv"  # Change the file name to test CSV output
    file_format = "csv"  # Change the format to 'csv'

    writer = Write(file_name, file_format)  # Initialize the Write class
    writer.run()  # Execute the write process
