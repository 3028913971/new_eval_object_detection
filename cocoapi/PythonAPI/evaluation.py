import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

import numpy as np
import skimage.io as io
import pylab
gtJsonPath = 'output/parent_instances_minival2014.json'
resultJsonPath = 'output/result.json'

def evaluate():
    annType = ['segm','bbox','keypoints']
    annType = annType[1]      #specify type here
    print 'Running demo for *%s* results.'%(annType)

    #initialize COCO ground truth api
    annFile = gtJsonPath
    cocoGt=COCO(annFile)

    #initialize COCO detections api
    resFile = resultJsonPath
    cocoDt=cocoGt.loadRes(resFile)

    imgIds=sorted(cocoGt.getImgIds())

    # running evaluation
    cocoEval = COCOeval(cocoGt, cocoDt, annType)
    cocoEval.params.imgIds  = imgIds
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()
