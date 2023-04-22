import ctypes

from sys import platform
from classes import City, Settings
from functions import setup_dataframe, setup_cities, setup_projection, pygame_loop 


def main():
    #check for OS
    if platform == "win32":
        ctypes.windll.user32.SetProcessDPIAware()

    # setup the settings 
    bg_color = (0, 0, 0)
    fg_color = (255, 255, 255)
    padding_percentage = 0.05
    screen_width = 1280
    screen_height = 960

    settings = Settings(screen_width, screen_height, bg_color, fg_color, padding_percentage, 60)

    df = setup_dataframe()
    cities = setup_cities(df, City)
    setup_projection(settings, cities)
    pygame_loop(settings, cities)

if __name__ == '__main__':
    main()
