#!/usr/bin/python3

"""Square clicking in classic PyGame

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   This is a reference implementation to be replaced by
   an implementation utilising planes.
"""

# This file is part of planes.
#
# planes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# planes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with planes.  If not, see <http://www.gnu.org/licenses/>.

# work started on 01. Oct 2010

import pygame
from collections import deque

def main():
	pygame.init()

	print("setting up clock")
	clock = pygame.time.Clock()

	# distance from border
	#
	distance = 25

	# main screen
	#
	print("creating surface")
	screen_surface = pygame.display.set_mode((400, 300))

	# square sprite setup
	#
	print("sprite setup")
	square = pygame.sprite.Sprite()

	square.image = pygame.Surface((50, 50))
	square.rect = pygame.Rect((distance, distance), (50, 50))

	# custom extensions for movement, color, dragging
	#
	square.vector = (1, 0)
	square.colors = deque([(255, 128, 0), (0, 255, 128), (0, 0, 255)])
	square.drag = False

	# dropzone setup
	#
	print("drop zone setup")

	dropzone = pygame.sprite.Sprite()

	dropzone.image = pygame.Surface((200, 100))
	dropzone.image.fill((0, 0, 128))

	dropzone.rect = pygame.Rect((100, 100), (200, 100))

	# main loop
	#
	print("starting main loop")

	while True:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				print("got pygame.QUIT, terminating")
				raise SystemExit

			elif (event.type == pygame.MOUSEBUTTONDOWN
			and event.button == 1
			and square.rect.collidepoint(event.pos)):
				print("square clicked, starting to drag")
				square.drag = True

			elif (event.type == pygame.MOUSEBUTTONUP
			and event.button == 1
			and square.rect.collidepoint(event.pos)):
				print("mouse released on square, stopping to drag")
				square.drag = False
				square.colors.rotate(-1)

		if square.drag:
			print("square is dragged, following mouse")
			square.rect.center = pygame.mouse.get_pos()

		elif dropzone.rect.collidepoint(square.rect.center):
			print("square in drop zone, no animation")

			if not dropzone.rect.contains(square.rect):
				square.rect.clamp_ip(dropzone.rect)
				print("*snap*")

		else:
			if square.rect.top > (300 - square.rect.width - distance):

				square.rect.top = 300 - square.rect.width - distance

				# turn left
				#
				square.vector = (-1, 0)

			if square.rect.left > (400 - square.rect.width - distance):

				square.rect.left = 400 - square.rect.width - distance

				# turn down
				#
				square.vector = (0, 1)

			if square.rect.top < distance:

				square.rect.top = distance

				# turn right
				#
				square.vector = (1, 0)

			if square.rect.left < distance:

				square.rect.left = distance

				# turn up
				#
				square.vector = (0, -1)

			square.rect.move_ip(square.vector[0], square.vector[1])

		square.image.fill(square.colors[0])

		screen_surface.fill((0, 128, 0))
		screen_surface.blit(dropzone.image, dropzone.rect)
		screen_surface.blit(square.image, square.rect)
		pygame.display.flip()

		# run at 60 fps
		#
		clock.tick(60)
		#print(clock.get_fps())

if __name__ == "__main__":
	main()
