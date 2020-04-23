# Importing modules
import secrets # Secrets is a crypto grade randomness library - in my opinion better than random for this.
import math # For the math
from collections import namedtuple
from pygame import Rect

WIDTH = 1024
HEIGHT = 768

# Map variables
TILE_SIZE = 32 # Dimensions of the tiles - change if neccessary
TILE_ACROSS = int(WIDTH/TILE_SIZE) # Use the previous variables to set a tile width
TILE_DOWN = int(HEIGHT/TILE_SIZE) # and tile height

MAX_ROOM_SIZE = 7
MIN_ROOM_SIZE = 3
ROOM_PADDING = 3

MAP_BORDER = 1

NUMBER_OF_ROOMS = 12

LOOT_ROOMS = 2

MAX_ENEMIES = NUMBER_OF_ROOMS*2

Room = namedtuple('Room', ['width', 'height', 'pos_x', 'pos_y'])

def generate_room():
    rm_width = MIN_ROOM_SIZE + secrets.randbelow(MAX_ROOM_SIZE - MIN_ROOM_SIZE + 1)
    rm_height = MIN_ROOM_SIZE + secrets.randbelow(MAX_ROOM_SIZE - MIN_ROOM_SIZE + 1)

    rm_pos_x = secrets.randbelow(TILE_ACROSS - rm_width)
    if rm_pos_x < MAP_BORDER:
        rm_pos_x = MAP_BORDER
    rm_pos_y = secrets.randbelow(TILE_DOWN - rm_height)
    if rm_pos_y < MAP_BORDER:
        rm_pos_y = MAP_BORDER

    return Room(rm_width, rm_height, rm_pos_x, rm_pos_y)

def create_rooms():
    Rooms = []
    for i in range(NUMBER_OF_ROOMS):
        intersect = True
        while intersect: 
            intersect = False
            rm = generate_room()
            for other in Rooms:
                room = other[0]
                padded_pos_x = rm.pos_x - 1
                padded_pos_y = rm.pos_y - 1
                padded_width = rm.width + 3
                padded_height = rm.height + 3
                rm_1 = Rect((room.pos_x*32, room.pos_y*32), (room.width*32, room.height*32))
                rm_2 = Rect((padded_pos_x*32, padded_pos_y*32), (padded_width*32, padded_height*32))
                if rm_1.colliderect(rm_2):
                    intersect = True
        Rooms.append([rm, {"NORTH": None, "SOUTH": None, "EAST": None, "WEST": None}])
    return Rooms

def create_corridors(rm, Rooms):
    candidates = {"NORTH": None, "SOUTH": None, "EAST": None, "WEST": None}
    for other in Rooms:
        if other[0] != rm[0]:
            current_room = rm[0]
            other_room = other[0]
            left_marker = max(current_room.pos_x, other_room.pos_x)
            right_marker = min(current_room.pos_x + current_room.width, other_room.pos_x + other_room.width)
            horizontal_overlap = list(range(left_marker, right_marker))
            if len(horizontal_overlap) > 0:
                vertical_corridors(candidates, other, rm, horizontal_overlap)
            top_marker = max(current_room.pos_y, other_room.pos_y)
            bottom_marker = min(current_room.pos_y + current_room.height, other_room.pos_y + other_room.height)
            vertical_overlap = list(range(top_marker, bottom_marker))
            if len(vertical_overlap) > 0:
                horizontal_corridors(candidates, other, rm, vertical_overlap)
    return candidates
                

def vertical_corridors(candidates, other, rm, horizontal_overlap):
    current_room = rm[0]
    current_connections = rm[1]
    other_room = other[0]
    other_connections = other[1]
    if current_room.pos_y > other_room.pos_y and other_connections["SOUTH"] == None and current_connections["NORTH"] != 0:
        connector = candidates["NORTH"]
        if connector == None:
            candidates["NORTH"] = (other, horizontal_overlap)
            other_connections["SOUTH"] = 0
        else:
            if other_room.pos_y + other_room.height > connector[0][0].pos_y + connector[0][0].height:
                connector[0][1]["SOUTH"] = None
                candidates["NORTH"] = (other, horizontal_overlap)
                other_connections["SOUTH"] = 0
    if current_room.pos_y < other_room.pos_y and other_connections["NORTH"] == None and current_connections["SOUTH"] != 0:
        connector = candidates["SOUTH"]
        if connector == None:
            candidates["SOUTH"] = (other, horizontal_overlap)
            other_connections["NORTH"] = 0
        else:
            if other_room.pos_y < connector[0][0].pos_y:
                connector[0][1]["NORTH"] = None
                candidates["SOUTH"] = (other, horizontal_overlap)
                other_connections["NORTH"] = 0

def horizontal_corridors(candidates, other, rm, vertical_overlap):
    current_room = rm[0]
    current_connections = rm[1]
    other_room = other[0]
    other_connections = other[1]
    if current_room.pos_x > other_room.pos_x and other_connections["EAST"] == None and current_connections["WEST"] != 0:
        connector = candidates["WEST"]
        if connector == None:
            candidates["WEST"] = (other, vertical_overlap)
            other_connections["EAST"] = 0
        else:
            if other_room.pos_x < connector[0][0].pos_x:
                connector[0][1]["EAST"] = None
                candidates["WEST"] = (other, vertical_overlap)
                other_connections["EAST"] = 0
    if current_room.pos_x < other_room.pos_x and other_connections["WEST"] == None and current_connections["EAST"] != 0:
        connector = candidates["EAST"]
        if connector == None:
            candidates["EAST"] = (other, vertical_overlap)
            other_connections["WEST"] = 0
        else:
            if other_room.pos_x + other_room.width < connector[0][0].pos_x + connector[0][0].width:
                connector[0][1]["WEST"] = None
                candidates["EAST"] = (other, vertical_overlap)
                other_connections["WEST"] = 0

