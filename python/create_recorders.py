import re
import json
import subprocess
import pandas as pd
from pprint import pprint as pp


class create_glm_objects():

    def __init__(self):
        
        # Paths:
        self.glm_path = '../glm/'
        self.json_path = '../json/'
        self.downstream_obj = 'downstream_objects'  # GridLAB-D file name
        self.up_stream_objects = 'gld_basecase'     # GridLAB-D file name
        self.water_draw_profiles = '../wd_files/psu_feeder_output_profiles/'
        
        # object multi recorder properties:
        self.recorder_time_resolution = 60
        self.property = "measured_real_power"
        
        # Needed glm files
        self.recorders_file_name = 'multi_recorders.glm'
        self.player_objects_file_name = 'player_objects.glm'

        # Change the following to True if glm2json (or viceversa ) is needed 
        self.glm_json = {
            'False':'json2glm(self)',
            'False':'glm2json(self)'
        }

    def conversions(self):
        for key, value in self.glm_json.items():
            if key == 'True':
                eval(f"create_glm_objects.{value}")

    # glm to json and vice-versa:
    def json2glm(self):
        p1 = subprocess.Popen(f'json2glm -p {self.json_path}{self.downstream_obj}.json > {self.glm_path}{self.downstream_obj}.glm')
        p1.wait()

    def glm2json(self):
        p1 = subprocess.Popen(f'glm2json -p {self.glm_path}{self.downstream_obj}.glm > {self.glm_path}{self.downstream_obj}.json')
        p1.wait()

    # Open recorder and glm files
    def open_files(self):
        with open(f"{self.json_path}{self.downstream_obj}.json", "r") as file:
            self.downstream_obj = json.load(file)
        
        self.multi_recorders = open (f'{self.glm_path}{self.recorders_file_name}','w')
        self.player_objects = open (f'{self.glm_path}{self.player_objects_file_name}', 'w')

    
    # Pull meter object names to link to recorders
    def setup_recorder_names(self):
        self.node = []
        self.meter_names = []
        self.recorders_property = []
        for i in self.downstream_obj['objects']:
            if 'name' in i['attributes']:
                if i['attributes']['name'].startswith('trip_node_meter'):
                    self.meter_names.append(i['attributes']['name'])
                
                if i['attributes']['name'].startswith('wh_'):
                    self.node.append(re.findall(r'\d+',i['attributes']['name'])[0])
                    
    # Get properties for multi-recorder objects
    def setup_recorder_properties(self):
        
        power_prop = [str(self.property) for i in range(960)]
        for names, pwr_prop in zip(self.meter_names, power_prop):
            rec = f'{names}:{pwr_prop}'
            self.recorders_property.append(rec)
        
        return self.recorders_property
    
    '''
    print multi-recorder objects to glm file.
    NOTE: GridLAB-D does not read more than 25 meter objects in one multi-recorder object. This number 
    could be different from one OS to another. 
    '''

    def print_multi_recorders(self):
        counter = 1
        for i in range(0, len(self.recorders_property), 25):
            group = self.recorders_property[i: i+25]
            print(f"object multi_recorder {{\n\tinterval {self.recorder_time_resolution};\n\tproperty {','.join(str(meters) for meters in group)};\n\tfile ./{self.glm_path}glm_output/meter_{counter}.csv;\n}}", file=self.multi_recorders)
            counter +=1
    
    def print_player_objects(self):
        counter = 1
        for node in self.node:
            print(f"object player {{\n\tname wd_{node}_{counter};\n\tfile '{self.water_draw_profiles}wd_{counter}.csv';\n}};",file=f'{self.glm_path}{self.player_objects_file_name}')
            counter += 1


if __name__== '__main__':
    glm_objects = create_glm_objects()
    glm_objects.conversions()
    glm_objects.open_files()
    glm_objects.setup_recorder_names()
    glm_objects.setup_recorder_properties()
    glm_objects.print_multi_recorders()
    glm_objects.print_player_objects()
    
