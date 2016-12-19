#! python
"""
This module is used for displaying and running a maze generation algorithm.
This moduel uses pygame to create the graphical display.
"""

import pygame
import generator
import argparse
import functools
import sys

RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# -- ALL VARIABLES ARE SET BY setup() FROM THE COMMAND LINE ARGUMENTS OR DEFAULT VALUES -- #

WINDOW_SIZE = None
SQUARE_SIZE = None

FRAMERATE = None
UPDATES = None # every other frame

BACKGROUND_COLOR = None
LINE_COLOR = None
CURRENT_COLOR = None
VISITED_COLOR = None
BACKTRACKED_COLOR = None
FROM_COLOR = None
TO_COLOR = None

SHOW_BACKTRACK = None
SHOW_LOAD = None

def setup():
	"""
	Sets all global constants to their apropriate values, either a default value or one specified from the command line
	"""
	global WINDOW_SIZE, SQUARE_SIZE, FRAMERATE, BACKGROUND_COLOR, LINE_COLOR, UPDATES, CURRENT_COLOR, VISITED_COLOR
	global BACKTRACKED_COLOR, SHOW_BACKTRACK, SHOW_LOAD, FROM_COLOR, TO_COLOR

	parser = argparse.ArgumentParser(description="Randomly creates a maze and displays the proces and the result in a new window")
	parser.add_argument("-nl", "--no-load", action = "store_true", help = "Skips the loadingprocec of the maze generation")
	parser.add_argument("-nb", "--no-backtrack", action = "store_true", help = "Does not mark backtrackted positions with a different color")
	parser.add_argument("-s", "--size", default = (800, 600),  help = "Specifies the window size. Defalut is 800x600.", nargs = 2, type = int, metavar = ("width", "height"))
	parser.add_argument("-S", "--square-size", default = 20, help = "Specifies the squares' size. Default is 20.", type = int, metavar = "size")
	parser.add_argument("-f", "--framerate", default = 60, help = "Specifies the framerate. Default is 60 fps.", type = int, metavar ="fps")
	parser.add_argument("-u", "--update", default = 1, help = "Specifies how oft the screen should update, i.e. a value of 1 means every frame, a value of 2 means every other frame and so on. Default is 1", type=int)
	
	parser.add_argument("-b", "--background-color", default = (32, 32, 32), help = "Specifies the background color. Colors are given in RGB format. Defalut is (32, 32, 32)",
						nargs = 3, type = int, metavar = ("r", "g", "b"))
	parser.add_argument("-l", "--line-color", default = WHITE, help = "Specifies the color used for the lines. The color is given in RGB format. Default is %s" % (str(WHITE)),
						nargs = 3, type = int, metavar = ("r", "g", "b"))
	parser.add_argument("-c", "--current-color", default = (0, 255, 0, 255), help = "Specifies the color of the current position. The color is given in RGBA form. Default is (0, 255, 0, 0)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-v", "--visited-color", default = (255, 0, 255, 50), help = "Specifies the color of the visited positions. The color is given in RGBA form. Default is (255, 0, 255, 50)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-B", "--backtrack-color", default = (0, 128, 255, 50), help = "Specifies the color of backtracked positions. The color is given in RGBA form. Default is (0, 128, 255, 50)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-F" , "--from-color", default = (255, 0, 0, 50), help = "Specifies the color of from positions. The color is given in RGBA form. Default is (255, 0, 0, 50)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-t" , "--to-color", default = (0, 255, 0, 255), help = "Specifies the color of from positions. The color is given in RGBA form. Default is (0, 0, 255, 255)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))

	

	args = parser.parse_args()

	WINDOW_SIZE = tuple(args.size)
	SQUARE_SIZE = args.square_size
	FRAMERATE = args.framerate
	BACKGROUND_COLOR = tuple(args.background_color)
	LINE_COLOR = tuple(args.line_color)
	UPDATES = args.update
	CURRENT_COLOR = tuple(args.current_color)
	VISITED_COLOR = tuple(args.visited_color)
	BACKTRACKED_COLOR = tuple(args.backtrack_color)
	SHOW_BACKTRACK = not args.no_backtrack
	SHOW_LOAD = not args.no_load
	FROM_COLOR = tuple(args.from_color)
	TO_COLOR = tuple(args.to_color)

def clear_screen(display):
	"""
	Clears the given display by filling it with BACKGOUND_COLOR

	Args:
	dispalay	-	The display to clear

	Types:
	display 	-	pygame.Surface
	"""
	display.fill(BACKGROUND_COLOR)

def run_generator(display, clock, grid):
	"""
	Runs the maze generation with the given display, clock, grid

	Args:
	display 	-	The display to display everyting on
	clock 		-	The clock used for limiting the framerate
	grid 		- 	The grid to generate the maze on

	Types:
	display 	-	pygame.Surface
	clock 		- 	pygame.time.Clock
	grid 		- 	generation.Grid
	"""
	frame = 0
	for current in generator.make_maze(grid):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
		frame += 1
		frame %= UPDATES
		if frame == 0 and SHOW_LOAD:
			draw_grid(display, grid)
		if SHOW_LOAD:
			clock.tick(FRAMERATE)

	pick_positions(grid)
	return True

def init_vars():
	"""
	Initializes all of Cell's common variables based on the global variables
	"""
	generator.Cell.BACKGROUND_COLOR = BACKGROUND_COLOR
	generator.Cell.VISITED_COLOR = VISITED_COLOR
	generator.Cell.CURRENT_COLOR = CURRENT_COLOR
	generator.Cell.BACKTRACKED_COLOR = BACKTRACKED_COLOR
	generator.Cell.SHOW_BACKTRACK = SHOW_BACKTRACK
	generator.Cell.END_COLOR = TO_COLOR
	generator.Cell.START_COLOR = FROM_COLOR

def keypress_handler(display, clock, event, grid):
	keybindings = {
		pygame.K_c     : grid.reset,
		pygame.K_SPACE : lambda : run_generator(display, clock, grid) if not grid[0,0].visited else None,
		pygame.K_UP    : functools.partial(arrow_key, grid, (-1, 0)),
		pygame.K_DOWN  : functools.partial(arrow_key, grid, (1, 0)),
		pygame.K_LEFT  : functools.partial(arrow_key, grid, (0, -1)),
		pygame.K_RIGHT : functools.partial(arrow_key, grid, (0, 1))
	}
	if event.key in keybindings:
		res = keybindings[event.key]()
		print()
		sys.stdout.flush()
		return res
	else:
		return None

def draw_grid(display, grid):
	for cell in grid:
		cell.draw(display, LINE_COLOR, SQUARE_SIZE)
	pygame.display.update()

def pick_positions(grid):
	grid[0,0].start = True
	grid[grid.rows - 1, grid.cols - 1].end = True

def move(grid, direction, current):
	wall_map = {
		(1 ,  0): 3,
		(-1,  0): 0,
		(0 , -1): 2,
		(0 ,  1): 1
	}
	new_pos = generator.Vector(direction) + (current.row, current.col)
	print("NEW POS:", new_pos)
	if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < grid.rows and new_pos[1] < grid.cols:
		to_move_to = grid[new_pos]
		print("WALLS", current.walls)
		if not current.walls[wall_map[direction]]:
			to_move_to.current = True
			current.current = False
			print(to_move_to.row, to_move_to.col)
			return to_move_to
		else:
			return current
	else:
		print(current)
		return current

def arrow_key(grid, direction):
	if grid.current is None:
		grid.current = find_start(grid)
		grid.current.current = True
	print("INSIDE", grid.current)
	grid.current = move(grid, direction, grid.current)
	print("MOVE", (grid.current.row, grid.current.col) if grid.current is not None else None, direction)

def find_start(grid):
	for cell in grid:
		if cell.start:
			print("found cell:", (cell.row, cell.col))
			return cell

def main():
	"""
	Main function of the program.
	"""
	pygame.init()
	init_vars()
	game_display = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Maze Generator")
	clock = pygame.time.Clock()
	running = True
	background = pygame.Surface(WINDOW_SIZE)
	background.fill(BACKGROUND_COLOR)
	game_display.blit(background, (0,0))
	grid = generator.Grid(WINDOW_SIZE[1] // SQUARE_SIZE, WINDOW_SIZE[0] // SQUARE_SIZE)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				res = keypress_handler(game_display, clock, event, grid)
				if res == False:
					return

		draw_grid(game_display, grid)
		clock.tick(FRAMERATE)

if __name__ == '__main__':
	setup()
	main()