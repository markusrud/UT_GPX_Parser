GPX_file = "ut-no_kalhovd-turisthytte.gpx"
Type = "DNT"
Stafftype = "Betjent"
Beds = 10
Area = "Hardangervidda"
Lock = "Åpen"
Season = "2. jun til 10. aug"

#TODOs
# - Load GPX file from file location
# - Use data from cabins GPX file
# - Load excel file
# - Use data from Excel
# - - Serach after filename and find correct row for the data
# - Iterate over all files in the folder

from xml.dom import minidom
from xml.etree import cElementTree as ET
import datetime
import os, glob

def createHeaderData(root):
    xml = root.createElement('gpx') 
    xml.setAttribute('creator', 'Garmin Desktop App')
    xml.setAttribute('version', '1.1')
    xml.setAttribute('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/ActivityExtension/v1 http://www8.garmin.com/xmlschemas/ActivityExtensionv1.xsd http://www.garmin.com/xmlschemas/AdventuresExtensions/v1 http://www8.garmin.com/xmlschemas/AdventuresExtensionv1.xsd http://www.garmin.com/xmlschemas/PressureExtension/v1 http://www.garmin.com/xmlschemas/PressureExtensionv1.xsd http://www.garmin.com/xmlschemas/TripExtensions/v1 http://www.garmin.com/xmlschemas/TripExtensionsv1.xsd http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1 http://www.garmin.com/xmlschemas/TripMetaDataExtensionsv1.xsd http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1 http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensionsv1.xsd http://www.garmin.com/xmlschemas/CreationTimeExtension/v1 http://www.garmin.com/xmlschemas/CreationTimeExtensionsv1.xsd http://www.garmin.com/xmlschemas/AccelerationExtension/v1 http://www.garmin.com/xmlschemas/AccelerationExtensionv1.xsd http://www.garmin.com/xmlschemas/PowerExtension/v1 http://www.garmin.com/xmlschemas/PowerExtensionv1.xsd http://www.garmin.com/xmlschemas/VideoExtension/v1 http://www.garmin.com/xmlschemas/VideoExtensionv1.xsd')
    xml.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')
    xml.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    xml.setAttribute('xmlns:wptx1', 'http://www.garmin.com/xmlschemas/WaypointExtension/v1')
    xml.setAttribute('xmlns:gpxtrx', 'http://www.garmin.com/xmlschemas/GpxExtensions/v3')
    xml.setAttribute('xmlns:gpxtpx', 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1')
    xml.setAttribute('xmlns:gpxx', 'http://www.garmin.com/xmlschemas/GpxExtensions/v3')
    xml.setAttribute('xmlns:trp', 'http://www.garmin.com/xmlschemas/TripExtensions/v1')
    xml.setAttribute('xmlns:adv', 'http://www.garmin.com/xmlschemas/AdventuresExtensions/v1')
    xml.setAttribute('xmlns:prs', 'http://www.garmin.com/xmlschemas/PressureExtension/v1')
    xml.setAttribute('xmlns:tmd', 'http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1')
    xml.setAttribute('xmlns:vptm', 'http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1')
    xml.setAttribute('xmlns:ctx', 'http://www.garmin.com/xmlschemas/CreationTimeExtension/v1')
    xml.setAttribute('xmlns:gpxacc', 'http://www.garmin.com/xmlschemas/AccelerationExtension/v1')
    xml.setAttribute('xmlns:gpxpx', 'http://www.garmin.com/xmlschemas/PowerExtension/v1')
    xml.setAttribute('xmlns:vidx1', 'http://www.garmin.com/xmlschemas/VideoExtension/v1')
    root.appendChild(xml)
    return xml

def createLevel(root, levelName, appenTo):
    level = root.createElement(levelName)  
    appenTo.appendChild(level)
    return level

def createElementAndAppend(root, elementName, elementText, appendTo):
    elementHeader = root.createElement(elementName)
    txt = root.createTextNode(elementText)  
    elementHeader.appendChild(txt) 
    appendTo.appendChild(elementHeader)


#def parserloop(level):


def main():
    root = minidom.Document()
    xml = createHeaderData(root)
   
    for filename in glob.glob(os.path.join('GPX_from_UT/', '*.gpx')):
        name = ""
        link = ""
        lat = 0
        lon = 0

        #with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        tree = ET.parse(filename)
        for elem in tree.iter():
            #print("Tag:", elem.tag, "Attr", elem.attrib, "Text:", elem.text)
            if(elem.tag.find("name") != -1):
                name = elem.text
            if(elem.tag.find("link") != -1):
                link = elem.get("href")
            if(elem.tag.find("wpt") != -1):
                lat = elem.get("lat")
                lon = elem.get("lon")

    wpt = root.createElement('wpt')
    wpt.setAttribute('lat', lat)
    wpt.setAttribute('lon', lon)
    xml.appendChild(wpt)

    now = datetime.datetime.now()
    createElementAndAppend(root, "time", str(now.strftime("%Y-%m-%dT%H:%M:%SZ")), wpt)
    createElementAndAppend(root, "name", name, wpt)
    createElementAndAppend(root, "cmt", "testdesc", wpt)
    createElementAndAppend(root, "desc", "testdesc", wpt)

    x = root.createElement('link')
    x.setAttribute('href', link)
    wpt.appendChild(x)

    createElementAndAppend(root, "sym", "Lodge", wpt)
    createElementAndAppend(root, "type", "user", wpt)

    extensions= createLevel(root, "extensions", wpt)
    gpxx_ext= createLevel(root, "gpxx:WaypointExtension", extensions)

    createElementAndAppend(root, "gpxx:DisplayMode", "SymbolAndName", gpxx_ext)

    gpxx_cat= createLevel(root, "gpxx:Categories", gpxx_ext)

    createElementAndAppend(root, "gpxx:Category", "Hardangervidda", gpxx_cat)
    createElementAndAppend(root, "gpxx:Category", "Betjent", gpxx_cat)

    wptx1_ext= createLevel(root, "wptx1:WaypointExtension", extensions)

    createElementAndAppend(root, "wptx1:DisplayMode", "SymbolAndName", wptx1_ext)

    wptx1_cat= createLevel(root, "wptx1:Categories", wptx1_ext)

    createElementAndAppend(root, "wptx1:Category", "Hardangervidda", wptx1_cat)
    createElementAndAppend(root, "wptx1:Category", "Betjent", wptx1_cat)

    ctx_ext= createLevel(root, "ctx:CreationTimeExtension", extensions)

    createElementAndAppend(root, "ctx:CreationTime", str(now.strftime("%Y-%m-%dT%H:%M:%SZ")), ctx_ext)

    xml_str = root.toprettyxml(indent ="\t") 
    
    save_path_file = "testfile.gpx"
    print("Hello2")
    
    with open(save_path_file, "w") as f:
        f.write(xml_str) 




if __name__ == "__main__":
    main()
  
