'''
 This module handles loading maps for game2.py and it defines the map structure.
 The map grid contains integers, and each integer defines a tile type.

 Author: Andrew Frank

'''

'''
A two dimensional grid to hold map data
'''
#TODO change grid to contain cell objects
class MapGrid:
    width = 0
    height = 0
    grid = []
    player = None
    guards = []
    turn = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        out = ""
        for row in self.grid:
            out = out + ''.join(str(e) for e in row) + '\n'
        return out

    def AddRow(self, row):
        self.grid.append(row)

    def AddGuard(self, guard):
        self.guards.append(guard)


'''
Standard cell to fill the map space with
'''
class Cell:
    x = None
    y = None
    color = "#000000"

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "0"

    def can_walk(self, player):
        return False

    def collide(self, player):
        return

    def draw(self, renderer):
        renderer.draw_pixel(self.color)
        return

'''
 The cell containing the keys
'''
class KeyCell(Cell):   

    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        self.color = "#ffd700"

    def __str__(self):
        return "8"

    def collide(self, player):
        player.hasKey = True
        player.game.grid[self.y][self.x] = PathCell(self.x, self.y)

    def can_walk(self, player):
        return True

    def draw(self, renderer):
        xcor = float(renderer.pen.xcor())
        ycor = float(renderer.pen.ycor())

        renderer.draw_pixel("#b5651d")
        renderer.pen.up()
        renderer.pen.setx(xcor + renderer.pixel_size/8)
        renderer.pen.sety(ycor - renderer.pixel_size/3)
        renderer.pen.down()
        renderer.pen.fillcolor(self.color)
        renderer.pen.begin_fill()
        renderer.pen.forward(renderer.pixel_size/2)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/6)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.left(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.left(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/12)
        renderer.pen.left(90)
        renderer.pen.forward(renderer.pixel_size/4)
        renderer.pen.end_fill()

        renderer.pen.setheading(0)
        renderer.pen.up()
        renderer.pen.setx(xcor)
        renderer.pen.sety(ycor)
        renderer.pen.down()
        return

'''
 The cell that is the door
'''
class DoorCell(Cell):
        
    def __init__(self, x, y):
        Cell.__init__(self, x, y)

    def __str__(self):
        return "9"

    def can_walk(self, player):
        return player.hasKey

    def collide(self, player):
        player.hasWon = True

    def draw(self, renderer):
        xcor = float(renderer.pen.xcor())
        ycor = float(renderer.pen.ycor())

        renderer.draw_pixel("#85350d")
        renderer.pen.up()
        renderer.pen.setx(xcor + (7 * (renderer.pixel_size/8)))
        renderer.pen.sety(ycor - (7 * (renderer.pixel_size/16)))
        renderer.pen.down()

        renderer.pen.fillcolor("#ffd700")
        renderer.pen.begin_fill()
        renderer.pen.forward(renderer.pixel_size/16)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/16)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/16)
        renderer.pen.right(90)
        renderer.pen.forward(renderer.pixel_size/16)
        renderer.pen.end_fill()

        renderer.pen.setheading(0)
        renderer.pen.up()
        renderer.pen.setx(xcor)
        renderer.pen.sety(ycor)
        renderer.pen.down()
        return 

'''
This defines player cell and actions
'''
class Player(Cell):
    hasKey = False
    hasWon = False
    hasLost = False
    isTired = False
    game = None

    def __init__(self, x, y, game):
        Cell.__init__(self, x, y)
        self.color = "#ffd700"
        self.game = game
    
    def __str__(self):
        return "5"

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def right(self):
        self.x += 1

    def left(self):
        self.x -= 1

    def SetKey(self, state):
        self.hasKey = state

    def draw(self, renderer):        
        leftMargin = (abs(self.x - abs(renderer.frame[0]))) * renderer.pixel_size
        bottomMargin = (renderer.frame[3] - self.y) * renderer.pixel_size
        xPos = -renderer.screen.canvwidth/2 + leftMargin
        yPos = -renderer.screen.canvheight/2 + bottomMargin        
        
        renderer.pen.up()
        renderer.pen.setpos(xPos + renderer.pixel_size/2, yPos)
        renderer.pen.down()        

        renderer.pen.fillcolor(self.color)
        renderer.pen.begin_fill()
        renderer.pen.circle(renderer.pixel_size/3)
        renderer.pen.end_fill()
        return 

