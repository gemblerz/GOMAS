# How to Test
This document is about how to use sc2client-proto messages to write and run your program. Besides, This article is based on `protobuf` syntax.
If you wonder how to use it, [protobuf tutorial](https://developers.google.com/protocol-buffers/) will be helpful.

1. Launch SC2 with SC2Switcher. Set the port number 5000 to listen the message.
2. Write down your code. Before you read below lists, I recommend to see the hierarchy of sc2 protobuf msg.
    (Img of Hierarchy)
	1. Create Connection
		We have to connect with SC2. Using `websocket`, we can connect and send messages.
		```
			conn = websocket.create_connection("ws://%s:%s/sc2api" % (address, port), timeout=60)
		```
		Address would be `localhost`, and `host` could be any number. we used `127.0.0.1` for address, and `5000` for port.


	2. Create New Game
	    To create new game, we also need to request SC2 to make new game.
	    The following is the protobuf msg format of request to create game.
	    ```
	        message RequestCreateGame {
                oneof Map {
                    LocalMap local_map = 1;                         // Local .SC2Map file
                    string battlenet_map_name = 2;                  // Map published to BattleNet
                }

                repeated PlayerSetup player_setup = 3;

                optional bool disable_fog = 4;

                optional uint32 random_seed = 5;                  // Sets the pseudo-random seed for the game.
                optional bool realtime = 6;                       // If set, the game plays in real time.
            }
        ```

	    The sc2api require us the map info to make the new game. You can choose the way to give info of map which you want to use.
	    If you want to use your local map file, you need to fill the below structure.

	    ```
	        message LocalMap {
                // A map can be specified either by a file path or the data of the .SC2Map file.
                // If you provide both, it will play the game using map_data and store map_path
                // into the replay. (260 character max)
                optional string map_path = 1;
                optional bytes map_data = 7;
            }
        ```

        Also, you can setup the players with following msg.

        ```
            message PlayerSetup {
                optional PlayerType type = 1;

                // Only used for a computer player.
                optional Race race = 2;
                optional Difficulty difficulty = 3;
            }
        ```

	    Our example is below.

	    ```
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
	    ```

	3. Join to New Game

	    ```
	        interface_options = sc_pb.InterfaceOptions(raw = True, score = False)
            join_game = sc_pb.RequestJoinGame(race = 3, options = interface_options)

            #send Request
            test_client.comm.send(join_game=join_game)
            #print (test_client.comm.read())

            #Game Start
            print(test_client.comm.send(step = sc_pb.RequestStep(count = 1)))
            #print (test_client.comm.read())
	    ```