def find_position(Room, Map):
    x_pos = Room.pos_x + secrets.randbelow(Room.width - 1)
    y_pos = Room.pos_y + secrets.randbelow(Room.height - 1)
    while Map[x_pos][y_pos] != 1:
        x_pos = Room.pos_x + secrets.randbelow(Room.width)
        y_pos = Room.pos_y + secrets.randbelow(Room.height)
    return x_pos, y_pos

def placeEnemies(Rooms, Map):
    for i in range(NUMBER_OF_ROOMS - LOOT_ROOMS):
        room = secrets.choice(Rooms)
        amount_of_enemies = secrets.randbelow(4)
        for enemy in range(amount_of_enemies):
            x_pos, y_pos = find_position(room[0], Map)
            Map[x_pos][y_pos] = 4
        chest_x_pos, chest_y_pos = find_position(room[0], Map)
        Map[chest_x_pos][chest_y_pos] = 6
        Rooms.remove(room)
    return Map

def placeBoss(boss_room, Map):
    x_pos = boss_room.pos_x + (boss_room.width//2)
    y_pos = boss_room.pos_y + (boss_room.height//2)

    Map[x_pos][y_pos] = 5

    boss_enemies = secrets.randbelow(4) + 1

    for henchman in range(boss_enemies):
        hench_x, hench_y = find_position(boss_room, Map)
        Map[hench_x][hench_y] = 4
    
    for chest in range(2):
        chest_x_pos, chest_y_pos = find_position(boss_room, Map)
        Map[chest_x_pos][chest_y_pos] = 6

    return Map

def placePlayer(room, Map):
    player_x, player_y = find_position(room, Map)
    Map[player_x][player_y] = 7
    return Map

def populateRooms(Rooms, Map):
    biggestArea = 0
    biggestRoom = ""
    smallestArea = math.inf
    smallestRoom = ""
    
    for rm in Rooms:
        area = rm[0].width * rm[0].height
        if area >= biggestArea:
            biggestArea = area
            biggestRoom = rm
        if area <= smallestArea:
            smallestArea = area
            smallestRoom = rm
    rooms_to_populate = Rooms
    rooms_to_populate.remove(biggestRoom)
    rooms_to_populate.remove(smallestRoom)

    Map = placeEnemies(rooms_to_populate, Map)
    
    boss_room = biggestRoom[0]
    Map = placeBoss(boss_room, Map)

    player_spawn = smallestRoom[0]
    Map = placePlayer(player_spawn, Map)
    return Map

def create_map():
    Map = []
    for x in range(TILE_ACROSS):
        row = []
        for y in range(TILE_DOWN):
            row.append(0)
        Map.append(row)
    Rooms = create_rooms()
    for rm in Rooms:
        for x in range(rm[0].width):
            for y in range(rm[0].height):
                Map[rm[0].pos_x+x][rm[0].pos_y+y] = 1
        rm[1] = create_corridors(rm, Rooms)
        #Create the corridors on the map array
        for key, value in rm[1].items():
            if len(rm[1].items()) > 1:
                skip = secrets.randbelow(100) # Chance to skip drawing this corridor
            else: 
                skip = 100
            if value is not None and value is not 0 and skip > 20:
                dir = [0, 0]
                start_pos = [rm[0].pos_x, rm[0].pos_y]
                end_pos = [value[0][0].pos_x, value[0][0].pos_y]
                mid_overlap = value[1][len(value[1])//2]
                if key == "NORTH":
                    dir[1] = -1
                    start_pos[0] = mid_overlap
                    start_pos[1] -= 1
                    end_pos[0] = mid_overlap
                    end_pos[1] += value[0][0].height
                    tile = 3
                elif key == "SOUTH":
                    dir[1] = 1
                    start_pos[0] = mid_overlap
                    start_pos[1] += rm[0].height
                    end_pos[0] = mid_overlap
                    end_pos[1] -= 1
                    tile = 3
                elif key == "EAST":
                    dir[0] = 1
                    start_pos[0] += rm[0].width
                    start_pos[1] = mid_overlap
                    end_pos[0] -= 1
                    end_pos[1] = mid_overlap
                    tile = 2
                elif key == "WEST":
                    dir[0] = -1
                    start_pos[0] -= 1
                    start_pos[1] = mid_overlap
                    end_pos[0] += value[0][0].width
                    end_pos[1] = mid_overlap
                    tile = 2
                Map[start_pos[0]][start_pos[1]] = tile
                Map[end_pos[0]][end_pos[1]] = tile 
                distance = (start_pos[0] - end_pos[0]) + (start_pos[1] - end_pos[1])
                next_pos = start_pos
                for i in range(abs(distance)):
                    next_pos = [next_pos[0] + dir[0], next_pos[1] + dir[1]]
                    if Map[next_pos[0]][next_pos[1]] == 0:
                        Map[next_pos[0]][next_pos[1]] = tile
    Map = populateRooms(Rooms, Map) 
    return Map
    