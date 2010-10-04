"""Square clicking using Click'n'Drag

   (c) Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

# work started on 03. Oct 2010

import clickndrag
import pygame
from collections import deque

class ColorChangeSquare(clickndrag.Plane):

	def __init__(self, name, rect):

		clickndrag.Plane.__init__(self, name, rect)

		# custom extensions for movement, color
		#
		self.moving = True
		self.vector = (1, 0)
		self.colors = deque([(255, 128, 0), (0, 255, 128), (0, 0, 255)])

		self.image.fill(self.colors[0])

	def clicked(self):
		self.colors.rotate(-1)
		self.image.fill(self.colors[0])

	def update(self):

		if self.rect.top > (300 - self.rect.width - 25):

			self.rect.top = 300 - self.rect.width - 25

			# turn left
			#
			self.vector = (-1, 0)

		if self.rect.left > (400 - self.rect.width - 25):

			self.rect.left = 400 - self.rect.width - 25

			# turn down
			#
			self.vector = (0, 1)

		if self.rect.top < 25:

			self.rect.top = 25

			# turn right
			#
			self.vector = (1, 0)

		if self.rect.left < 25:

			self.rect.left = 25

			# turn up
			#
			self.vector = (0, -1)

		if self.moving:
			self.rect.move_ip(self.vector[0], self.vector[1])

class DropZone(clickndrag.Plane):

	def dropped_upon(self, plane, coordinates):

		clickndrag.Plane.dropped_upon(self, plane, coordinates)

		plane.moving = False

class DropDisplay(clickndrag.Display):

	def dropped_upon(self, plane, coordinates):

		if isinstance(plane, ColorChangeSquare):

			clickndrag.Display.dropped_upon(self, plane, coordinates)

			plane.moving = True

def main():
	pygame.init()
	clickndrag.init(pygame)

	print("setting up clock")
	clock = pygame.time.Clock()

	# main screen
	#
	print("creating main screen")
	screen = DropDisplay((400, 300))
	screen.grab_dropped_planes = True
	screen.image.fill((0, 128, 0))

	# square sprite setup
	#
	print("square setup")
	screen.sub(ColorChangeSquare("square", pygame.Rect((25, 25), (50, 50))))

	# dropzone setup
	#
	print("drop zone setup")
	screen.sub(DropZone("dropzone", pygame.Rect((100, 100), (200, 100))))
	screen.dropzone.draggable = False
	screen.dropzone.grab_dropped_planes = True
	screen.dropzone.image.fill((0, 0, 128))

	# main loop
	#
	print("starting main loop")

	while True:
		events = pygame.event.get()

		for event in events:

			if event.type == pygame.QUIT:
				print("got pygame.QUIT, terminating")
				raise SystemExit

		screen.process(events)
		screen.update()
		screen.render()

		pygame.display.flip()

		# run at 60 fps
		#
		clock.tick(60)
		#print(clock.get_fps())

if __name__ == "__main__":
	main()
