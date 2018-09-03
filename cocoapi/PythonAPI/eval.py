import xml

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
from utils import label_map_util
from utils import visualization_utils as vis_util
import cv2
import json


from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

sys.path.append("..")
PATH_TO_CKPT = 'C:\\Users\\t-jiec\PycharmProjects\ObjDecVideo\\frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'oid_bbox_trainable_label_map.pbtxt')
NUM_CLASSES = 545


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
  print('init model done')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
print('label map done')
#print (category_index)

#print (category_index[1]['name'])
#print (category_index[3]['name'])

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def readXML(xmlPath):
    # read xml file
    root = xml.dom.minidom.parse(xmlPath)

    # get picture size, object name && bndbox
    size = root.getElementsByTagName('size')
    width = size[0].getElementsByTagName('width')
    height = size[0].getElementsByTagName('height')
    w = width[0].childNodes[0].data
    h = height[0].childNodes[0].data
    print(w, h)
    res = []
    objList = root.getElementsByTagName('object')
    for i in range(len(objList)):
        name = objList[i].getElementsByTagName('name')
        label = name[0].childNodes[0].data
        print(label)

        bndbox = objList[i].getElementsByTagName('bndbox')
        xmin = bndbox[0].getElementsByTagName('xmin')
        xmax = bndbox[0].getElementsByTagName('xmax')
        ymin = bndbox[0].getElementsByTagName('ymin')
        ymax = bndbox[0].getElementsByTagName('ymax')

        xmin = xmin[0].childNodes[0].data
        xmax = xmax[0].childNodes[0].data
        ymin = ymin[0].childNodes[0].data
        ymax = ymax[0].childNodes[0].data
        print(xmin, xmax, ymin, ymax)
        res.append([int(ymin), int(xmin), int(ymax), int(xmax), str(label)])
    return int(w), int(h), res

def getIoU(bbox, gtbox):
    up = max(bbox[0], gtbox[0])
    left = max(bbox[1], gtbox[1])
    down = min(bbox[2], gtbox[2])
    right = min(bbox[3], gtbox[3])

    if (down>up and right>left):
        return (down-up)*(right-left)*1.0/((bbox[2]-bbox[0])*(bbox[3]-bbox[1])+(gtbox[2]-gtbox[0])*(gtbox[3]-gtbox[1])-(down-up)*(right-left))
    else:
        return 0

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    testFile = 'D:\\openImage_data\\ImageSets\\Main\\test2.txt'
    imgPath = 'D:\\openImage_data\\JPEGImages'
    count = 1
    dic = []
    with open("dict.json", 'r') as load_f:
        imgId_dict = json.load(load_f)
    with detection_graph.as_default():
        # detection_graph.finalize()
        with tf.Session(graph=detection_graph) as sess:
            testFileName = open(testFile, 'r')
            for line in testFileName.readlines():
                imgName = line.strip() + '.jpg'
                print (imgName)
                # get prediction
                image = cv2.imread(imgPath+'\\\\'+imgName)
                image_np = np.array(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                start_time = time.time()
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                end_time = time.time()
                print('image number: ' + str(count) + '  use time:  ' + str(end_time - start_time) + '  s')
                boxes = np.squeeze(boxes)
                scores = np.squeeze(scores)
                classes = np.squeeze(classes)
                for i in range(len(num_detections[0])):
                    cell = {}
                    cell['image_id'] = imgId_dict[line.strip()]
                    cell['category_id'] = classes[i]
                    cell['bbox'] = [boxes[i][1], boxes[i][0], boxes[3]-boxes[1], boxes[2]-boxes[0]]
                    cell['score'] = scores[i]
                    dic.append(cell)
                '''
                w, h, gt = readXML(xmlPath+'\\\\'+imgName[:-4]+'.xml')
                # count gt class number
                for i in range(len(gt)):
                    if gt[i][-1] in gtCount:
                        gtCount[gt[i][-1]] += 1
                    else:
                        gtCount[gt[i][-1]] = 1
                # calculate IoU
                for i in range(int(num_detections[0])):
                    if scores[i] < scorethreshold:
                        continue
                    bbox = boxes[i]
                    for i in range(4):
                        if i%2 == 0:
                            bbox[i] *= h
                        else:
                            bbox[i] *= w
                    if classes[i] in category_index:
                        label = category_index[classes[i]]['name']
                    else:
                        label = 'Dress'
                    # count dt class number
                    if label in dtCount:
                        dtCount[label] += 1
                    else:
                        dtCount[label] = 1
                    # count dt right class number
                    for j in range(len(gt)):
                        gtBox = gt[j][:-1]
                        if getIoU(bbox, gtBox) >= 0.5 and label == gt[j][-1]:
                            #print ('label: ' + label)
                            if label in dtRightCount5:
                                dtRightCount5[label] += 1
                            else:
                                dtRightCount5[label] = 1
                            break
                    for j in range(len(gt)):
                        gtBox = gt[j][:-1]
                        if getIoU(bbox, gtBox) >= 0.75 and label == gt[j][-1]:
                            #print ('label: ' + label)
                            if label in dtRightCount75:
                                dtRightCount75[label] += 1
                            else:
                                dtRightCount75[label] = 1
                            break
                '''
                del boxes
                del scores
                del classes
                del num_detections
                count += 1
            testFileName.close()

    with open('testResult.json', 'w') as f:
        f.write(json.dumps(dic))
    f.close()

if  __name__ == "__main__":
    main()
