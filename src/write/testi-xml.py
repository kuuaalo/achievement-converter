# import the document class for creating XML documents
from xml.dom.minidom  import Document 

# define a dictionary to store achievement details
achievement = {
    "achievement1": "true",
    "status": "winner",
    "number": "100"
}

# create a new XML document
doc = Document ()

# create the root element 'achievement' for the XML document
root = doc.createElement ('achievement')
# add the root element to the document
doc.appendChild(root)

# loop through each key-value pair in the achievement dictionary
for key, value in achievement.items():
    item = doc.createElement(key) # create an XML element for each key

    item.appendChild(doc.createTextNode(value)) # add the value as a text node to the created element
    root.appendChild(item) # add the item element to the root element

# save the XML structure to a file named 'achievements.xml'
with open("achievements.xml", "w", encoding="utf-8") as f:
    f.write(doc.toprettyxml(indent=" "))

