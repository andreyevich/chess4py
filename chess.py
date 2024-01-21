import pygame

window = pygame.display.set_mode((784, 784))
board_img = pygame.image.load('rect-8x8.png')
selected_sqr_img = pygame.image.load('selected-square.png')
available_sqr_img = pygame.image.load('available-square.png')
sqr_size = {'x': 96, 'y': 96}
border_width = 8
border_height = border_width

class Piece:
	def __init__(self, y, x, piece_type, color):
		self.y = y
		self.x = x
		self.type = piece_type
		self.color = color
		self.selected = False
		self.sqr = pygame.Rect(self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])

		self.img = pygame.image.load(f'{color}-{piece_type}.png')
		self.img = pygame.transform.scale(self.img, (sqr_size['x'], sqr_size['y']))

	def draw(self, pieces_matrix):
		if self.selected:
			window.blit(selected_sqr_img, (self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height))

			moves = self.available_moves(pieces_matrix)

			for move in moves:
				window.blit(available_sqr_img, (move[1] * sqr_size['x'] + border_width, move[0] * sqr_size['y'] + border_height))

		window.blit(self.img, (self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height))

	def update(self, event):
		self.sqr = pygame.Rect(self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])
		moves = self.available_moves(pieces_matrix)

		if event == None:
			return

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.sqr.collidepoint(pygame.mouse.get_pos()):
				self.selected = not self.selected
			elif self.selected:
				for move in moves:
					sqr = pygame.Rect(move[1] * sqr_size['x'] + border_width, move[0] * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])

					if sqr.collidepoint(pygame.mouse.get_pos()):
						self.y = move[0]
						self.x = move[1]
					self.selected = False


	# Returns the available moves a piece can do in the form [(y, x)]
	def available_moves(self, pieces_matrix):
		return []

class Rook(Piece):
	def available_moves(self, pieces_matrix):
		moves = []

		for y in range(self.y + 1, 8):
			if pieces_matrix[y][self.x] == None:
				moves.append((y, self.x))
			else:
				break

		for y in range(self.y - 1, -1, -1):
			if pieces_matrix[y][self.x] == None:
				moves.append((y, self.x))
			else:
				break

		for x in range(self.x + 1, 8):
			if pieces_matrix[self.y][x] == None:
				moves.append((self.y, x))
			else:
				break

		for x in range(self.x - 1, -1, -1):
			if pieces_matrix[self.y][x] == None:
				moves.append((self.y, x))
			else:
				break

		return moves

pieces = [
	Rook(0, 0, 'rook', 'black'),
	Rook(0, 7, 'rook', 'black'),
	Rook(7, 0, 'rook', 'white'),
	Rook(7, 7, 'rook', 'white')
]
pieces_matrix = []

for y in range(0, 8):
	pieces_matrix.append([])
	for x in range(0, 8):
		pieces_matrix[y].append(None)

for piece in pieces:
	pieces_matrix[piece.y][piece.x] = piece

running = True
while running:
	event = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	window.blit(board_img, (0, 0))

	for piece in pieces:
		piece.draw(pieces_matrix)

	for piece in pieces:
		piece.update(event)

	pygame.display.update()

pygame.quit()