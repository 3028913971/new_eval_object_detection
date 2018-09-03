# New Evaluation on Object Detection
This is an implementation of evaluation on object detection. As is known to us all, clothing contains skirt, jacket, scarf and so on. Skirt contains miniskirt. 
Compared with traditional evaluation methods, we consider the parent-child relationship between categories, making the mAP more meaningful. And we display the AP of every category as well.
This repository includes:
- Utils to generate intermediate files
- Test examples
- Modified source code of [cocoapi](https://github.com/cocodataset/cocoapi)
# Getting Started
## 1. Install cocoapi
- For Matlab, add coco/MatlabApi to the Matlab path (OSX/Linux binaries provided)
- For Python, run "make" under coco/PythonAPI
- For Lua, run “luarocks make LuaAPI/rocks/coco-scm-1.rockspec” under coco/
## 2. Prepare files
- **Hierarchy file**: the parent-child relationship between categories. Example: data/bbox_labels_600_hierarchy.json
- **Class description file**(optional): mapping between category name and label. Example: data/class-descriptions.csv
- **Annotation directory**: containing the groud truth bounding box. Example: test_example/independent_relationship/annotation
- **Xml text**: contains the prefix of image's name to test. Example: test_example/independent_relationship/test.txt
- **test result**: the detection results of using your own model to test on evaluation dataset. Example: test_example/independent_relationship/result.txt
## 3. Run
python main.py
## 4. Output files
- analysis result
	- 0.50_all.csv
	- o.75_all.csv
	- 0.5:0.95_small.csv
	- 0.5:0.95_medium.csv
	- 0.5:0.95_large.csv
	- 0.5:0.95_all.csv
	
	

