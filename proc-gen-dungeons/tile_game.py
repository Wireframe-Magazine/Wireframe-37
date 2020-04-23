from Map_Generator import create_map
import pygame_gui

SCREEN_WIDTH = 10
SCREEN_HEIGHT = 8
TILE_SIZE = 32 # Dimensions of the tiles - change if neccessary

WIDTH = SCREEN_WIDTH * TILE_SIZE
HEIGHT = SCREEN_HEIGHT * TILE_SIZE

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

#gold_display = pygame_gui.elements.ui_text_box.UITextBox("Hello", relative_rect=Rect((WIDTH/4, HEIGHT/5), (10, 50)), manager=manager)

# Map variables

room_tile = "sprite_00.png"
south_corridor = "floor_1.png"
north_corridor = "floor_2.png"
dirt_tile = "dirt.png"
enemy_basic = "enemy_00.png"
enemy_boss = "enemy_01.png"
chest = "chest.png"
player_image = "player.png"

Map = create_map()

global screen_pos
global playerTile
screen_pos = [0, 0]
playerTile = [0, 0]
for x in range(len(Map)):
    for y in range(len(Map[0])):
        if Map[x][y] == 7:
            playerTile = [x, y]
            print(playerTile)

player = Actor(player_image)



def camera_follow():
    global screen_pos, player_Offset, player
    screen_pos[0] = playerTile[0] - (SCREEN_WIDTH//2)
    screen_pos[1] = playerTile[1] - (SCREEN_HEIGHT//2)

    if screen_pos[0] < 0: 
        screen_pos[0] = 0
        player_Offset[0] -= TILE_SIZE
    elif screen_pos[0] + SCREEN_WIDTH > len(Map):
        screen_pos[0] = len(Map)-SCREEN_WIDTH
    
    if screen_pos[1] < 0:
        screen_pos[1] = 0
    elif screen_pos[1] + SCREEN_HEIGHT > len(Map[0]):
        screen_pos[1] = len(Map[0])-SCREEN_HEIGHT

camera_follow()

def on_key_down(key):
    global playerTile
    new_pos = [playerTile[0], playerTile[1]]
    if key == key.RIGHT:
        new_pos[0] += 1
    if key == key.LEFT:
        new_pos[0] -= 1
    if key == key.UP:
        new_pos[1] -= 1
    if key == key.DOWN:
        new_pos[1] += 1
    if clamp_pos(new_pos) == True:
        playerTile[0] = new_pos[0]
        playerTile[1] = new_pos[1]
    camera_follow()

def clamp_pos(position):
    global Map
    tile = Map[position[0]][position[1]]
    print(tile)
    if tile == 1 or tile == 2 or tile == 3:
        return True
    elif tile == 0:
        return False

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
    manager.draw_ui(screen.surface)