import pandas as pd
import pygame as pg
import math
import random

from geoname_columns import geoname_columns

def setup_dataframe():
    # open a text file as csv with tab as separator and UTF-8 encoding
    path = 'res/RO.txt'
    df_ro = pd.read_csv(path, sep='\t', encoding='utf-8')

    path = 'res/MD.txt'
    df_md = pd.read_csv(path, sep='\t', encoding='utf-8')

    # rename the columns
    df_ro.columns = geoname_columns
    df_md.columns = geoname_columns

    # remove entries where the population is 0 from Romania 
    # I suspect that the population data for Moldova is not accurate
    df_ro = df_ro[df_ro['population'] != 0]

    # merge the two dataframes
    df = pd.concat([df_ro, df_md])

    # keep columns name, population, longitude and latitude
    df = df[['name', 'population', 'longitude', 'latitude']]

    return df


def mercator_projection(latitude, longitude):
    # convert latitude and longitude to radians
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)

    # calculate x and y coordinates
    x = 6378137 * longitude
    y = 6378137 * math.log(math.tan(math.pi / 4 + latitude / 2))

    return x, y


def setup_cities(df, City):
    # create a list of cities
    cities = []

    # add the cities to the list
    for index, row in df.iterrows():
        cities.append(City(row['name'], row['population'], row['longitude'], row['latitude']))

    return cities

# setup the projection, accounting for the fact that in pygame the origin is in the top left corner
def setup_projection(settings, cities):
    # setup the projection
    for city in cities:
        city.x_coordinate, city.y_coordinate = mercator_projection(city.latitude, city.longitude)

    # find the minimum and maximum x and y coordinates
    min_x = min(city.x_coordinate for city in cities)
    max_x = max(city.x_coordinate for city in cities)
    min_y = min(city.y_coordinate for city in cities)
    max_y = max(city.y_coordinate for city in cities)

    # calculate the width and height of the map
    width = max_x - min_x
    height = max_y - min_y

    # calculate the scale
    scale = settings.padded_width / width

    # calculate the offset
    offset_x = -min_x * scale
    offset_y = -min_y * scale

    # apply the scale and lift the coordinates upwards
    correction_pixels = 25
    for city in cities:
        city.x_coordinate = city.x_coordinate * scale + offset_x
        city.y_coordinate = settings.padded_height - (city.y_coordinate * scale + offset_y) - correction_pixels # flip the y coordinate and center on the y axis


def pygame_loop(settings, cities):
    pg.init()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    screen.fill(settings.bg_color)
    pg.display.set_caption('Catană Ioan-Alexandru : PyGame visualization project : Cities in Romania and Moldova')

    clock = pg.time.Clock()

    font = pg.font.Font('font/Monocraft.ttf', 14)
    border_text = font.render('Catană Ioan-Alexandru', True, (255, 255, 255))
    border_text_x = (settings.screen_width - settings.padded_width) / 2 + 10
    screen.blit(border_text, (border_text_x, 10))

    while True:
        # check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                # when the spacebar is pressed, the background changes to a random color
                if event.key == pg.K_SPACE:
                    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    settings.bg_color = random_color
                    settings.fg_color = (255-random_color[0], 255-random_color[1], 255-random_color[2])

        # setup a surface for the map
        map_surface = pg.Surface((settings.padded_width, settings.padded_height))

        # draw the map
        map_surface.fill(settings.bg_color)

        # draw the cities
        for city in cities:
            pg.draw.circle(map_surface, settings.fg_color, (int(city.x_coordinate), int(city.y_coordinate)), 1)

        # setup custom font and text-related variables
        title_text = "Localities in Romania and Moldova"
        bg_color_info_text = f"Current background color: {settings.bg_color}"
        fg_color_info_text = f"Current foreground color: {settings.fg_color}"
        
        # draw the title and the info text
        title = font.render(title_text, True, settings.fg_color)
        bg_color_info = font.render(bg_color_info_text, True, settings.fg_color)
        fg_color_info = font.render(fg_color_info_text, True, settings.fg_color)
        map_surface.blit(title, (10, 10))
        map_surface.blit(bg_color_info, (10, 30))
        map_surface.blit(fg_color_info, (10, 50))

        # draw the words "Press space to change the background color" in the bottom left corner
        text = font.render("Press space to change the background color", True, settings.fg_color)
        map_surface.blit(text, (10, settings.padded_height - 20))

        screen.blit(map_surface, (settings.screen_width * settings.padding_percentage, settings.screen_height * settings.padding_percentage))
        # update the display
        pg.display.update()

        clock.tick(settings.framerate)
