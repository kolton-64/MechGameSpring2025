import pygame as pg

def load_background_image(filename, width, height):
    """
    Loads and scales the background image to fit the game screen.
    filename: The path to the background image file.
    width: The width to scale the image to.
    height: The height to scale the image to.
    returns The scaled background image.
    """
    image = pg.image.load(filename)
    image = pg.transform.scale(image, (width, height))
    return image
'''
this neeeds to be what the main loop looks like to now load the image
background_image = load_background_image('backgroundFight.jpeg', 1280, 720)

    while True:
        screen.blit(background_image, (0, 0))
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                   	'''
