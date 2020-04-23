import Map_Generator

WIDTH = Map_Generator.WIDTH
HEIGHT = Map_Generator.HEIGHT

room_tile = "sprite_00.png"
south_corridor = "floor_1.png"
north_corridor = "floor_2.png"
dirt_tile = "dirt.png"
enemy_basic = "enemy_00.png"
enemy_boss = "enemy_01.png"
chest = "chest.png"

frame_count = 0
Map = Map_Generator.create_map()

def update():
    global frame_count, Map
    frame_count += 1
    if frame_count == 60:
        Map = Map_Generator.create_map()
        frame_count = 0

def draw():
    global Map
    for x in range(WIDTH//32):
        for y in range(HEIGHT//32):
            if Map[x][y] == 0:
                screen.blit(dirt_tile, (x*32, y*32))
            elif Map[x][y] == 1:
                screen.blit(room_tile, (x*32, y*32))
            elif Map[x][y] == 2:
                screen.blit(south_corridor, (x*32, y*32))
            elif Map[x][y] == 3:
                screen.blit(north_corridor, (x*32, y*32))
            elif Map[x][y] == 4:
                screen.blit(room_tile, (x*32, y*32))
                screen.blit(enemy_basic, (x*32, y*32))
            elif Map[x][y] == 5:
                screen.blit(room_tile, (x*32, y*32))
                screen.blit(enemy_boss, (x*32, y*32))
            elif Map[x][y] == 6:
                screen.blit(room_tile, (x*32, y*32))
                screen.blit(chest, (x*32, y*32))
            elif Map[x][y] == 7:
                screen.blit(room_tile, (x*32, y*32))