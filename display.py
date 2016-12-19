#! python
"""
This module is used for displaying and running a maze generation algorithm.
This moduel uses pygame to create the graphical display.
"""

import pygame
import generator
import argparse
import functools
import random

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


# -- PROGRAM SPECIFIC EVENTS -- #
START_CLOCK = pygame.USEREVENT + 1
STOP_CLOCK  = pygame.USEREVENT + 2
HIT_WALL    = pygame.USEREVENT + 3

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
	global SHOW_LOAD
	prev_show = SHOW_LOAD
	frame = 0
	for current in generator.make_maze(grid):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				SHOW_LOAD = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return False
		frame += 1
		frame %= UPDATES
		if frame == 0 and SHOW_LOAD:
			draw_grid(display, grid)
		if SHOW_LOAD:
			clock.tick(FRAMERATE)

	pick_positions(grid)
	SHOW_LOAD = prev_show
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
		pygame.K_c      : functools.partial(reset, display, grid),
		pygame.K_SPACE  : lambda : run_generator(display, clock, grid) if not grid[0,0].visited else None,
		pygame.K_UP     : functools.partial(arrow_key, grid, (-1, 0)),
		pygame.K_DOWN   : functools.partial(arrow_key, grid, (1, 0)),
		pygame.K_LEFT   : functools.partial(arrow_key, grid, (0, -1)),
		pygame.K_RIGHT  : functools.partial(arrow_key, grid, (0, 1)),
		pygame.K_ESCAPE : lambda : False
	}
	if event.key in keybindings:
		res = keybindings[event.key]()
		return res
	else:
		return None

def reset(display, grid):
	grid.reset()
	pygame.event.post(pygame.event.Event(STOP_CLOCK, finnished=False))
	for cell in grid:
		cell.draw(display, LINE_COLOR, SQUARE_SIZE, force_draw = True)

def draw_grid(display, grid):
	for cell in grid:
		cell.draw(display, LINE_COLOR, SQUARE_SIZE)
	pygame.display.update()

def pick_positions(grid):
	grid.start = grid[0,0]
	grid.start.start = True

	grid.end = grid[grid.rows - 1, grid.cols - 1]
	grid.end.end = True

def move(grid, direction, current):
	wall_map = {
		(1 ,  0): 3,
		(-1,  0): 0,
		(0 , -1): 2,
		(0 ,  1): 1
	}
	new_pos = generator.Vector(direction) + (current.row, current.col)
	if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < grid.rows and new_pos[1] < grid.cols:
		to_move_to = grid[new_pos]
		if not current.walls[wall_map[direction]]:
			to_move_to.current = True
		else:
			pygame.event.post(pygame.event.Event(HIT_WALL))
			new_pos = (random.randint(0, grid.rows - 1), random.randint(0, grid.cols - 1))
			while new_pos == (grid.rows - 1, grid.cols - 1):
				new_pos = (random.randint(0, grid.rows - 1), random.randint(0, grid.cols - 1))
			to_move_to = grid[new_pos]
			current.current = False
			to_move_to.current = True

		if to_move_to == grid.end:
			pygame.event.post(pygame.event.Event(STOP_CLOCK, finnished=True))
			to_move_to.current = False
			return None

		current.current = False
		return to_move_to
	else:
		pygame.event.post(pygame.event.Event(HIT_WALL))
		return current

def arrow_key(grid, direction):
	if grid.start is not None:
		if grid.current is None:
			grid.current = grid.start
			grid.current.current = True
			pygame.event.post(pygame.event.Event(START_CLOCK))
		grid.current = move(grid, direction, grid.current)

def display_text(display, text, color, size, pos, grid):
	font = pygame.font.SysFont("monospace", size)
	label = font.render(text, 1, color)
	if type(pos) == str:
		display_pos = tuple([e for e in map(int, (generator.Vector((display.get_size())) / 2) - generator.Vector(label.get_size())/2)])

		if "south" in pos:
			display_pos = (display_pos[0], display.get_height() - label.get_height())
		elif "north" in pos:
			display_pos = (display_pos[0], 0)

		if "east" in pos:
			display_pos = (display.get_width() - label.get_width(), display_pos[1])
		elif "west" in pos:
			display_pos = (0, display_pos[1])
		pos = display_pos

	force_update_surface(display, label, pos, grid)
	display.blit(label, pos)
	return label, pos

