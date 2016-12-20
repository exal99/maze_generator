"""
This module is for generating a random maze using a recursive backtracking
algorithm and then displaying it on a pygame.Surface surface.
"""

import pygame
import random

def draw_rect_with_alpha(display, rgba, pos, size):
	"""
	Draws a rectangle at a given position on a given surface with a given size and rgba color.

	Args:
	display 	-	The surface to draw on
	rgba 		- 	The rgba color, i.e. color given in a (Red, Green, Blue, Alpha) format.
	pos 		- 	The position of the rectangle
	size 		- 	The size of the rectangle

	Types:
	display 	-	pygame.Surface
	rgba 		- 	tuple
	pos 		-	tuple
	size 		- 	tuple
	"""
	rect = pygame.Surface(size, flags = int("0x00010000", 16))
	rect.fill(rgba)
	display.blit(rect, pos)

class Cell:
	"""
	A cell in a grid. Used for making a maze out of the grid.
	Cell(row, col) -> Cell
	"""

	# -- ALL VALUES SHOULD BE SET SOMEWHERE OUTSIDE. BY DEFAULT display.init_vars() WILL HANDLE THIS -- #
	CURRENT_COLOR = (0,0,0)
	VISITED_COLOR = (0,0,0)
	BACKGROUND_COLOR = (0,0,0)
	BACKTRACKED_COLOR = (0,0,0)
	START_COLOR = (0,0,0)
	END_COLOR = (0,0,0)
	SHOW_BACKTRACK = False

	def __init__(self, row, col):
		"""
		Initializes the Cell object
		"""
		self.row = row
		self.col = col
		self.visited = False
		self.walls = [True for e in range(4)]
		self.current = False
		self.backtracked = False
		self.start = False
		self.end = False
		self.last_draw = {
			"walls": [],
			"visited": None,
			"current": None,
			"backtracked": None,
			"start": False,
			"end": False
		}

	def __repr__(self):
		return str(self.__dict__)

	def __str__(self):
		return self.__repr__()

	def draw(self, display, color, size, force_draw = False):
		"""
		Draws the cell onto the given display with the given color and size if (and only if)
		there has been a change since the last call of draw.
		Otherwise this method has no effect. The color is a RGB color.

		Args:
		display		-	The surface to draw on
		color 		- 	The color to use for drawing the lines around the cell
		size 		- 	The size of the cell in pixels
		force_draw	-	Forces the cell to paint itself, regardless of any change

		Types:
		display 	- 	pygame.Surface
		color 		-	tuple
		size		-	tuple
		force_draw 	-	bool
		"""
		to_compare = {
			"walls": self.walls,
			"current": self.current,
			"visited": self.visited,
			"backtracked": self.backtracked,
			"start": self.start,
			"end": self.end
		}

		if to_compare != self.last_draw or force_draw:
			pygame.draw.rect(display, self.BACKGROUND_COLOR, pygame.Rect(Vector((self.col, self.row)) * size, (size, size)))
			self.__draw(display, color, size)
			self.last_draw["walls"] = self.walls[:]
			self.last_draw["current"] = self.current
			self.last_draw["visited"] = self.visited
			self.last_draw["backtracked"] = self.backtracked
			self.last_draw["start"] = self.start
			self.last_draw["end"] = self.end


	def __draw(self, display, color, size):
		"""
		Used internally for drawing the cell onto the display regardless of any change.
		This method should not be called outside of Cell as it is very slow to call repeatedly.

		Args:
		display		-	The surface to draw on
		color 		- 	The color to use for drawing the lines around the cell
		size 		- 	The size of the cell in pixels

		Types:
		display 	- 	pygame.Surface
		color 		-	tuple
		size		-	tuple
		"""
		if self.walls[0]: # up
			pygame.draw.line(display, color, (self.col * size       , self.row * size)       , (self.col * size + size, self.row * size))
		if self.walls[3]: # down
			pygame.draw.line(display, color, (self.col * size + size, self.row * size + size), (self.col * size       , self.row * size + size))
		if self.walls[1]: #left
			pygame.draw.line(display, color, (self.col * size + size, self.row * size)       , (self.col * size + size, self.row * size + size))
		if self.walls[2]: #right
			pygame.draw.line(display, color, (self.col * size       , self.row * size + size), (self.col * size       , self.row * size))

		if self.current:
			draw_rect_with_alpha(display, self.CURRENT_COLOR, Vector((self.col, self.row)) * size + (1, 1), (size - 2, size - 2))

		elif self.start:
			draw_rect_with_alpha(display, self.START_COLOR, Vector((self.col, self.row)) * size  + (1, 1), (size - 2, size - 2))

		elif self.end:
			draw_rect_with_alpha(display, self.END_COLOR, Vector((self.col, self.row)) * size  + (1, 1), (size - 2, size - 2))

		elif self.backtracked and self.SHOW_BACKTRACK:
			draw_rect_with_alpha(display, self.BACKTRACKED_COLOR, Vector((self.col, self.row)) * size, (size, size))

		elif self.visited:
			draw_rect_with_alpha(display, self.VISITED_COLOR, Vector((self.col, self.row)) * size, (size, size))



	def get_neighbours(self, grid):
		"""
		Yields all the neighbours of the cell within the given grid.

		Args:
		grid		-	The grid to yield the neighbours

		Types:
		grid		-	Grid


		Yields		-	The neigbours of the cell in the given grid.
		Yield type 	-	Cell
		"""
		for diff in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			res = Vector((self.row, self.col)) + diff
			if res[0] >= 0 and res[1] >= 0 and res[0] < grid.rows and res[1] < grid.cols:
				yield grid[res[0], res[1]]

	def get_unvisited_neighbours(self, grid):
		"""
		Yields all unvisited neighbours of the cell in the given grid.

		Args:
		grid 		-	The grid to yield the neighbours.

		Types:
		grid		-	Grid

		Yields		-	The unvisited neighbours of the cell in the given grid.
		Yield type 	-	Cell
		"""
		for neighbour in self.get_neighbours(grid):
			if not neighbour.visited:
				yield neighbour

	def remove_wall(self, direction, other):
		"""
		Removes the wall between the cell and the other cell, 'other' in the direction 'direction'

		Args:
		direction	-	The direction of the other cell
		other 		- 	The neighbouring cell in the direcion direction

		Types:
		direciton 	-	tuple, {(-1, 0), (1, 0), (0, -1), (0, 1)}
		other 		- 	Cell
		"""
		d_map = {
			(-1,  0): 3,
			(1 ,  0): 0,
			(0 , -1): 1,
			(0 ,  1): 2
		}
		self.walls[d_map[direction]] = False
		other.walls[3 - d_map[direction]] = False


