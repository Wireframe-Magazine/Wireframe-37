from Map_Generator import create_map
from tiles import *
from collections import namedtuple

## Dimensions of the tiles - change if neccessary
TILE_SIZE = 32

## Window Parameters // Viewport
SCREEN_WIDTH = 10
SCREEN_HEIGHT = 8

## Pygame Zero width and height for the game
WIDTH = SCREEN_WIDTH * TILE_SIZE
HEIGHT = SCREEN_HEIGHT * TILE_SIZE

## Set up world co-ordinates
## Top left corner of the screen
screen_pos = [0, 0]
## Player world co-ordinates
playerTile = [0, 0]

## Create the player Actor
player = Actor(player_image)

## Create the player variables
class Player:
    def __init__(self, actor, health, inventory):
        self.Actor = actor
        self.Health = health
        self.Inventory = inventory
    

    def Attack(self):
        global playerTile, Map
        for y in range(-1, 2):
            for x in range(-1, 2):
                check_x = playerTile[0] + x
                check_y = playerTile[1] + y
                if Map[check_x][check_y] == 4 or Map[check_x][check_y] == 5:
                    Map[check_x][check_y] = 1
                    break

player_object = Player(player, 100, {})


## Generate the first Map
Map = create_map()
## Search the Map for spawn positions
for x in range(len(Map)):
    for y in range(len(Map[0])):
        if Map[x][y] == 7:
            playerTile = [x, y]
            Map[x][y] = 1

def camera_follow():
    global screen_pos
    screen_pos[0] = playerTile[0] - (SCREEN_WIDTH//2)
    screen_pos[1] = playerTile[1] - (SCREEN_HEIGHT//2)

    if screen_pos[0] < 0: 
        screen_pos[0] = 0
    elif screen_pos[0] + SCREEN_WIDTH > len(Map):
        screen_pos[0] = len(Map)-SCREEN_WIDTH
    
    if screen_pos[1] < 0:
        screen_pos[1] = 0
    elif screen_pos[1] + SCREEN_HEIGHT > len(Map[0]):
        screen_pos[1] = len(Map[0])-SCREEN_HEIGHT

camera_follow()

def on_key_down(key):
    global playerTile
    if key == key.A :
        player_object.Attack()
    new_pos = [playerTile[0], playerTile[1]]
    if key == key.RIGHT:
        new_pos[0] += 1
    if key == key.LEFT:
        new_pos[0] -= 1
    if key == key.UP:
        new_pos[1] -= 1
    if key == key.DOWN:
        new_pos[1] += 1
    if movement_collision(new_pos) == True:
        playerTile[0] = new_pos[0]
        playerTile[1] = new_pos[1]
    camera_follow()

def movement_collision(position):
    global Map
    tile = Map[position[0]][position[1]]
    if tile == 1 or tile == 2 or tile == 3 or tile == 4:
        return True
    elif tile == 0:
        return False
    elif tile == 6:
        Map[position[0]][position[1]] = 1
        print("Gold!")

def draw_level():
    global player
    for i in range(SCREEN_WIDTH):
        for j in range(SCREEN_HEIGHT):
            x = screen_pos[0] + i
            y = screen_pos[1] + j
            if Map[x][y] == 0:
                screen.blit(dirt_tile, (i*32, j*32))
            elif Map[x][y] == 1:
                screen.blit(room_tile, (i*32, j*32))
            elif Map[x][y] == 2:
                screen.blit(south_corridor, (i*32, j*32))
            elif Map[x][y] == 3:
                screen.blit(north_corridor, (i*32, j*32))
            elif Map[x][y] == 4:
                screen.blit(room_tile, (i*32, j*32))
                screen.blit(enemy_basic, (i*32, j*32))
            elif Map[x][y] == 5:
                screen.blit(room_tile, (i*32, j*32))
                screen.blit(enemy_boss, (i*32, j*32))
            elif Map[x][y] == 6:
                screen.blit(room_tile, (i*32, j*32))
                screen.blit(chest, (i*32, j*32))
            elif Map[x][y] == 7:
                screen.blit(room_tile, (i*32, j*32))

            if x == playerTile[0] and y == playerTile[1]:
                player.x = i*32+player.width//2
                player.y = j*32+player.height//2

def draw():
    draw_level()
    player.draw()

