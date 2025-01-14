'''
***************************COLLABORATORS******************************
Korbin, Kyle, Kolton, James

*****************************CITATION*********************************
Game mechanic inspirtation - Slay the Spire
Graphic inspiration - WarHammer
PyGame learning - 
	Video: The ultimate introduction to Pygame, 
	Channel: Clear Code
	Link: https://youtu.be/AY9MnQ4x3zk?si=gvivndXhupNE7cak

'''

def main():
	import pygame as pg
	from sys import exit

	pg.init()
	screen = pg.display.set_mode((1280,720), pg.NOFRAME)
	pg.display.set_caption('Runner')
	clock = pg.time.Clock()

	while True:
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

		pg.display.update()
		clock.tick(60)
		

if __name__ == '__main__':
	main()
