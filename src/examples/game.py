from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as raw_pb
from s2clientprotocol import score_pb2 as score_pb

import sys
sys.path.append('../core')
from sc2_comm import sc2
from core import Core

"""Initialize"""
# Try to make a connection with SC2
test_client = Core()
test_client.init()

"""Create Game"""
#Make Request(CreateGame)


map_info = sc_pb.LocalMap()
#Windows
#map_info.map_path = "C:\Program Files (x86)\StarCraft II\Maps\Melee\Simple128.SC2Map"
#Mac
map_info.map_path = "/Applications/StarCraft II/Maps/Melee/Simple128.SC2Map"
create_game = sc_pb.RequestCreateGame(local_map = map_info)
create_game.player_setup.add(type=1)
create_game.player_setup.add(type=2)

create_game.realtime = True
print("Make")
#send Request
print(test_client.comm.send(create_game = create_game))
#print (test_client.comm.read())
"""Join Game"""
#Make Requst(JoinGame)

interface_options = sc_pb.InterfaceOptions(raw = True, score = True)
join_game = sc_pb.RequestJoinGame(race = 3, options = interface_options)

#send Request
test_client.comm.send(join_game=join_game)
#print (test_client.comm.read())

#Game Start
print(test_client.comm.send(step = sc_pb.RequestStep(count = 1)))
#print (test_client.comm.read())

#Get Data
"""

data = sc_pb.RequestData()
data.ability_id=True
data.unit_type_id=True
test_client.comm.send(data=data)
#print(test_client.comm.read())

"""

"""Action"""
"""
unit_tag_list=[]

observation = sc_pb.RequestObservation()
t=test_client.comm.send(observation=observation)

for unit in t.observation.observation.raw_data.units:
    if unit.unit_type == 84: # Probe unit_type_tag
        unit_tag_list.append(unit.tag)

unit_command = raw_pb.ActionRawUnitCommand()
unit_command.ability_id = 16 # Move Ability
unit_command.target_unit_tag = unit_tag_list[0]
unit_command.unit_tags.append(unit_tag_list[1])
action_raw = raw_pb.ActionRaw(unit_command = unit_command)

action = sc_pb.RequestAction()
action.actions.add(action_raw = action_raw)
test_client.comm.send(action=action)

"""

"""Move Units"""

"""
unit_tag_list=[]

observation = sc_pb.RequestObservation()
t=test_client.comm.send(observation=observation)

for unit in t.observation.observation.raw_data.units:
    if unit.unit_type == 84: # Probe unit_type_tag
        unit_tag_list.append(unit.tag)

unit_command = raw_pb.ActionRawUnitCommand()
unit_command.ability_id = 16 # Move Ability
unit_command.target_world_space_pos.x = 30
unit_command.target_world_space_pos.y = 30
for i in range(0,12):
    unit_command.unit_tags.append(unit_tag_list[i])
action_raw = raw_pb.ActionRaw(unit_command = unit_command)

action = sc_pb.RequestAction()
action.actions.add(action_raw = action_raw)
test_client.comm.send(action=action)

#conn.close()

"""

"""Gather Mules"""
unit_tag_list=[]
observation = sc_pb.RequestObservation()
t=test_client.comm.send(observation=observation)

for unit in t.observation.observation.raw_data.units:
    if unit.unit_type == 84: # Probe unit_type_tag
        unit_tag_list.append(unit.tag)

unit_command = raw_pb.ActionRawUnitCommand()
unit_command.ability_id = 166 # Gather Mule
action_raw = raw_pb.ActionRaw(unit_command = unit_command)

#12 units keep gettering mules until minerals are over 200
while True:

    #Ask keep going gether minerals
    action = sc_pb.RequestAction()
    action.actions.add(action_raw=action_raw)
    test_client.comm.send(action=action)

    #request information about collected_minerals
    get_mineral = test_client.comm.send(observation=observation)
    collected_minerals = get_mineral.observation.observation.score.score_details.collected_minerals
    print(collected_minerals)

    #if collected_minerals are over 200, all units is stop
    if collected_minerals >= 200:
        break

print ("Stop")
unit_command.ability_id = 4 # Stop Ability

for i in range(0,12):
    unit_command.unit_tags.append(unit_tag_list[i])

action_raw = raw_pb.ActionRaw(unit_command=unit_command)
action = sc_pb.RequestAction()
action.actions.add(action_raw=action_raw)
test_client.comm.send(action=action)


#conn.close()
