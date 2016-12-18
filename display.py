import pygame
import generator

pygame.init()

RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

WINDOW_SIZE = (800,600)
SQUARE_SIZE = 10

FRAMERATE = 600
UPDATES = 1 # every other frame

BACKGROUND_COLOR = BLACK

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
					cell.draw(display, WHITE, SQUARE_SIZE)
			#rect = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), flags = int("0x00010000", 16))
			#rect.fill((0, 255, 0, 100))
			#display.blit(rect, (current.col * SQUARE_SIZE, current.row * SQUARE_SIZE))


			pygame.display.update()
		clock.tick(FRAMERATE)
		#clear_screen(display)
	for row in grid:
		for cell in row:
			cell.draw(display, WHITE, SQUARE_SIZE)
	rect = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), flags = int("0x00010000", 16))
	rect.fill((0, 255, 0, 100))
	display.blit(rect, (current.col * SQUARE_SIZE, current.row * SQUARE_SIZE))


	pygame.display.update()


def main():
	game_display = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Maze Generator")
	clock = pygame.time.Clock()
	running = True
	first_time = True
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
					cell.draw(game_display, WHITE, SQUARE_SIZE)
			pygame.display.update()
			clock.tick(FRAMERATE)
			clear_screen(game_display)
		else:
			clock.tick(FRAMERATE)
			# rect = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), flags = int("0x00010000", 16))
			# rect.fill((0, 255, 0, 100))
			# game_display.blit(rect, (current.col * SQUARE_SIZE, current.row * SQUARE_SIZE))


			# pygame.display.update()
			# clock.tick(30)
			# clear_screen(game_display)

		

if __name__ == '__main__':
	main()