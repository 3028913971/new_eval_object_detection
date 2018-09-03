import json
import xml
import os


def readXML(xmlPath):
    # read xml file
    root = xml.dom.minidom.parse(xmlPath)

    # get picture size, object name && bndbox
    size = root.getElementsByTagName('size')
    width = size[0].getElementsByTagName('width')
    height = size[0].getElementsByTagName('height')
    w = width[0].childNodes[0].data
    h = height[0].childNodes[0].data
    #print(w, h)
    res = []
    objList = root.getElementsByTagName('object')
    for i in range(len(objList)):
        name = objList[i].getElementsByTagName('name')
        label = name[0].childNodes[0].data
        #print(label)

        bndbox = objList[i].getElementsByTagName('bndbox')
        xmin = bndbox[0].getElementsByTagName('xmin')
        xmax = bndbox[0].getElementsByTagName('xmax')
        ymin = bndbox[0].getElementsByTagName('ymin')
        ymax = bndbox[0].getElementsByTagName('ymax')

        xmin = xmin[0].childNodes[0].data
        xmax = xmax[0].childNodes[0].data
        ymin = ymin[0].childNodes[0].data
        ymax = ymax[0].childNodes[0].data
        #print(xmin, xmax, ymin, ymax)
        res.append([int(ymin), int(xmin), int(ymax), int(xmax), str(label)])
    return int(w), int(h), res

xmlPath = 'D:\\openImage_data\\test.txt'
dic = {}
with open("gtResult.json", 'r') as load_f:
    imgId_dict = json.load(load_f)
'''
for root, dirs, files in os.walk(xmlPath):
    for f in files:
        xmlp = xmlPath + '\\\\' + f
        w, h, res = readXML(xmlp)

'''
f = open(xmlPath, 'r')

for line in f.readlines():
    xmlp = 'D:\\openImage_data\\testXml'+'\\\\'+line+'.xml'

