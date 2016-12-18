import pygame
import random

def draw_rect_with_alpha(display, rgba, pos, size):
	rect = pygame.Surface(size, flags = int("0x00010000", 16))
	rect.fill(rgba)
	display.blit(rect, pos)

class Cell:

	CURRENT_COLOR = None
	VISITED_COLOR = None
	BACKGROUND_COLOR = None
	BACKTRACKED_COLOR = None
	SHOW_BACKTRACK = None

	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.visited = False
		self.walls = [True for e in range(4)]
		self.current = False
		self.backtracked = False
		self.last_draw = {
			"walls": [],
			"visited": None,
			"current": None,
			"backtracked": None
		}

	def draw(self, display, color, size):
		to_compare = {
			"walls": self.walls,
			"current": self.current,
			"visited": self.visited,
			"backtracked": self.backtracked
		}

		if to_compare != self.last_draw:
			pygame.draw.rect(display, self.BACKGROUND_COLOR, pygame.Rect(Vector((self.col, self.row)) * size, (size, size)))
			self.__draw(display, color, size)
			self.last_draw["walls"] = self.walls[:]
			self.last_draw["current"] = self.current
			self.last_draw["visited"] = self.visited
			self.last_draw["backtracked"] = self.backtracked


	def __draw(self, display, color, size):
		if self.walls[0]: # up
			pygame.draw.line(display, color, (self.col * size       , self.row * size)       , (self.col * size + size, self.row * size))
		if self.walls[3]: # down
			pygame.draw.line(display, color, (self.col * size + size, self.row * size + size), (self.col * size       , self.row * size + size))
		if self.walls[1]: #left
			pygame.draw.line(display, color, (self.col * size + size, self.row * size)       , (self.col * size + size, self.row * size + size))
		if self.walls[2]: #right
			pygame.draw.line(display, color, (self.col * size       , self.row * size + size), (self.col * size       , self.row * size))

		if self.current:
			draw_rect_with_alpha(display, self.CURRENT_COLOR, Vector((self.col, self.row)) * size, (size, size))

		elif self.backtracked and self.SHOW_BACKTRACK:
			draw_rect_with_alpha(display, self.BACKTRACKED_COLOR, Vector((self.col, self.row)) * size, (size, size))

		elif self.visited:
			draw_rect_with_alpha(display, self.VISITED_COLOR, Vector((self.col, self.row)) * size, (size, size))

		

	def get_neighbours(self, grid):
		for diff in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			res = Vector((self.row, self.col)) + diff
			if res[0] >= 0 and res[1] >= 0 and res[0] < len(grid) and res[1] < len(grid[0]):
				yield grid[res[0]][res[1]]

	def get_unvisited_neighbours(self, grid):
		for neighbour in self.get_neighbours(grid):
			if not neighbour.visited:
				yield neighbour

	def remove_wall(self, direction, other):
		d_map = {
			(-1,  0): 3,
			(1 ,  0): 0,
			(0 , -1): 1,
			(0 ,  1): 2
		}
		self.walls[d_map[direction]] = False
		other.walls[3 - d_map[direction]] = False


class Vector(tuple):
	def __mul__(self, other):
		return Vector([e * other for e in self])

	def __add__(self, other):
		return Vector([a + b for a, b in zip(self, other)])

	def __sub__(self, other):
		return Vector([a - b for a, b in zip(self, other)])


def make_maze(grid):
	current = grid[0][0]
	current.visited = True
	current.current = True
	visited = [current]
	stack = []
	yield current
	while len(visited) < len(grid) * len(grid[0]):
		current_neighbours = [neighbour for neighbour in current.get_unvisited_neighbours(grid)]
		if len(current_neighbours) > 0:
			next_cell = random.choice(current_neighbours)
			stack.append(current)
			current.remove_wall(Vector((current.row, current.col)) - (next_cell.row, next_cell.col), next_cell)
			current.current = False
			current = next_cell
			current.visited = True
			current.current = True
			visited.append(current)
		elif len(stack) > 0:
			current.current = False
			current.backtracked = True
			current = stack.pop(-1)
			current.current = True
			current.backtracked = True
		yield current
	while len(stack) > 0:
		current.current = False
		current.backtrackted = True
		current = stack.pop(-1)
		current.current = True
		current.backtrackted = True
		yield current
	current.current = False
