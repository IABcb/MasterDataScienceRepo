import json
import os

'''
This script convert the string year into integer year
'''
source_dir = 'Data'
dest_dir = 'json_mod'
for file in os.listdir(source_dir):
    print(file)
    if file.endswith(".json"):
        print('@@@@@@@@@@@@@@@@@START@@@@@@@@@@@@@@@')
        source_file = open(source_dir+'/'+file, 'r')
        # print(file)
        dest_file = open(dest_dir+'/'+file.split('.')[0]+'_mod.json','w')

        for line in source_file:
            dict_line = json.loads(line)
            year = int(dict_line['year'])
            dict_line['year'] = year
            json.dump(dict_line, dest_file)
            dest_file.write('\n')
        print('@@@@@@@@@@@@@@@END@@@@@@@@@@@@@@@@@')