class Vector(tuple):
	"""
	A basic vector that supports multiplication (only with Scalar), addition and subtraction.
	Vector inherits from 'tuple' and therefore it behaves almost the same.
	"""
	def __mul__(self, other):
		return Vector([e * other for e in self])

	def __truediv__(self, other):
		return Vector([e / other for e in self])

	def __floordiv__(self, other):
		return Vector([e // other for e in self])

	def __add__(self, other):
		return Vector([a + b for a, b in zip(self, other)])

	def __sub__(self, other):
		return Vector([a - b for a, b in zip(self, other)])

class Grid:

	def __init__(self, rows, cols):
		self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
		self.rows = rows
		self.cols = cols
		self.current = None
		self.start = None
		self.end = None
		self.visited = set()

	def __getitem__(self, pos):
		return self.grid[pos[0]][pos[1]]

	def __iter__(self):
		for row in self.grid:
			for cell in row:
				yield cell

	def __len__(self):
		return self.rows * self.cols

	def reset(self, new_size = None):
		if new_size is not None:
			self.__init__(new_size[0], new_size[1])
		else:
			self.__init__(self.rows, self.cols)





def make_maze(grid):
	"""
	Runs the generation algorithm on the given grid, yeilding a new
	position every time which is set as the current position.
	For more information on the algorithm in use, see:
	https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker


	Args:
	grid 		-	The grid to make the maze on.

	Types:
	grid		-	Grid


	Yields		-	The current position of the algorithm, i.e. the position
					that will be evaluated next according to the rules of the
					algorithm.
	Yield type 	-	Cell
	"""
	current = grid[0, 0]
	current.visited = True
	current.current = True
	visited = [current]
	stack = []
	yield current
	while len(visited) < len(grid):
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

	while len(stack) > 0 and Cell.SHOW_BACKTRACK:
		current.current = False
		current.backtracked = True

		current = stack.pop(-1)
		current.current = True
		current.backtracked = True

		yield current

	current.current = False
