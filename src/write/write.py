import xml.dom.minidom as minidom
import csv 
import vdf
from tero import tero

class Write:
    def __init__(self, file_name, file_format, tero):
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
        self.tero=tero
        
    def run(self):
        achievements = self.tero.get_achievements()
        
        if self.file_format == ".xml":
            self.write_to_xml(achievements) # Write to XML if format is XML
        elif self.file_format == ".csv":
            self.write_to_csv(achievements) # Write to CSV if format is CSV
        elif self.file_format == ".vdf":
            self.write_to_vdf(achievements) # Write to VDF if format is VDF
        else:
            print(f"Unsupported format: {self.file_format}")  # Print error for unsupported formats

    def write_to_xml(self, achievements):
        doc = minidom.Document()  # Create a new XML document
        root = doc.createElement('Achievements')  # Create the root element
        doc.appendChild(root)

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
        with open(self.file_name, "w", newline='') as f: 
            writer = csv.DictWriter(f, fieldnames=["Name", "Status"])  # Define field names for the CSV
            writer.writeheader()
            writer.writerows(achievements)  # Write all rows from the achievements list

        print(f"Data written to {self.file_name} in CSV format.")  # Confirm the write operation

    def write_to_vdf(self, achievements):
        # Prepare data in a format compatible with VDF
        vdf_data = {"Achievements": {str(i): ach for i, ach in enumerate(achievements)}} 
         # Convert dictionary to VDF format and write it
        with open(self.file_name, "w") as f:
            f.write(vdf.dumps(vdf_data, pretty=True)) # pretty=True adds indentations
        
        print(f"Data written to {self.file_name} in VDF format.")
    