def force_update_surface(display, surface, pos, grid):
	to_pos = generator.Vector(surface.get_size()) + pos
	from_index =(pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE)   # row col
	to_index = (to_pos[1] // SQUARE_SIZE + (1 if to_pos[1] % SQUARE_SIZE != 0 else 0), to_pos[0] // SQUARE_SIZE + (1 if to_pos[0] % SQUARE_SIZE != 0 else 0))

	if from_index[0] != to_index[0] and from_index[1] != to_index[1]:
		for row in range(from_index[0], to_index[0]):
			for col in range(from_index[1], to_index[1]):
				grid[row,col].draw(display, LINE_COLOR, SQUARE_SIZE, force_draw = True)
	elif from_index[0] != to_index[0]:
		for row in range(from_index[0], to_index[0]):
			grid[row,from_index[1]].draw(display, LINE_COLOR, SQUARE_SIZE, force_draw = True)
	else:
		for col in range(from_index[1], to_index[1]):
			grid[from_index[0],col].draw(display, LINE_COLOR, SQUARE_SIZE, force_draw = True)

def format_time(time):
	hundrets = (time // 10) % 100
	seconds = time // 1000
	minutes = seconds // 60
	seconds %= 60

	return minutes, seconds, hundrets

def display_timer(display, start_time, grid, font_size):
	time_passed = pygame.time.get_ticks() - start_time
	display_text(display, "%d:%02d.%02d" %(format_time(time_passed)), RED, font_size, "north east", grid)

def display_time(display, time, grid, font_size):
	display_text(display, "%d:%02d.%02d" %(format_time(time)), RED, font_size, "north east", grid)


def main():
	"""
	Main function of the program.
	"""
	pygame.init()
	pygame.font.init()
	pygame.mixer.init()
	init_vars()

	hit_sound = pygame.mixer.Sound("hit.wav")
	game_display = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Maze Generator")
	clock = pygame.time.Clock()
	running = True
	background = pygame.Surface(WINDOW_SIZE)
	background.fill(BACKGROUND_COLOR)
	game_display.blit(background, (0,0))
	grid = generator.Grid(WINDOW_SIZE[1] // SQUARE_SIZE, WINDOW_SIZE[0] // SQUARE_SIZE)
	start_time = -1
	final_time = -1
	time_flash = 60
	hit_flash = 0
	hits = 0
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				res = keypress_handler(game_display, clock, event, grid)
				if res == False:
					return
			if event.type == START_CLOCK:
				start_time = pygame.time.get_ticks()
				final_time = -1
				hits = 0
			if event.type == STOP_CLOCK:
				if event.finnished:
					final_time = pygame.time.get_ticks() - start_time
				else:
					final_time = -1
				start_time = -1
			if event.type == HIT_WALL:
				hit_sound.play().play(hit_sound)
				hit_flash = 10
				hits += 1

		draw_grid(game_display, grid)
		display_text(game_display, "HITS: %d" %(hits), RED, 40, "north", grid)

		if hit_flash % 2 and hit_flash > -1:
			generator.draw_rect_with_alpha(game_display, (255, 0, 0, 100), (0,0), WINDOW_SIZE)
			pygame.display.update()
		elif hit_flash > -1:
			force_update_surface(game_display, pygame.Surface(WINDOW_SIZE), (0,0), grid)

		if start_time != -1:
			display_timer(game_display, start_time, grid, 40)
		elif final_time != -1:
			if time_flash > FRAMERATE / 2:
				display_time(game_display, final_time, grid, 40)
			if time_flash < FRAMERATE / 2:
				label, pos = display_text(game_display, "%d:%02d.%02d" %(format_time(final_time)), RED, 40, "north east", grid)
				force_update_surface(game_display, label, pos, grid)
			time_flash = max(time_flash - 1, 0)
			if time_flash == 0:
				time_flash = FRAMERATE

		hit_flash = max(hit_flash - 1, -1)
		clock.tick(FRAMERATE)

if __name__ == '__main__':
	setup()
	main()