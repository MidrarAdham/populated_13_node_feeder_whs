import re
import os
import json
import subprocess
import pandas as pd
from pprint import pprint as pp


class create_glm_objects():

    def __init__(self):
        
        # Paths:
        self.glm_path = '../glm/'
        self.json_path = '../json/'
        self.up_stream_objects = 'gld_basecase'
        self.downstream_obj = 'downstream_objects'
        
        # object multi recorder properties:
        self.recorder_time_resolution = 60
        self.property = "measured_real_power"
        self.recorders_file_name = 'multi_recorders.glm'

    # glm to json and vice-versa:
    def convert_json_glm(self):
        p1 = subprocess.Popen(f'json2glm -p {self.json_path}{self.downstream_obj}.json > {self.glm_path}{self.downstream_obj}.glm')
        p1.wait()

    def convert_glm_json(self):
        p1 = subprocess.Popen(f'glm2json -p {self.glm_path}{self.downstream_obj}.glm > {self.glm_path}{self.downstream_obj}.json')
        p1.wait()

    # Open recorder and glm files
    def open_recorders_file(self):
        with open(f"{self.json_path}{self.downstream_obj}.json", "r") as file:
            self.data = json.load(file)
        
        self.multi_recorders = open(f'{self.glm_path}{self.recorders_file_name}','w')
    
    # Pull meter object names to link to recorders
    def setup_recorder_names(self):
        self.node = []
        self.meter_names = []
        self.recorders_property = []
        for i in self.data['objects']:
            if 'name' in i['attributes']:
                if i['attributes']['name'].startswith('trip_node_meter'):
                    self.meter_names.append(i['attributes']['name'])

    # Get properties for multi-recorder objects
    def setup_recorder_properties(self):
        
        power_prop = [str(self.property) for i in range(960)]
        for names, pwr_prop in zip(self.meter_names, power_prop):
            rec = f'{names}:{pwr_prop}'
            self.recorders_property.append(rec)
        
        return self.recorders_property
    
    '''
    print multi-recorder objects to glm file.
    NOTE: GridLAB-D does not read more than 25 meters in one recorder objects. This number could be different from
    one OS to another. 
    '''

    def print_multi_recorders(self):
        counter = 1
        for i in range(0, len(self.recorders_property), 25):
            group = self.recorders_property[i: i+25]
            print(f"object multi_recorder {{\n\tinterval {self.recorder_time_resolution};\n\tproperty {','.join(str(meters) for meters in group)};\n\tfile ./{self.glm_path}glm_output/meter_{counter}.csv;\n}}", file=self.multi_recorders)
            counter +=1


if __name__== '__main__':
    glm_objects = create_glm_objects()
    extensions = ['json', 'glm']
    
    for extension in extensions:
        file_exists = os.path.isfile(f'{glm_objects.json_path}{glm_objects.downstream_obj}.{extension}')
        if 'json' == extension:
            if not file_exists:
                glm_objects.convert_json_glm()
        # else:
        #     if not file_exists:
        #         glm_objects.convert_glm_json()

    glm_objects.open_recorders_file()
    glm_objects.setup_recorder_names()
    glm_objects.setup_recorder_properties()
    glm_objects.print_multi_recorders()
    
