'''

This is a python game to simulate navigating the steam tunnels of Iowa State at night. 
You are not supposed to be in there so you will have to be very sneaky, areful, and lucky
to make it through without getting caught. Objective: get to the other side so you can buy a hot
chocolate form the hub.

Players will have limited knowledge of the map surrounding them and the obstacles they face.

Author: Andrew Frank

'''
import tkinter as tk
import map
import render
PIXELWIDTH = 10

INTRO = '''Woah, you're not supposed to be here!
These are the Iowa State steam tunnels; authorized personnel only!
Aw, I'll let you off the hook since it seems like you've had a bad day, but the other staff might not be so kind... 
If you want to leave you'll have to find the key and an exit before a guard catches you.
If you see one, don't worry too much about getting caught. They are slow but diligent.
I'd be quick about it too if I were you, there's no food or water down here.
Sorry to leave you like this, but I have some leaky pipes to fix... smell ya later!

CONTROLS:
W: up
S: down
A: left
D: right
Esc: quit

'''

WIN = '''CONGRATULATIONS!
You made it out of the steam tunnels! Sorry it was so dank and quiet in there,
we don't usually have lots of visitors.

If you want a real reward, send an email to akfrank@iastate.edu requesting a 
hot chocolate and a screenshot of this message, he's a nice guy so I'm sure
he'll ge one for you :)
'''

LOSE = '''Look what we got here, another student sneaking around the steam tunnels. 
Wendy is going to want to hear about this.

Oh no! You couldn't escape the guards! Better luck next time...
'''

TIRED = '''After wandering around in the steam tunnels for hours, you pass out on the floor.
You're filled with determination to try again.
'''

QUIT = '''Goodbye, see you again soon!'''

def start():
	#Initialization
	game = map.LoadMap("lvl1.map")

	# print intro message
	print(INTRO)
	input("Press enter to start playing.")

	#Load Renderer
	app = tk.Tk()
	graphics = render.Renderer(app, 1080, 756, PIXELWIDTH, game)
	graphics.start()
	if game.player.hasWon:	
		print(WIN)
	else:
		if game.player.hasLost:
			print(LOSE)
		elif game.player.isTired:
			print(TIRED)
		else:
			print(QUIT)

start()




