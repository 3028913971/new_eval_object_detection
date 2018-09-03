import json

cellList = {}
finalList = {}


class_description_file = '../data/class-descriptions.csv'
labels_hierarchy_file = '../data/bbox_labels_600_hierarchy.json'
outputJson_file = 'output/parentList.json'

def getChar2Name(decripFile):
    char2Name = {}
    with open(decripFile, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            lineList = line.split(',')
            char2Name[lineList[0]] = lineList[1]
    return char2Name

def modifyName(cell, parent, char2Name, cellList, cls_des):
    #print cell['LabelName'].replace('"', '')
    if cell.has_key('LabelName'):
        if char2Name.has_key(cell['LabelName'].replace('"', '')) and cls_des:
            cell['LabelName'] = char2Name[cell['LabelName'].replace('"', '')]
            #print cell['LabelName']
        cell['parent'] = parent
        if not cellList.has_key(cell['LabelName']):
            cellList[cell['LabelName']] = []
            cellList[cell['LabelName']].append(cell['parent'])
        else:
            if cell['parent'] not in cellList[cell['LabelName']]:
                cellList[cell['LabelName']].append(cell['parent'])

    if cell.has_key('Subcategory'):
        for i in range(len(cell['Subcategory'])):
            modifyName(cell['Subcategory'][i], cell['LabelName'], char2Name, cellList, cls_des)

def findParent(key, node, tree):
    if tree[node][0] == 'hhh':
        return
    for i in range(len(tree[node])):
        finalList[key].append(tree[node][i])
        findParent(key, tree[node][i], tree)

def getParentList(hierarchy_file, cls_des=None):
    if cls_des:
        char2Name = getChar2Name(cls_des)
    with open(hierarchy_file, 'r') as load_f:
        dic = json.load(load_f)
    dic_copy = dic
    modifyName(dic_copy, 'hhh', char2Name, cellList, cls_des)
    for key in cellList:
        finalList[key] = []
        findParent(key, key, cellList)
        finalList[key] = list(set(finalList[key]))
    with open(outputJson_file, 'w') as f:
        f.write(json.dumps(finalList, indent=2))

    '''
    with open('new_dic.json', 'w') as new_f:
        new_f.write(json.dumps(dic_copy, indent=2))

    with open('singList_dic.json', 'w') as f2:
        f2.write(json.dumps(cellList, indent=2))
    with open(outputJson_file, 'w') as f:
        f.write(json.dumps(finalList, indent=2))
    '''

if __name__=="__main__":
    char2Name = getChar2Name(class_description_file)
    cellList = {}
    finalList = {}
    with open(labels_hierarchy_file, 'r') as load_f:
        dic = json.load(load_f)
    dic_copy = dic
    modifyName(dic_copy, 'hhh', char2Name, cellList)
    for key in cellList:
        finalList[key] = []
        findParent(key, key, cellList)
        finalList[key] = list(set(finalList[key]))
    '''
    with open('new_dic.json', 'w') as new_f:
        new_f.write(json.dumps(dic_copy, indent=2))

    with open('singList_dic.json', 'w') as f2:
        f2.write(json.dumps(cellList, indent=2))
    '''
    with open(outputJson_file, 'w') as f:
        f.write(json.dumps(finalList, indent=2))


