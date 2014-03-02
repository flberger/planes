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

WINDOW = planes.Display((800, 600))

def display_fonts(scale):
    """Add planes with font examples.
       `scale` is a float giving the scaling factor.
    """

    line_height = 40
    ypos = 30

    print("Re-displaying with scale {0}".format(scale))

    # TODO: Using _font_dict. Use new API once it exists.
    #
    for i, font_name in enumerate(planes.gui.FONTS._font_dict.keys()):

        # Using default font for display

        number_label = planes.gui.Label("num{0}-{1}".format(i, scale),
                                        '{0}'.format(i + 1),
                                      pygame.Rect((10, ypos),
                                                  (30, line_height)),
                                      text_color = (255, 255, 255))

        name_label = planes.gui.Label("desc{0}-{1}".format(i, scale),
                                      '"{0}"'.format(font_name),
                                      pygame.Rect((40 + 2, ypos),
                                                  (200, line_height)),
                                      text_color = (255, 255, 255))

        px_label = planes.gui.Label("px{0}-{1}".format(i, scale),
                                    '{0} px'.format(planes.gui.FONTS._font_dict[font_name][1] * scale),
                                    pygame.Rect((240 + 2 * 2, ypos),
                                                (40, line_height)),
                                    text_color = (255, 255, 255))

        font_label = planes.gui.Label("font{0}-{1}".format(i, scale),
                                      "The Quick Brown Fox Jumps Over The Lazy Dog 12345 CAPS",
                                      pygame.Rect((280 + 3 * 2, ypos),
                                                  (500, line_height)),
                                      text_color = (255, 255, 255),
                                      font = planes.gui.FONTS.by_name(font_name,
                                                                      scale))

        print("adding '{0}'".format(font_name))

        WINDOW.sub(number_label)
        WINDOW.sub(name_label)
        WINDOW.sub(px_label)
        WINDOW.sub(font_label)

        ypos += line_height + 2

    return

def mainloop(framerate):
    """Runs a pygame / planes main loop.
       framerate is the framerate.
       This must be run in the main thread, otherwise pygame.event will not
       receive any events under MS Windows.
    """

    print("about to start main loop")

    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                print("got pygame.QUIT, terminating in mainloop()")
                pygame.quit()
                raise SystemExit

        WINDOW.process(events)
        WINDOW.update()
        WINDOW.render()

        pygame.display.flip()

        # Slow down to framerate given
        #
        clock.tick(framerate)

    return

def main():
    """Main method.
    """
    WINDOW.image.fill((127, 127, 127))

    pygame.display.set_caption("planes Font Demo")

    plus_minus_box = planes.gui.PlusMinusBox("scale_pmbox", 2, value = 1)

    plus_minus_box.rect.topleft = (10, 10)

    def decrease_scale(plane):

        # Call default
        #
        planes.gui.PlusMinusBox.minus_callback(plane.parent, plane)

        display_fonts(int(plus_minus_box.textbox.text))

        return

    def increase_scale(plane):

        # Call default
        #
        planes.gui.PlusMinusBox.plus_callback(plane.parent, plane)

        display_fonts(int(plus_minus_box.textbox.text))

        return

    plus_minus_box.minus.left_click_callback = decrease_scale
    plus_minus_box.plus.left_click_callback = increase_scale

    WINDOW.sub(plus_minus_box)

    display_fonts(1)

    print("starting main loop in main thread")

    try:
        mainloop(60)

    except:
        print("Exception in mainloop():")
        print(traceback.format_exc())
        pygame.quit()
        raise SystemExit

    return

if __name__ == "__main__":

    main()
