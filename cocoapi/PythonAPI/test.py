import json


ff = open('D:\\openImage_data\\ImageSets\\Main\\test.txt', 'r')
dic = [{'name': 1}, {'name': 2}]
idx = 1
'''
for line in ff.readlines():
    line = line.strip()
    dic[line] = idx
    idx += 1
'''

with open('dict.json', 'w') as f:
    f.write(json.dumps(dic))

f.close()


'''
with open("temp.json", 'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict['e6e6c29e3af412df'])
'''