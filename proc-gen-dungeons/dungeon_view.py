import Map_Generator

WIDTH = Map_Generator.WIDTH
HEIGHT = Map_Generator.HEIGHT

room_tile = "sprite_00.png"
south_corridor = "sprite_00.png"
north_corridor = "sprite_00.png"
dirt_tile = "sprite_01.png"
enemy_basic = "henchman.png"
enemy_boss = "boss.png"
chest = "chest.png"
player_image = "player.png"

Map = Map_Generator.create_map()

def draw():
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
                screen.blit(player_image, (x*32, y*32))