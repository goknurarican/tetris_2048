import sys

import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np



class GameGrid:
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles locked on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.current_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(90, 19, 59)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness


        self.score = 0 # score object
        self.winner = None
        self.doubled = False # first double'ing the tiles
        self.quadrupled = False # second double
        self.game_won = False



    # A method for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None
        # (the case when the game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(250)

        self.draw_score() #calls the draw_core function to display the overall score

    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # if the current grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    # draw this tile
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the game grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game gridhod for drawing the cells and the lines of the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value


    # A method used checking whether the grid cell with the given row and column
    # indexes is occupied by a tile or not (i.e., empty)
    def is_occupied(self, row, col):
        # considering the newly entered tetrominoes to the game grid that may
        # have tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False  # the cell is not occupied as it is outside the grid
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # A method that locks the tiles of a landed tetromino on the grid checking
    # if the game is over due to having any tile above the topmost grid row.
    # (This method returns True when the game is over and False otherwise.)
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile (occupied cell) onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the value of the game_over flag
        self.clear_and_move_down_rows()
        return self.game_over

################################################################################

# method to draw the current score on the right-top side of the game canvas
    def draw_score(self):
        #text properties of the score
        stddraw.setFontSize(28)
        stddraw.setPenColor(stddraw.YELLOW)
        stddraw.setFontFamily("Arial")

        # defining the position of the score text on the canvas
        score_pos_x = self.grid_width - 1.5
        score_pos_y = self.grid_height - 1
        stddraw.text(score_pos_x, score_pos_y, "score: " + str(self.score))

#method to update the score
    def update_score(self, points):
        self.score += points #add the points to the current score

         # double the tile values if the overall score exceeds a certain threshold
        if self.score >= 200 and not self.doubled:
            self.double_tiles_value() #uses the double_tiles_value method to double each tile's value
            self.doubled = True  # mark as doubled

        elif self.score >= 16000 and not self.quadrupled:
            self.double_tiles_value()
            self.quadrupled = True  # mark as quadrupled


# a method for deleting the hanging/floating free tiles and adding the value of these tiles to score
    def delete_free_tiles_and_update_score(self):
        for col in range(self.grid_width): # scan each column for free tile
            conqat = [False] * self.grid_height #initialize a list to keep track of 4-connected tiles

            # scan from botom to tpo to find the first conqateneted tile
            for row in range(self.grid_height - 1, -1, -1):
                if self.tile_matrix[row][col] is not None:
                    if row == self.grid_height - 1 or conqat[row + 1]: #if the current tile is connected, mark it as connected
                        conqat[row] = True
                    else:
                        # if it is not connected, thern it is a free tile. and it needs to be removed
                          # and its value needs to be added up to the overall score
                        self.update_score(self.tile_matrix[row][col].number)
                        self.tile_matrix[row][col] = None


#method to clear full rows and move down the rows above
    def clear_and_move_down_rows(self):
        rows_cleared = 0
        for row in range(self.grid_height):
            if all(self.tile_matrix[row]):  # Check if the row is fully occupied
                rows_cleared += 1
            elif rows_cleared > 0:  # Move rows down if any rows were cleared above
                self.tile_matrix[row - rows_cleared] = self.tile_matrix[row].copy()
                self.tile_matrix[row] = [None] * self.grid_width  # Clear the current row as it has been moved down

        # Update the score based on the number of rows cleared
        self.score += rows_cleared * 100

