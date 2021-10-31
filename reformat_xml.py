import xml.dom.minidom as dom
from xml.dom import getDOMImplementation


# 将xml按照activity进行排序重新写入到文件中
def format_xml(xml_path):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'root', None)
    activities_data = {}

    DOMTree = dom.parse(xml_path)
    collection = DOMTree.documentElement
    activities = collection.getElementsByTagName("Activity")

    for activity in activities:
        activities_data[activity.attributes["name"].value] = activity

    activities_data = sorted(activities_data.items(), key=lambda x: x[0])

    for activity in activities_data:
        doc.firstChild.appendChild(activity[1])
    format_xml_path = str(xml_path)[:-4] + "_format.xml"
    fp = open(format_xml_path, "w", encoding="utf8")
    doc.writexml(fp)
    fp.close()


if __name__ == "__main__":
    format_xml("apk.xml")
    format_xml("res/base_apk.xml")
