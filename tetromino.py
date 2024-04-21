from tile import Tile
from point import Point
import copy as cp
import numpy as np
import random
class Tetromino:
   # the dimensions of the game grid (defined as class variables)
   grid_height, grid_width = None, None
   tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']

   # A constructor for creating a tetromino with a given shape (type)
   def __init__(self, shape):
      self.type = shape  # set the type of this tetromino
      # determine the occupied (non-empty) cells in the tile matrix based on
      # the shape of this tetromino (see the documentation given with this code)
      occupied_cells = []
      if self.type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial rotation state
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((1, 3))
      elif self.type == '.':
         n = 1  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial rotation state
         occupied_cells.append((0, 0))  # (column_index, row_index)


      elif self.type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial rotation state
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial rotation state
         occupied_cells.append((0, 1))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((2, 2))
      elif self.type == 'J':
         n = 3
         # shape of the tetromino J in its initial rotation state
         occupied_cells.append((0, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'L':
         n = 3
         # shape of the tetromino L in its initial rotation state
         occupied_cells.append((2, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'S':
         n = 3
         # shape of the tetromino S in its initial rotation state
         occupied_cells.append((1, 0))
         occupied_cells.append((2, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'T':
         n = 3
         # shape of the tetromino T in its initial rotation state
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      # create a matrix of numbered tiles based on the shape of this tetromino
      self.tile_matrix = np.full((n, n), None)
      # create the four tiles (minos) of this tetromino and place these tiles
      # into the tile matrix
      for col_index, row_index in occupied_cells:
         # Assign a random number (2 or 4) to each tile in the tetromino
         self.tile_matrix[row_index][col_index] = Tile(random.choice([2, 4]))

      # initialize the position of this tetromino (as the bottom left cell in
      # the tile matrix) with a random horizontal position above the game grid
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)


   # matrix specified by the given row and column indexes
   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      # horizontal position of the cell
      position.x = self.bottom_left_cell.x + col
      # vertical position of the cell
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position


   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      # copy the tiles from the tile matrix of this tetromino
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      # return just the matrix copy when return_position is not set (as True)
      # the argument return_position defaults to False when a value is not given
      if not return_position:
         return copy
      # otherwise return the position of the bottom left cell in copy as well
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied cell as a tile on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.get_cell_position(row, col)
               # draw only the tiles that are inside the game grid
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position)

   def move(self, direction, game_grid):
      # check if this tetromino can be moved in the given direction by using
      # the can_be_moved method defined below
      if not (self.can_be_moved(direction, game_grid)):
         return False  # the tetromino cannot be moved in the given direction
      # move this tetromino by updating the position of its bottom left cell
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      else:  # direction == "down"
         self.bottom_left_cell.y -= 1
      return True  # a successful move in the given direction

   def rotate(self, game_grid):
      if self.type == 'O':
         return False
      self.tile_matrix = np.rot90(self.tile_matrix, -1)

      if not self.can_be_moved("rotate", game_grid):
         self.tile_matrix = np.rot90(self.tile_matrix, 1)
         return False

      return True

   # method for checking if this tetromino can be moved in a given direction
   # method for checking if this tetromino can be moved in a given direction
   def can_be_moved(self, direction, game_grid):
       n = len(self.tile_matrix)  # n = number of rows = number of columns
       for row in range(n):
           for col in range(n):
               # if the cell is not empty (there is a tile)
               if self.tile_matrix[row][col] is not None:
                   # calculate the position of the cell on the grid
                   pos = self.get_cell_position(row, col)
                   # check for the left boundary
                   if direction == "left" and (pos.x - 1 < 0 or game_grid.is_occupied(pos.y, pos.x - 1)):
                       return False
                   # check for the right boundary
                   if direction == "right" and (
                           pos.x + 1 >= game_grid.grid_width or game_grid.is_occupied(pos.y, pos.x + 1)):
                       return False
                   # check for the lower boundary
                   if direction == "down" and (pos.y - 1 < 0 or game_grid.is_occupied(pos.y - 1, pos.x)):
                       return False
                   # for rotation, we need to check every tile of the tetromino
                   if direction == "rotate":
                       for rot_row in range(n):
                           for rot_col in range(n):
                               # calculate the new position after rotation
                               new_pos = self.get_cell_position(rot_row, rot_col)
                               # check if the new position is inside the grid and not occupied
                               if not game_grid.is_inside(new_pos.y, new_pos.x) or game_grid.is_occupied(new_pos.y,
                                                                                                         new_pos.x):
                                   return False
       # if none of the checks above failed, the tetromino can be moved/rotated
       return True
