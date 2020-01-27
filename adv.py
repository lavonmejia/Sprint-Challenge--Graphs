from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
walk_graph = {}
todo = []
path_back = []
player_visited_rooms = (player.current_room.id,)
prior_steps = ((None, player.current_room.id),)

reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

def append_room(g, player):
    g.update({player.current_room.id: {i : '?' for i in player.current_room.get_exits()}})

def create_todos(player):
    for direction in player.current_room.get_exits():
        todo.append((player.current_room.id, direction))

create_todos(player)
append_room(walk_graph, player)

next_step = todo.pop()
while len(todo) != 0 or next_step is not None:
    
    if player.current_room.id == next_step[0]:
        if (player.current_room, player.current_room.get_room_in_direction(next_step[1]).id) not in prior_steps:
            walk_graph[player.current_room.id][next_step[1]] = player.current_room.get_room_in_direction(next_step[1]).id
            traversal_path.append(next_step[1])
            player.travel(next_step[1])
            path_back.append(reverse[next_step[1]])
            append_room(walk_graph, player)
        if player.current_room.id not in player_visited_rooms:
            for direction in player.current_room.get_exits():
                if direction != reverse[next_step[1]]:
                    todo.append((player.current_room.id, direction))
        if len(todo) == 0:
            next_step = None
        else:
            player_visited_rooms = (*player_visited_rooms, player.current_room.id)
            next_step = todo.pop()
    else:
        while player.current_room.id != next_step[0]:
            direction = path_back.pop()
            player.travel(direction)
            traversal_path.append(direction)



# carl, take the room you're in, find every exit and put each exit in your work queue, then take a direction, move in that direction, and put the opposite directin in your steps (you're going to have to keep track of your steps)
# ...go to the next room , get exits, auto populate the one you just came from, add then unknown exists to the stack queue, do that until you reach a room with no exits that are unknown, then move back until at room that has a valid option to explore


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
