import json
import xml
import os
import time
import xml.dom.minidom
import copy
xml.dom.minidom.parseString("<xml><item/></xml>")


trainJson = {}
testParentJson = {}

# input
img2Id_File = 'output/img2Id.json'
parent_File = 'output/parentList.json' # output from buildDic
id2Cat_File = 'output/id2Cat.json'
cat2Id_File = 'output/cat2Id.json'
testTxt_File = 'data/test.txt'
#xmlRoot = 'D:\\openImage_copy\\Annotations_rts_52'
#xmlTxt = 'D:\\openImage_copy\\ImageSets\\Main\\test.txt'

# output
output_parent_File = 'output/parent_instances_minival2014.json'
output_parent_id2cat = 'output/parent_id2cat.json'
output_parent_cat2id = 'output/parent_cat2id.json'

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

def getTxt(annotationDir):
    txtF = open(testTxt_File, 'w')
    for roots, dirs, files in os.walk(annotationDir):
        for f in files:
            txtF.write(f[:-4]+'\n')
    txtF.close()
    return testTxt_File

def getImg2Id(xmlTxt):
    img2Id = {}
    with open(xmlTxt, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            name = line.strip() + '.jpg'
            img2Id[name] = idx + 1
    f.close()
    with open(img2Id_File, 'w') as wf:
        wf.write(json.dumps(img2Id))
    wf.close()
    return img2Id

def getId2Cat(Annotation, xmlTxt):
    id2cat = {}
    cat2id = {}
    with open(xmlTxt, 'r') as f:
        for line in f.readlines():
            line = line.strip() + '.xml'
            w, h, res = readXML(os.path.join(Annotation, line))
            for i in range(len(res)):
                category = res[i][4]
                if not cat2id.has_key(category):
                    id = len(cat2id)+1
                    cat2id[category] = id
                    id2cat[id] = category
    f.close()
    with open(id2Cat_File, 'w') as wf:
        wf.write(json.dumps(id2cat))
    wf.close()
    with open(cat2Id_File, 'w') as wf:
        wf.write(json.dumps(cat2id))
    wf.close()
    return id2cat, cat2id

def buildGt(Annotation, xmlTxt=None):
    if not xmlTxt:
        xmlTxt = getTxt(Annotation)
    imgName2Id = getImg2Id(xmlTxt)
    with open(parent_File, 'r') as f:
        parentDic = json.load(f)
    f.close()
    id2cat, cat2id = getId2Cat(Annotation, xmlTxt)
    info = {"year": 2018, "version": 'v1.0', "description": 'for fun',
            "contributor": 'jiechen', "url": '', "date_created": '2018/7/9' }
    images = []
    annotations = []
    licenses = []
    categories = []
    # add images and categories info
    f = open(xmlTxt, 'r')
    annId = 1
    imgNum = 1
    for line in f.readlines():
        xmlp = os.path.join(Annotation, line.strip()) + '.xml'
        w, h, res = readXML(xmlp)
        imageCell = {}
        imageCell['id'] = imgName2Id[line.strip()+'.jpg']
        imageCell['width'] = w
        imageCell['height'] = h
        imageCell['file_name'] = line.strip() + '.jpg'
        imageCell['license'] = 1
        imageCell['flickr_url'] = ''
        imageCell['coco_url'] = ''
        imageCell['date_captured'] = time.asctime(time.localtime(time.time()))
        images.append(imageCell)
        for i in range(len(res)):
            annCell = {}
            annCell['id'] = annId
            annCell['image_id'] = imgName2Id[line.strip()+'.jpg']
            annCell['category_id'] = int(cat2id[res[i][4]])
            annCell['area'] = (res[i][2]-res[i][0])*(res[i][3]-res[i][1])
            annCell['bbox'] = [res[i][1], res[i][0], res[i][3]-res[i][1], res[i][2]-res[i][0]]
            annCell['iscrowd'] = 0
            annCell['segmentation'] = []
            seg = []
            seg.append(res[i][1])
            seg.append(res[i][0])
            seg.append(res[i][1])
            seg.append(res[i][2])
            seg.append(res[i][3])
            seg.append(res[i][2])
            seg.append(res[i][3])
            seg.append(res[i][0])
            annCell['segmentation'].append(seg)
            annotations.append(annCell)
            annId += 1
            ttt = res[i][4]
            for ele in parentDic[ttt]:
                if not cat2id.has_key(ele):
                    tempNum = len(cat2id.keys())+1
                    cat2id[ele] = tempNum
                    id2cat[tempNum] = ele
                tempCell = copy.deepcopy(annCell)
                tempCell['id'] = annId
                tempCell['category_id'] = int(cat2id[ele])
                annotations.append(tempCell)
                annId += 1
        if imgNum%100 == 0:
            print('processed image number: ' + str(imgNum))
        imgNum+=1

    # build category dictionary
    for key in id2cat:
        catCell = {}
        catCell['id'] = int(key)
        catCell['name'] = id2cat[key]
        catCell['supercategory'] = 'none'
        categories.append(catCell)

    liceCell = {}
    liceCell['id'] = 1
    liceCell['name'] = 'jiechen'
    liceCell['url'] = ''
    licenses.append(liceCell)

    testParentJson['info'] = info
    testParentJson['images'] = images
    testParentJson['annotations'] = annotations
    testParentJson['licenses'] = licenses
    testParentJson['categories'] = categories

    with open(output_parent_File, 'w') as f:
        f.write(json.dumps(testParentJson))
    f.close()
    with open(output_parent_id2cat, 'w') as f:
        f.write(json.dumps(id2cat))
    f.close()
    with open(output_parent_cat2id, 'w') as f:
        f.write(json.dumps(cat2id))
    f.close()

