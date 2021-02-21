'''
 Stores functions for drawing graphics to screen

 NOTE: Top of screen is -y, bottom is +y for coordinates (Except in turtle it is the reverse) @_@

 Author: Andrew Frank
'''
import tkinter as tk
import turtle

class Renderer:
    PIXELWIDTH = None
    PIXELHEIGHT = None
    canvas = None
    screen = None
    pen = None
    pixel_size = None
    game = None
    frame = None

    def __init__(self, app, width, height, pixelwidth, game):
        self.game = game
        self.canvas = tk.Canvas(app, bg="black", height=height, width=width)
        self.canvas.pack()
        self.screen = turtle.TurtleScreen(self.canvas)
        self.pen = turtle.RawTurtle(self.screen)
        self.pen.ht()        
        self.pen.speed(0)
        self.pen._delay(0)
        self.pen._tracer(0)
        self.size_pixels(pixelwidth)
        # set initial frame around player
        self.frame = [game.player.x - self.PIXELWIDTH//2, game.player.y - self.PIXELHEIGHT//2, game.player.x + self.PIXELWIDTH//2, game.player.y + self.PIXELHEIGHT//2]
        self.draw_screen() #draw initial screen             

    def size_pixels(self, pixelwidth):
        self.PIXELWIDTH = pixelwidth
        self.pixel_size = int(self.screen.window_width()) / self.PIXELWIDTH
        self.PIXELHEIGHT = int(self.screen.window_height()) / self.pixel_size

    def up(self):
        xP = self.game.player.x
        yP = self.game.player.y
        if (yP - 1) >= 0:
            target = self.game.grid[yP - 1][xP]
            if target.can_walk(self.game.player):
                self.game.player.y -= 1
                target.collide(self.game.player)
                if self.game.player.y < self.frame[1]:
                    self.frame[3] -= self.PIXELHEIGHT
                    self.frame[1] -= self.PIXELHEIGHT                
        self.loop()
        return

    def left(self):
        xP = self.game.player.x
        yP = self.game.player.y
        if (xP - 1) >= 0:
            target = self.game.grid[yP][xP - 1]
            if target.can_walk(self.game.player):
                self.game.player.x -= 1
                target.collide(self.game.player)
                if self.game.player.x < self.frame[0]:
                    self.frame[2] -= self.PIXELWIDTH
                    self.frame[0] -= self.PIXELWIDTH                
        self.loop()
        return

    def right(self):
        xP = self.game.player.x
        yP = self.game.player.y
        if (xP + 1) < self.game.width:
            target = self.game.grid[yP][xP + 1]
            if target.can_walk(self.game.player):
                self.game.player.x += 1
                target.collide(self.game.player)    
                if self.game.player.x >= self.frame[2]:
                    self.frame[2] += self.PIXELWIDTH
                    self.frame[0] += self.PIXELWIDTH                
        self.loop()
        return

    def down(self):
        xP = self.game.player.x
        yP = self.game.player.y
        if yP + 1 < self.game.height:
            target = self.game.grid[yP + 1][xP]               
            if target.can_walk(self.game.player):
                self.game.player.y += 1
                target.collide(self.game.player)   
                if self.game.player.y >= self.frame[3]:
                    self.frame[3] += self.PIXELHEIGHT
                    self.frame[1] += self.PIXELHEIGHT
        self.loop()
        return

    def start(self):
        self.screen.onkey(self.stop, "Escape") 
        self.screen.onkey(self.up, "w")
        self.screen.onkey(self.down, "s")
        self.screen.onkey(self.left, "a")
        self.screen.onkey(self.right, "d")
        self.screen.listen()
        self.screen.mainloop()

    def loop(self):
        for guard in self.game.guards:
            if(guard.x < self.frame[2] and guard.x > self.frame[0] and guard.y < self.frame[3] and guard.y > self.frame[1]):
                guard.active = True
            if guard.active and (self.game.turn % 2) == 0:
                guard.move(self.game.player)
            if guard.x == self.game.player.x and guard.y == self.game.player.y:
                guard.collide(self.game.player)
        if self.game.player.hasWon or self.game.player.hasLost or self.game.player.isTired:
            self.stop()
        self.game.turn += 1
        if self.game.turn > 1000:
            self.game.player.isTired = True
        self.draw_screen()

    def stop(self):
        self.canvas.winfo_toplevel().quit()

    def draw_pixel(self, color):
        self.pen.color(color.strip(), color.strip())
        self.pen.begin_fill()
        self.pen.forward(self.pixel_size)
        self.pen.right(90)
        self.pen.forward(self.pixel_size)
        self.pen.right(90)
        self.pen.forward(self.pixel_size)
        self.pen.right(90)
        self.pen.forward(self.pixel_size)
        self.pen.end_fill()
        self.pen.setheading(0)

    def draw_screen(self):
        self.pen.up()
        self.pen.setpos(-self.screen.canvwidth/2, self.screen.canvheight/2) # set pen at top left corner
        self.pen.down()
        for y in range(round(self.frame[1]), round(self.frame[3]) + 1):
            for x in range(round(self.frame[0]), round(self.frame[2])):
                if x < 0 or x >= self.game.width or y < 0 or y >= self.game.height:
                    self.draw_pixel("#000000")      # if the frame is not defined by map, draw walls                
                else:
                    self.game.grid[y][x].draw(self) # draw a cell of the game grid                
                self.pen.setx(self.pen.xcor() + self.pixel_size) # move the pen over one pixel
           
            self.pen.up()
            self.pen.setpos(-self.screen.canvwidth/2, self.pen.ycor() - self.pixel_size) # move pen down one pixel and all the way left
            self.pen.down()
        self.game.player.draw(self)
        for guard in self.game.guards:            
            guard.draw(self)
        self.pen._update()