import pygame
import random
black = (0,0,0)
red = (255,0,0)
dark_red = (122,0,0)
dark_green = (0,122,0)
green = (0,255,0)
background_color = black
tile_color = (122,122,122)
pygame.init()
tilesize = 60
rows = 10
columns = 10
amount_mines = 15
width, height = tilesize * rows, tilesize * columns
tile_font = pygame.font.SysFont('arial', tilesize)
end_screen_font = pygame.font.SysFont('arial', int(tilesize * columns / 5))
tile_number = rows * columns

# "?" = unknown
# "X" = mine

class Tile:
    def __init__(self, x, y, type, surrounding=0, revealed=False, flagged=False):
        self.x, self.y = x * tilesize, y * tilesize
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
        self.surrounding = surrounding
        self.text =tile_font.render(" ", False, black)

    def update(self):
        if self.flagged == True:
            self.text = tile_font.render("?", False, dark_red)
        elif self.revealed == True:
            if self.type == "0":
                self.text =tile_font.render(self.type, False, dark_green)
            else:
                self.text =tile_font.render(self.type, False, black)
        else:
            self.text =tile_font.render(" ", False, black)

    def dig(self):
        self.revealed = True
        self.update()

    def flag(self):
        self.flagged = not self.flagged
        self.update()
    
class Board:
    def __init__(self):
        self.board_surface = pygame.Surface((width, height))
        self.board_list = [[Tile(column, row, '0') for row in range(rows)] for column in range(columns)]
        self.tiles_left = rows*columns - amount_mines

    def place_mines(self, mx, my):
        for i in range(amount_mines):
            while True:
                x = random.randint(0, rows-1)
                y = random.randint(0, columns-1)
                if self.board_list[x][y].type == '0' and (abs(x-mx) > 2 or abs(y-mx) > 2):
                    self.board_list[x][y].type = 'X'
                    self.board_list[x][y].update()
                    break

    def check_neighbors(self, mx, my):   
        for x in range(rows):
            for y in range(columns):
                if not self.board_list[x][y].type == 'X':
                    if x>0:
                        if self.board_list[x-1][y].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                        if y > 0 and self.board_list[x-1][y-1].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                        if y < columns-1 and self.board_list[x-1][y+1].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                    if x < rows-1:
                        if self.board_list[x+1][y].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                        if y > 0 and self.board_list[x+1][y-1].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                        if y < columns-1 and self.board_list[x+1][y+1].type == 'X':
                            self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                            self.board_list[x][y].update()
                    if y>0 and self.board_list[x][y-1].type == 'X':
                        self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                        self.board_list[x][y].update()
                    if y<columns-1 and self.board_list[x][y+1].type == 'X':
                        self.board_list[x][y].type = str((int(self.board_list[x][y].type)+1))
                        self.board_list[x][y].update()
                self.board_list[x][y].update()

    def dig_multiple(self, mx, my):
        if self.board_list[mx][my].revealed == False and self.board_list[mx][my].flagged == False:
            self.board_list[mx][my].dig() 
            self.tiles_left-=1
            if self.board_list[mx][my].type == "0":
                if mx>0:
                    self.dig_multiple(mx-1,my)
                    if my>0:
                        self.dig_multiple(mx-1,my-1)
                    if my<columns-1:
                        self.dig_multiple(mx-1,my+1)
                if mx<rows-1:
                    self.dig_multiple(mx+1,my)
                    if my>0:
                        self.dig_multiple(mx+1,my-1)
                    if my<columns-1:
                        self.dig_multiple(mx+1,my+1)
                if my>0:
                    self.dig_multiple(mx,my-1)
                if my<columns-1:
                    self.dig_multiple(mx,my+1)


class Game: 
    def __init__(self):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper")
        Game.is_playing = True
        self.end_text = end_screen_font.render("YOU LOSE", False, red)
        self.first_Click = True

    def new(self):
        self.board = Board()

    def draw(self):
        self.display.fill(background_color)
        for x in range(rows):
            for y in range(columns):
                pygame.draw.rect(self.display, tile_color, [x*tilesize + 2, y*tilesize + 2, tilesize-4, tilesize-4])
                self.display.blit(self.board.board_list[x][y].text, (x*tilesize + tilesize*0.2, y*tilesize - tilesize *0.1))
        pygame.display.flip()
    
    def end_screen(self):
        if self.board.tiles_left == 0:
            self.end_text = end_screen_font.render("YOU WIN!", False, green)
        while True:
            self.display.blit(self.end_text, (5, height/3))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def run(self):
        while self.is_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    mx //= tilesize
                    my //= tilesize
                    if event.button == 1 and self.board.board_list[mx][my].revealed == False and self.board.board_list[mx][my].flagged == False:
                        if self.first_Click:
                            self.board.place_mines(mx,my)
                            self.board.check_neighbors(mx,my)
                        self.board.dig_multiple(mx,my)
                        if self.board.board_list[mx][my].type == 'X':
                            self.is_playing = False
                            self.board.tiles_left == 100
                        else: 
                            if self.board.tiles_left == 0:
                                self.is_playing = False
                    if event.button == 3 and self.board.board_list[mx][my].revealed == False:
                        self.board.board_list[mx][my].flag()
                    self.first_Click = False
                self.draw()
        else:
            self.end_screen()

game = Game()
game.new()
while True:
    game.run()