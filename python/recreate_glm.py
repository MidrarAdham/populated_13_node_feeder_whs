import re
import os
import json
from pprint import pprint as pp

def create_players():

    players =  open ("../glm/player_objects.glm","w")
    with open ("../json/gld_basecase.json", 'r') as file:
        data = json.load(file)
    counter = 1
    
    for i in data['objects']:
        if 'name' in i['attributes']:
            if i['attributes']['name'].startswith('wh_'):
                node = (re.findall(r'\d+',i['attributes']['name']))[0]
                print(f"object player {{\n\tname wd_{node}_{counter};\n\tfile '../wd_files/wd_{counter}.csv';\n}};",file=players)
                i['attributes']['water_demand'] = f"wd_{node}_{counter}.value"
                counter += 1
    return data


def wr_files(data):
    with open('gld_test_basecase.json','w') as f:
        json.dump(data,f, indent=4)
    os.system('json2glm -p gld_basecase.json > test.glm')

# def main():
#     data = create_players()
#     wr_files(data)
# main()

import gridlabd