import pygame

window = pygame.display.set_mode((784, 784))
board_img = pygame.image.load('rect-8x8.png')
sqr_size = {'x': 96, 'y': 96}
border_width = 8
border_height = border_width

class Piece:
	def __init__(self, y, x, piece_type, color):
		self.y = y
		self.x = x
		self.type = piece_type
		self.color = color

		self.img = pygame.image.load(f'{color}-{piece_type}.png')
		self.img = pygame.transform.scale(self.img, (sqr_size['x'], sqr_size['y']))

	def draw(self):
		window.blit(self.img, (self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height))

class Rook(Piece):
	pass

pieces = [Rook(0, 0, 'rook', 'black'), Rook(7, 7, 'rook', 'white')]
pieces_matrix = []

for y in range(0, 8):
	pieces_matrix.append([])
	for x in range(0, 8):
		pieces_matrix[y].append(None)

for piece in pieces:
	pieces_matrix[piece.y][piece.x] = piece

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	window.blit(board_img, (0, 0))

	for piece in pieces:
		piece.draw()

	pygame.display.update()

pygame.quit()