import pygame

window = pygame.display.set_mode((784, 784))

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()

pygame.quit()