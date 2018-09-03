# add cell by jiechen
import copy
import json
import numpy as np

output_dic = []
# input
img2Id_File = 'output/img2Id.json'
parent_id2cat = 'output/parent_id2cat.json'
parent_cat2id = 'output/parent_cat2id.json'
parent_File = 'output/parentList.json'
# output
outputResult_File = 'output/result.json'

def getTestJson(resultTxt):
    with open(resultTxt, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            res = [i.strip() for i in line.split(',')]
            with open(img2Id_File, 'r') as f:
                im_dic = json.load(f)
            with open(parent_cat2id, 'r') as f:
                cat2id = json.load(f)
            with open(parent_id2cat, 'r') as f:
                id2cat = json.load(f)
            with open(parent_File, 'r') as f:
                parentDic = json.load(f)
            im_name = res[0]
            bbox = [float(i) for i in res[1:5]]
            score = np.float64(round(float(res[5]), 10))
            classId = cat2id[res[6]]
            # do inference of image balabala
            # add original cell
            cell = {}
            cell['image_id'] = im_dic[im_name] # image id int
            cell['category_id'] = classId # category_id int
            cell['bbox'] = [bbox[0], bbox[1], \
                            bbox[2] - bbox[0], bbox[3] - bbox[1]]  # bbox [x, y, width, height]  (x, y) --> left top point
            cell['score'] = score
            output_dic.append(cell)
            # add parent cell
            ttt = id2cat[str(cell['category_id'])]
            for ele in parentDic[ttt]:
                tempCell = copy.deepcopy(cell)
                if not cat2id.has_key(ele): #
                    continue
                tempCell['category_id'] = cat2id[ele]
                output_dic.append(tempCell)
	    if (idx+1)%1000 == 0:
		print 'processed {} bboxes'.format(idx+1) 

    with open(outputResult_File, 'w') as f:
        f.write(json.dumps(output_dic))


