import utils.buildDic as bd
import utils.gt2json as gt2json
import utils.vis as vis
import cocoapi.PythonAPI.evaluation as eval

hierarchy_file = 'data/bbox_labels_600_hierarchy.json'
class_description_file = 'data/class-descriptions.csv'
AnnotationDir = 'test_example/parent_n2n/annotation'
xmlTxt = 'test_example/parent_n2n/test.txt'
resultTxt = 'test_example/parent_n2n/result.txt'

def main():
    bd.getParentList(hierarchy_file, class_description_file)
    print 'generate parentList done!'
    gt2json.buildGt(AnnotationDir, xmlTxt)
    print 'generate groud truth json done!'
    vis.getTestJson(resultTxt)
    print 'generate test result json done!'
    eval.evaluate()


if __name__ == '__main__':
    main()



