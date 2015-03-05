"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
     # Get the length of line
    length = len(line)
    
    # Create two empty lists
    output = [0] * length
    result = [0] * length
    
    index_output = 0
    
    for index_line in range(length):
        if line[index_line] != 0:
            output[index_output] = line[index_line]
            index_output += 1
            
    for index_output in range(1, length):
        if output[index_output] == output[index_output-1]:
            output[index_output-1] *= 2
            output[index_output] = 0
    
    index_result = 0
    for index_output in range(length):
        if output[index_output] != 0:
            result[index_result] = output[index_output]
            index_result += 1
            
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_tiles_dictionary = {UP: [(0, col) for col in range(self._grid_width)],
                                         DOWN: [(self._grid_height-1, col) for col in range(self._grid_width)],
                                         LEFT: [(row, 0) for row in range(self._grid_height)],
                                         RIGHT:[ (row, self._grid_width-1) for row in range(self._grid_height)]}
        
        self.reset()

        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        dummy_row = self._grid_height
        dummy_col = self._grid_width
        self._cells = [ [0 for dummy_col in range(self._grid_width)] 
                          for dummy_row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._cells)
            
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        func = lambda direction: self._grid_height if direction == UP or direction == DOWN else self._grid_width
        steps = func(direction)
        
        for (row, col) in self._initial_tiles_dictionary[direction]:
                template_list = []
                for step in range(steps):
                    traverse_row = row + OFFSETS[direction][0] * step
                    traverse_col = col + OFFSETS[direction][1] * step
                    #print (traverse_row, traverse_col)
                    template_list.append(self._cells[traverse_row][traverse_col])
                
                template_list = merge(template_list)  
                #print template_list
                for step in range(steps):
                    traverse_row = row + OFFSETS[direction][0] * step
                    traverse_col = col + OFFSETS[direction][1] * step
                    self._cells[traverse_row][traverse_col] = template_list[step]
        
        
        self.new_tile()
                   

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
     
        empty_items = []
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.get_tile(row, col) == 0:
                    empty_items.append((row, col))
        
        random_row = 0
        random_col = 0
        if len(empty_items) != 0:
            random_empty_tile = random.randrange(0, len(empty_items))
            (random_row, random_col) = empty_items[random_empty_tile]
        else:
            return
        # the % of getting "4" from 0~9 is 10%
        random_time = random.randrange(0, 10)
        
        if random_time == 4:
            self._cells[random_row][random_col] = 4
        else:
            self._cells[random_row][random_col] = 2
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._cells[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
