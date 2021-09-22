import time
from math import sqrt
import pygame
from pygame.locals import *
import random

mazeLength, mazeWidth = 300, 300
maze = []

for y in range(mazeLength):
    mazeX = []
    for x in range(mazeWidth):
        if random.random() <= 0.4:
            mazeX.append(1)
        else:
            mazeX.append(0)
    maze.append(mazeX)



maze[1][1] = 10
maze[mazeLength-50][mazeWidth-100] = -1

# Press the green button in the gutter to run the script.


closed_set = []
old_paths = [(0, 0)]
current_path = []
splits = []


def determine_move(Xcur, Ycur, endPos):

    possible_moves = [(Xcur+1, Ycur), (Xcur-1, Ycur), (Xcur, Ycur+1), (Xcur, Ycur-1),(Xcur+1, Ycur+1),(Xcur+1, Ycur-1), (Xcur-1, Ycur-1),(Xcur-1, Ycur+1)]
    possible_moves += splits
    possible_paths = []
    next_move = {}



    total_travel = Xcur + Ycur

    for i in possible_moves:
        if not (0 <= i[-1] < mazeLength) or not (0 <= i[0] < mazeWidth):
            possible_moves.remove(i)

    for move in possible_moves:

        if move not in closed_set and maze[move[1]][move[0]] != 1 and move not in current_path:
            prediction = sqrt((endPos[0]-move[0])**2 + (endPos[1]-move[1])**2)

            possible_paths.append(prediction)
            next_move[prediction] = move

    if len(possible_paths) <= 0:
        for i in current_path:
            maze[i[1]][i[0]] = 5
            closed_set.append(i)
        closed_set.append((Xcur, Ycur))
        maze[Ycur][Xcur] = 5

        predictions = []
        reset_to = {}
        for resets in splits:
            prediction = sqrt((endPos[0] - resets[0]) ** 2 + (endPos[1] - resets[1]) ** 2)
            predictions.append(prediction)
            reset_to[prediction] = resets


        last_choice = reset_to[min(predictions)]
        splits.remove(last_choice)
        return last_choice


    elif len(possible_paths) >= 2:
        splits.append((Xcur, Ycur))


    for i in list(next_move.values()):
        if maze[i[1]][i[0]] == 0:
            maze[i[1]][i[0]] = 2


    current_path.append((Xcur, Ycur))

    return next_move[min(possible_paths)]


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width/2, height/2])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = (x*width)+width/4
        self.rect.y = (y*height)+height/4

    def move_to(self, x, y):
        x, y = round(x), round(y)
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height, = 1000, 1000
        self.tile_y = self.height / len(maze)
        self.tile_x = self.width / len(maze[0])
        self.walls = []

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.render_background()

    def render_background(self):
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                tile = maze[y][x]
                if tile == 1:
                    wallRect = Rect(x * self.tile_x, y * self.tile_y, self.tile_x, self.tile_y)
                    pygame.draw.rect(self._display_surf, (100, 100, 100), wallRect)
                    self.walls.append(wallRect)
                elif tile == -1:
                    self.endPos = (x, y)
                    self.goal = Rect(x * self.tile_x, y * self.tile_y, self.tile_x, self.tile_y)
                    pygame.draw.rect(self._display_surf, (0, 10, 100), self.goal)

                elif tile == 10:
                    self.x, self.y = x, y
                    maze[y][x] = 0
                    self.player = Player((0, 200, 100), self.tile_x, self.tile_y, x, y)
                    self.player.draw(self._display_surf)
                elif tile == 5:
                    pygame.draw.rect(self._display_surf, (255, 10, 10), Rect(x * self.tile_x, y * self.tile_y, self.tile_x, self.tile_y))
                elif tile == 'white':
                    pygame.draw.rect(self._display_surf, (110, 110, 0), Rect(x * self.tile_x, y * self.tile_y, self.tile_x, self.tile_y))
                elif tile == 2:
                    pygame.draw.rect(self._display_surf, (110, 0, 110),
                                     Rect(x * self.tile_x, y * self.tile_y, self.tile_x, self.tile_y))



    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):

        move_towards = determine_move(self.x, self.y, self.endPos)
        self.x, self.y = move_towards[0], move_towards[1]

        self.player.move_to(self.tile_x * self.x, self.tile_y * self.y)
        if pygame.Rect.collidelist(self.player.rect, self.walls) != -1:
            self.player.move_to(-self.tile_x / 2, 0)
        elif pygame.Rect.colliderect(self.player.rect, self.goal):
            self._running = False

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.render_background()
        self.player.draw(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pass

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()