#!/usr/bin/python3

"""Square clicking using Click'n'Drag

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

# This file is part of clickndrag.
#
# clickndrag is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# clickndrag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with clickndrag.  If not, see <http://www.gnu.org/licenses/>.

# work started on 03. Oct 2010

import sys

# Add current and parent directory. One of them is supposed to contain the
# clickndrag package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import clickndrag
from collections import deque

class ColorChangeSquare(clickndrag.Plane):

	def __init__(self, name, rect, drag = False, grab = False):

		clickndrag.Plane.__init__(self, name, rect, drag, grab)

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
	screen.sub(ColorChangeSquare("square", pygame.Rect((25, 25), (50, 50)), drag = True))

	# dropzone setup
	#
	print("drop zone setup")
	screen.sub(DropZone("dropzone", pygame.Rect((100, 100), (200, 100)), drag = True, grab = True))
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
