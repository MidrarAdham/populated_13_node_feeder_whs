import os
import json
import subprocess
import pandas as pd
from pprint import pprint as pp

# Setting up files path:

glm_path = '../glm/'
json_path = '../json/'
up_stream_objects = 'gld_basecase'
downstream_obj = 'downstream_objects'

# glm to json and vice-versa:

def convert_json_glm(glm_path, downstream_obj, json_path):
    p1 = subprocess.Popen(f'glm2json -p {glm_path}{downstream_obj}.glm >> {json_path}{downstream_obj}.json')
    p1.wait()

def convert_glm_json(glm_path, downstream_obj, json_path):
    p1 = subprocess.Popen(f'glm2json -p {glm_path}{downstream_obj}.glm >> {json_path}{downstream_obj}.json')
    p1.wait()

def setup_recorder_names(json_path, downstream_obj, glm_path):
    counter = 1
    multi_recorders = open(f'{glm_path}multi_recorders.glm','w')

    with open(f"{json_path}{downstream_obj}.json", "r") as file:
        data = json.load(file)
    
    index = [i for i in range(960)]
    power_prop = ["measured_real_power" for i in range(960)]
    meter_names = []
    recorders_property = []
    rec = ''
    for i in data['objects']:
        if 'name' in i['attributes']:
            if i['attributes']['name'].startswith('trip_node_meter'):
                meter_names.append(i['attributes']['name'])
    for i, names, pwr_prop in zip(index, meter_names, power_prop):
        rec = f'{names}:{pwr_prop}'
        recorders_property.append(rec)
    
    for i in range(0, len(recorders_property), 25):
        group = recorders_property[i: i+25]
        print(f"object multi_recorder {{\n\tinterval 60;\n\tproperty {' '.join(str(meters) for meters in group)};\n\tfile ./{glm_path}glm_output/meter_{counter}.csv;\n}}", file=multi_recorders)


def main(json_path, glm_path, up_stream_objects, downstream_obj):
    file_exists = os.path.isfile(f'{json_path}{downstream_obj}.json')
    if not file_exists:
        convert_json_glm(glm_path, downstream_obj, json_path)
    setup_recorder_names(json_path, downstream_obj, glm_path)
main(json_path, glm_path, up_stream_objects, downstream_obj)