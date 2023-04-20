# setup a class for the cities, containing the name, population, longitude and latitude
class City:
    def __init__(self, name, population, longitude, latitude):
        self.name = name
        self.population = population
        self.longitude = longitude
        self.latitude = latitude

        self.x_coordinate = 0
        self.y_coordinate = 0


class Settings:
    def __init__(self, screen_width, screen_height, bg_color, fg_color, padding_percentage, framerate):
        # screen settings
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.framerate = framerate

        # padding settings
        self.padding_percentage = padding_percentage

        self.padded_width = self.screen_width - (self.screen_width * self.padding_percentage * 2)   # padding on both sides
        self.padded_height = self.screen_height - (self.screen_height * self.padding_percentage * 2)