#method to merge tiles of the same value that are on top of each other- from top to bottom

    def merge_tiles(self):
        for col in range(self.grid_width):
            row = 0  # start from the bottom row
            while row < self.grid_height - 1:  # check toward the top-most row
                current_tile = self.tile_matrix[row][col]
                above_tile = self.tile_matrix[row + 1][col]

                # if the values are the same, start merging
                if current_tile is not None and above_tile is not None:
                    if current_tile.number == above_tile.number:
                        merged_number = current_tile.number * 2
                        current_tile.number = merged_number
                        self.tile_matrix[row + 1][col] = None  # remove the top-most tile
                        self.update_score(merged_number)  #update the score

                        # move down tiles above
                        for r in range(row + 1, self.grid_height - 1):
                            self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
                        self.tile_matrix[self.grid_height - 1][col] = None
                row += 1  # move to the next tile
        self.check_win()


    #method to label components for identification of connected groups of tiles

    def label_components(self):
        label_count = 1
        labels = {}

        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.tile_matrix[row][col] is not None and (row, col) not in labels:
                    self.flood_fill(row, col, label_count, labels)
                    label_count += 1
        return labels

    # helper method to perform flood fill for the label_components method

    def flood_fill(self, row, col, label, labels):
        # dfs with the use of stack
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) not in labels and self.tile_matrix[r][c] is not None:
                labels[(r, c)] = label
                # adding-up the neighbour tiles to the stack
                if r > 0: stack.append((r - 1, c))
                if r < self.grid_height - 1: stack.append((r + 1, c))
                if c > 0: stack.append((r, c - 1))
                if c < self.grid_width - 1: stack.append((r, c + 1))


#method to move down components based on labels assigned by label_components

    def move_down_components(self, labels):
        for label in set(labels.values()):
            # only checks the bottom-empty tiles
            component = [loc for loc, lbl in labels.items() if lbl == label]
            min_row = min(r for r, c in component)
            if min_row == 0 or all(self.tile_matrix[r - 1][c] is not None for r, c in component):
                continue
            for r, c in component:
                self.tile_matrix[r][c], self.tile_matrix[r - 1][c] = None, self.tile_matrix[r][c]


# method to double the value of all tiles on the grid

    def double_tiles_value(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:  # if there exist a tile
                    self.tile_matrix[row][col].number *= 2
                    self.tile_matrix[row][col].update_colors()

#inci
    def check_win(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None and self.tile_matrix[row][col].number == 2048:
                    self.game_won = True
                    self.draw_game_won()
                    return True
        return False # shows gui

    def draw_game_won(self):
        # Continuously update the game screen until an action is taken
        while True:
            stddraw.clear(self.empty_cell_color)
            stddraw.setFontSize(30)
            stddraw.setFontFamily("Arial")
            stddraw.setPenColor(stddraw.YELLOW)
            stddraw.text(self.grid_width / 2, self.grid_height / 2 + 3, "Congratulations! You reached 2048!")

            # Define button properties
            button_width = self.grid_width / 4
            button_height = 2
            button_spacing = 3

            # Draw Restart button
            restart_button_x = self.grid_width / 2 - button_width / 2
            restart_button_y = self.grid_height / 2 - button_spacing
            stddraw.setPenColor(Color(25, 255, 228))
            stddraw.filledRectangle(restart_button_x, restart_button_y, button_width, button_height)
            stddraw.setPenColor(Color(31, 160, 239))
            stddraw.text(restart_button_x + button_width / 2, restart_button_y + button_height / 2, "Restart")

            # Draw Exit button
            exit_button_x = self.grid_width / 2 - button_width / 2
            exit_button_y = self.grid_height / 2 - 2 * button_spacing
            stddraw.setPenColor(Color(25, 255, 228))
            stddraw.filledRectangle(exit_button_x, exit_button_y, button_width, button_height)
            stddraw.setPenColor(Color(31, 160, 239))
            stddraw.text(exit_button_x + button_width / 2, exit_button_y + button_height / 2, "Exit")

            stddraw.show(50)

            if stddraw.mousePressed():
                mx, my = stddraw.mouseX(), stddraw.mouseY()

                # Restart button logic
                if restart_button_x <= mx <= restart_button_x + button_width and restart_button_y <= my <= restart_button_y + button_height:
                    print("Restart button clicked.")
                    self.reset_game()
                    break

                # Exit button logic
                elif exit_button_x <= mx <= exit_button_x + button_width and exit_button_y <= my <= exit_button_y + button_height:
                    print("Exit button clicked.")
                    sys.exit()  # Use sys.exit() to close the application

    def reset_game(self):
        # Reset all necessary game variables to their initial states
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.tile_matrix = np.full((self.grid_height, self.grid_width), None)
        self.display()  # Redraw the game grid with the initial state


pass