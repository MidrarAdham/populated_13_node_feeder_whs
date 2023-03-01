import json
from pprint import pprint as pp

# with open ("../json/gld_basecase.json", 'r') as file:
#     data = json.load(file)

# houses = []
# tl_names = []
# tl_from = []
# to_tl = []
# phases = []
# config = []
# trip_node_phases = []
# trip_nodes = []
# for i in data['objects']:
#     attrib = i['attributes']
#     if 'name' in attrib:
#         if attrib['name'].startswith('house'):
#             houses.append(attrib['name'])
#         if attrib['name'].startswith('trip_line'):
#             tl_names.append(attrib['name'])
#             tl_from.append(attrib['from'])
#             to_tl.append(attrib['to'])
#             phases.append(attrib['phases'])
#             config.append(attrib['configuration'])
#         if attrib['name'].startswith('trip_node'):
#             trip_nodes.append(attrib['name'])
#             trip_node_phases.append(attrib['phases'])


# j = 0
# k = 0
# for i in range(len(houses)):
#     if j > int(960/len(trip_nodes)):
#         k += 1
#         j = 1
#     if 'A' in houses[i]:
#         print(f"object triplex_meter {{\n\tname trip_node_meter_{i};\n\tphases AS;\n\tnominal_voltage 120.0;\n}};")
#     if 'B' in houses[i]:
#         print(f"object triplex_meter {{\n\tname trip_node_meter_{i};\n\tphases BS;\n\tnominal_voltage 120.0;\n}};")
#     if 'C' in houses[i]:
#         print(f"object triplex_meter {{\n\tname trip_node_meter_{i};\n\tphases CS;\n\tnominal_voltage 120.0;\n}};")
#     j +=1


# j = 0
# k = 0
# for i in range(len(houses)):
#     if j > int(960/len(trip_nodes)):
#         k += 1
#         j = 1
#     if 'A' in tl_from[i]:
#         print(f"object triplex_line {{\n\tname {tl_names[i]};\n\tfrom {tl_from[i]};\n\tto trip_node_meter_{i};\n\tphases AS;\n\tlength 10;\n\tconfiguration {config[i]};\n}}\n")
#     if 'B' in tl_from[i]:
#         print(f"object triplex_line {{\n\tname {tl_names[i]};\n\tfrom {tl_from[i]};\n\tto trip_node_meter_{i};\n\tphases BS;\n\tlength 10;\n\tconfiguration {config[i]};\n}}\n")
#     if 'C' in tl_from[i]:
#         print(f"object triplex_line {{\n\tname {tl_names[i]};\n\tfrom {tl_from[i]};\n\tto trip_node_meter_{i};\n\tphases CS;\n\tlength 10;\n\tconfiguration {config[i]};\n}}\n")


# j = 0
# k = 0
# for i in range(len(houses)):
#     if j > int(960/len(trip_nodes)):
#         k += 1
#         j = 1
#     print(f"object house {{\n\tname {houses[i]};\n\tparent trip_node_meter_{i};\n}};\n")
#     j += 1


with open ("../json/downstream_objects.json", 'r') as file:
    data = json.load(file)

meter_names = []
for i in data['objects']:
    attrib = i['attributes']
    if 'name' in attrib:
        if attrib['name'].startswith('trip_node_meter'):
            meter_names.append(attrib['name'])

properties = []

for i in range(len(meter_names)):
    properties.append(f'{meter_names[i]}:measured_real_power,')


print(' '.join(str(i) for i in properties))