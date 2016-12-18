#! python

import pygame
import generator
import argparse

pygame.init()

RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

WINDOW_SIZE = None
SQUARE_SIZE = None

FRAMERATE = None
UPDATES = None # every other frame

BACKGROUND_COLOR = None
LINE_COLOR = None
CURRENT_COLOR = None
VISITED_COLOR = None
BACKTRACKED_COLOR = None

SHOW_BACKTRACK = None

def setup():
	global WINDOW_SIZE, SQUARE_SIZE, FRAMERATE, BACKGROUND_COLOR, LINE_COLOR, UPDATES, CURRENT_COLOR, VISITED_COLOR, BACKTRACKED_COLOR, SHOW_BACKTRACK

	parser = argparse.ArgumentParser(description="Randomly creates a maze with a given size")
	parser.add_argument("-s", "--size", default = (800, 600),  help = "Specifyes the window size. Defalut is 800x600.", nargs = 2, type = int, metavar = ("width", "height"))
	parser.add_argument("-S", "--square", default = 10, help = "Specifyes the squares' size. Default is 10.", type = int, metavar = "size")
	parser.add_argument("-f", "--framerate", default = 60, help = "Specifyes the framerate. Default is 60 fps.", type = int, metavar ="fps")
	parser.add_argument("-b", "--background", default = (32, 32, 32), help = "Specifyes the background color. Colors are given in RGB format. Defalut is (32, 32, 32)",
						nargs = 3, type = int, metavar = ("r", "g", "b"))
	parser.add_argument("-u", "--update", default = 1, help = "Specifyes how oft the screen should update, i.e. a value of 1 means every frame, a value of 2 means every other frame and so on. Default is 1", type=int)
	parser.add_argument("-l", "--line", default = WHITE, help = "Specifyes the color used for the lines. The color is given in RGB format. Default is %s" % (str(WHITE)),
						nargs = 3, type = int, metavar = ("r", "g", "b"))
	parser.add_argument("-c", "--current", default = (0, 255, 0, 255), help = "Specifyes the color of the current position. The color is given in RGBA form. Default is (0, 255, 0, 0)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-v", "--visited", default = (255, 0, 255, 50), help = "Specifyes the color of the visited positions. The color is given in RGBA form. Default is (255, 0, 255, 50)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-B", "--backtrack", default = (0, 128, 255, 50), help = "Specifyes the color of backtracked positions. The color is given in RGBA form. Default is (0, 128, 255, 50)",
						nargs = 4, type = int, metavar = ("r", "g", "b", "a"))
	parser.add_argument("-nb", "--no-backtrack", action = "store_true", help = "Does not mark backtrackted positions with a different color")

	args = parser.parse_args()

	WINDOW_SIZE = tuple(args.size)
	SQUARE_SIZE = args.square
	FRAMERATE = args.framerate
	BACKGROUND_COLOR = tuple(args.background)
	LINE_COLOR = tuple(args.line)
	UPDATES = args.update
	CURRENT_COLOR = tuple(args.current)
	VISITED_COLOR = tuple(args.visited)
	BACKTRACKED_COLOR = tuple(args.backtrack)
	SHOW_BACKTRACK = not args.no_backtrack

def clear_screen(display):
	display.fill(BACKGROUND_COLOR)

def run_generator(display, clock, grid):
	frame = 0
	for current in generator.make_maze(grid):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		frame += 1
		frame %= UPDATES
		if frame == 0:
			for row in grid:
				for cell in row:
					cell.draw(display, LINE_COLOR, SQUARE_SIZE)


			pygame.display.update()
		clock.tick(FRAMERATE)
	for row in grid:
		for cell in row:
			cell.draw(display, LINE_COLOR, SQUARE_SIZE)


	pygame.display.update()


def init_vars():
	generator.Cell.BACKGROUND_COLOR = BACKGROUND_COLOR
	generator.Cell.VISITED_COLOR = VISITED_COLOR
	generator.Cell.CURRENT_COLOR = CURRENT_COLOR
	generator.Cell.BACKTRACKED_COLOR = BACKTRACKED_COLOR
	generator.Cell.SHOW_BACKTRACK = SHOW_BACKTRACK
	

def main():
	init_vars()
	game_display = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Maze Generator")
	clock = pygame.time.Clock()
	running = True
	first_time = True
	background = pygame.Surface(WINDOW_SIZE)
	background.fill(BACKGROUND_COLOR)
	game_display.blit(background, (0,0))

	while running:
		grid = [[generator.Cell(row, col) for col in range(WINDOW_SIZE[0] // SQUARE_SIZE)] for row in range(WINDOW_SIZE[1] // SQUARE_SIZE)]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				run_generator(game_display, clock, grid)
				first_time = False

		if first_time:
			for row in grid:
				for cell in row:
					cell.draw(game_display, LINE_COLOR, SQUARE_SIZE)
			pygame.display.update()
			clock.tick(FRAMERATE)
			clear_screen(game_display)
		else:
			clock.tick(FRAMERATE)

if __name__ == '__main__':
	setup()
	main()