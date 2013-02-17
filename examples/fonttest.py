#!/usr/bin/python3

"""Demo planes.gui.Fonts

   Copyright 2012 Florian Berger <fberger@florian-berger.de>
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

# work started on 27. December 2012

import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import planes.gui
import traceback

print("creating window")

window = planes.Display((800, 600))
window.image.fill((127, 127, 127))
pygame.display.set_caption("planes Font Demo")

# Display fonts
#
line_height = 27
ypos = 10

for scale in (1, 2):

    for i, font_name in enumerate(planes.gui.FONTS.font_names):

        # Using default font for display
        #
        name_label = planes.gui.Label("desc{0}-{1}".format(i, scale),
                                      '{0}/{1}: "{2}"'.format(i + 1,
                                                              len(planes.gui.FONTS.font_names),
                                                              font_name),
                                      pygame.Rect((10, ypos),
                                                  (300, line_height)),
                                      text_color = (255, 255, 255))

        font_label = planes.gui.Label("font{0}-{1}".format(i, scale),
                                      "The Quick Brown Fox Jumps Over The Lazy Dog",
                                      pygame.Rect((320, ypos),
                                                  (440, line_height)),
                                      text_color = (255, 255, 255),
                                      font = planes.gui.FONTS.by_name(font_name,
                                                                      scale))

        print("adding '{0}'".format(font_name))

        window.sub(name_label)
        window.sub(font_label)

        ypos += line_height + 2

clock = pygame.time.Clock()
fps = clock.get_fps

def mainloop(framerate):
    """Runs a pygame / planes main loop.
       framerate is the framerate.
       This must be run in the main thread, otherwise pygame.event will not
       receive any events under MS Windows.
    """

    print("about to start main loop")

    while True:
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                print("got pygame.QUIT, terminating in mainloop()")
                pygame.quit()
                raise SystemExit

        window.process(events)
        window.update()
        window.render()

        pygame.display.flip()

        # Slow down to framerate given
        #
        clock.tick(framerate)

if __name__ == "__main__":

    print("starting main loop in main thread")

    try:
        mainloop(60)

    except:
        print("Exception in mainloop():")
        print(traceback.format_exc())
        pygame.quit()
        raise SystemExit
