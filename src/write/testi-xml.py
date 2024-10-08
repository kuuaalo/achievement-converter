from xml.dom.minidom  import Document

achievement = {
    "achievement1": "true",
    "status": "winner",
    "number": "100"
}

# luo uuden tiedoston (XML)
doc = Document ()

root = doc.createElement ('achievement')
doc.appendChild(root)

for key, value in achievement.items():
    item = doc.createElement(key)

    item.appendChild(doc.createTextNode(value))
    root.appendChild(item)

#tallenna xml-tiedostoon
with open("achievements.xml", "w", encoding="utf-8") as f:
    f.write(doc.toprettyxml(indent=" "))

