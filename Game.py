from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import raw_pb2 as raw_pb
from websocket import create_connection

def ping_pong(conn):
    #Make Request(RequestPing)
    req = sc_pb.Request(ping=sc_pb.RequestPing())
    #send Request
    conn.send(req.SerializeToString())
    #receive response
    response_str = conn.recv()
    #Parsing
    response = sc_pb.Response()
    response.ParseFromString(response_str)
    print(response)


"""Connect"""
conn = create_connection("ws://localhost:5000/sc2api", timeout=2 * 60)
print('Connected.')

"""Create Game"""
#Make Request(CreateGame)

map_info = sc_pb.LocalMap()
map_info.map_path = "C:\Program Files (x86)\StarCraft II\Maps\Melee\Simple128.SC2Map"

create_game = sc_pb.RequestCreateGame(local_map = map_info)
create_game.player_setup.add(type=1)
create_game.player_setup.add(type=2)


create_game.realtime = True

req = sc_pb.Request(create_game=create_game)

#send Request
conn.send(req.SerializeToString())
ping_pong(conn)


"""Join Game"""
#Make Requst(JoinGame)
interface_options = sc_pb.InterfaceOptions(raw = True, score = False)
join_game = sc_pb.RequestJoinGame(race = 3, options = interface_options)
req = sc_pb.Request(join_game = join_game)

#send Request
conn.send(req.SerializeToString())
ping_pong(conn)

#Game Start
req = sc_pb.Request(step = sc_pb.RequestStep(count = 1))
conn.send(req.SerializeToString())


"""Action"""
"""
unit_command = raw_pb.ActionRawUnitCommand()
unit_command.target_unit_tag = 1
unit_command.unit_tags.add(2)
unit_command.queue_command = False
action_raw = raw_pb.ActionRaw(unit_command = unit_command)

action = sc_pb.RequestAction()
action.actions.add(action_raw = action_raw)
req = sc_pb.Request(action = action)
"""

#send Request
conn.send(req.SerializeToString())
ping_pong(conn)

#conn.close()