'''
A grid representation of a path space
'''
class PathCell(Cell):

    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        self.color = "#b5651d"
    
    def __str__(self):
        return "1"

    def can_walk(self, player):
        return True


'''
Representation of a guard as a cell
'''
class Guard(Cell):
    speed = None
    active = 0

    def __init__(self, x, y, speed):
        Cell.__init__(self, x, y)
        self.speed = speed
        self.color = "#ff0000"

    def __str__(self):
        return "3"

    def collide(self, player):     
        player.hasLost = True

    def move(self, player):
        if(self.x == player.x and self.y == player.y):
            return
        if abs(player.x - self.x) > abs(player.y - self.y):
            if player.x > self.x:
                target = player.game.grid[self.y][self.x + 1]                
                if target.can_walk(player):
                    self.x += 1
            else:
                target = player.game.grid[self.y][self.x - 1]                
                if target.can_walk(player):
                    self.x -= 1
            return
        # if first branch checked, will return
        # otherwise also check second case
        if player.y > self.y:
            target = player.game.grid[self.y + 1][self.x]                
            if target.can_walk(player):
                self.y += 1
        else:
            target = player.game.grid[self.y - 1][self.x]                
            if target.can_walk(player):
                self.y -= 1
        return

    def draw(self, renderer):        
        leftMargin = (abs(self.x - abs(renderer.frame[0]))) * renderer.pixel_size
        bottomMargin = (renderer.frame[3] - self.y) * renderer.pixel_size
        xPos = -renderer.screen.canvwidth/2 + leftMargin
        yPos = -renderer.screen.canvheight/2 + bottomMargin        
        
        renderer.pen.up()
        renderer.pen.setpos(xPos + renderer.pixel_size/2, yPos)
        renderer.pen.down()        

        renderer.pen.fillcolor(self.color)
        renderer.pen.begin_fill()
        renderer.pen.circle(renderer.pixel_size/3)
        renderer.pen.end_fill()
        return 
        


    def draw(self, renderer):          
        leftMargin = (abs(self.x - abs(renderer.frame[0]))) * renderer.pixel_size
        bottomMargin = (renderer.frame[3] - self.y) * renderer.pixel_size
        xPos = -renderer.screen.canvwidth/2 + leftMargin
        yPos = -renderer.screen.canvheight/2 + bottomMargin        
        
        renderer.pen.up()
        renderer.pen.setpos(xPos + renderer.pixel_size/2, yPos)
        renderer.pen.down()        

        renderer.pen.fillcolor(self.color)
        renderer.pen.begin_fill()
        renderer.pen.circle(renderer.pixel_size/3)
        renderer.pen.end_fill()
        return 


'''
Reads a map from file. Maps are expected to list their width and height on the first line, and
on a newline read out each row of the map line by line. No spaces.

Returns the constructed MapGrid
'''
def LoadMap(filename):
    try:
        mapFile = open(filename, "r")
    except OSError:
        print("Map file could not be loaded.")
        return -1
    
    width = int(ReadUntil(mapFile, " "))
    height = int(ReadUntil(mapFile, '\n'))

    grid = MapGrid(width, height)

    for y in range(height):
        rowString = ReadUntil(mapFile, '\n')
        row = []
        for x in range(width):
            n = int(rowString[x])
            if n == 1:
                row.append(PathCell(x, y))
            elif n == 3:
                grid.guards.append(Guard(x, y, 2))
                row.append(PathCell(x, y))
            elif n == 5:
                grid.player = Player(x, y, grid)
                row.append(PathCell(x, y))
            elif n == 8:
                row.append(KeyCell(x, y))
            elif n == 9:
                row.append(DoorCell(x, y))
            else:
                row.append(Cell(x, y))

        grid.AddRow(row)
    return grid

'''
Reads the given file in bytes until it reaches the given delimeter character.
Returns what was read as a string.
'''
def ReadUntil(fileObject, delimiter):
    temp = fileObject.read(1)
    out = ""
    while temp != delimiter:
        out = out + temp
        temp = fileObject.read(1)
    return out

