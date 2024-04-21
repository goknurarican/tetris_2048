import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles


class Tile:
    boundary_thickness = 0.004
    font_family, font_size = "Arial", 14
    number_to_color = {
        2: Color(255, 224, 214),  # Light red for 2
        4: Color(255, 204, 188),  # Light coral for 4
        8: Color(255, 174, 150),  # Salmon for 8
        16: Color(255, 144, 122),  # Dark salmon for 16
        32: Color(255, 114, 94),  # Crimson for 32
        64: Color(255, 84, 66),   # Red-orange for 64
        128: Color(255, 64, 54),  # Red for 128
        256: Color(235, 52, 52),  # Dark red for 256
        512: Color(215, 42, 42),  # Darker red for 512
        1024: Color(195, 32, 32), # Deep red for 1024
        2048: Color(175, 22, 22), # Firebrick for 2048
    }
    def __init__(self, number):
        self._number = number
        self.update_colors()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        self.update_colors()  # Update colors whenever the number changes

    def update_colors(self):
        if self.number in self.number_to_color:
            self.background_color = self.number_to_color[self.number]
        else:
            self.background_color = Color(205, 193, 180)  # Default color for unspecified numbers

        # Set the foreground color based on the number for readability
        if self.number > 4:
            self.foreground_color = Color(249, 246, 242)  # Lighter color for text on dark backgrounds
        else:
            self.foreground_color = Color(119, 110, 101)  # Darker color for text on light backgrounds

        # Set the box color as a constant
        self.box_color = Color(187, 173, 160)

    def draw(self, position, length=1):
        # Draw the tile with the specified colors and text
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # Reset the pen radius to default
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(self.font_family)
        stddraw.setFontSize(self.font_size)
        stddraw.text(position.x, position.y, str(self.number))
