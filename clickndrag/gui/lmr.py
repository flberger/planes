"""lmr - Left-Mid-Right Background Styles for clickndrag.gui widgets.

   Copyright 2012 Florian Berger <fberger@florian-berger.de>
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

# work started on 27. Feb 2012

import clickndrag.gui
import pygame
import os.path

class LMRStyle:
    """This class encapsulates the left, mid and right images to be used as widget background.

       Attributes:

       LMRStyle.left_img
           A Pygame Surface, holding the left edge of the background image.

       LMRStyle.mid_img
           A Pygame Surface, holding the middle part of the background image.
           A widget might repeat this image to fit the desired width.

       LMRStyle.right_img
           A Pygame Surface, holding the right edge of the background image.
    """

    def __init__(self, left_img, mid_img, right_img):
        """Initialise.
           left_img, mid_img and right_img are the respective image file names.
        """

        self.left_img = pygame.image.load(left_img).convert_alpha()

        self.mid_img = pygame.image.load(mid_img).convert_alpha()

        self.right_img = pygame.image.load(right_img).convert_alpha()

        return

class LMRButton(clickndrag.gui.Button):
    """A clickndrag.gui.Button with LMR background.

       Additional attributes:

       LMRButton.background
           A Pygame Surface, holding the rendered background for this button.

       Doctest:

       >>> display = clickndrag.Display((300, 300))
       >>> display.image.fill((128, 128, 128))
       <rect(0, 0, 300, 300)>
       >>> style = LMRStyle(os.path.join(os.path.dirname(__file__), "button-l.png"),
       ...                  os.path.join(os.path.dirname(__file__), "button-m.png"),
       ...                  os.path.join(os.path.dirname(__file__), "button-r.png"))
       >>> def exit(plane):
       ...     pygame.quit()
       ...     raise SystemExit
       >>> button = LMRButton("LMRButton", exit, style)
       >>> button.rect.center = display.rect.center
       >>> display.sub(button)
       >>> clock = pygame.time.Clock()
       >>> while True:
       ...     events = pygame.event.get()
       ...     display.process(events)
       ...     display.update()
       ...     display.render()
       ...     pygame.display.flip()
       ...     clock.tick(30)
       Traceback (most recent call last):
           ...
       SystemExit
    """

    def __init__(self, label, callback, style):
        """Initialise the Button.
        """

        if not isinstance(style, LMRStyle):

            msg = "'style' argument must be of class 'LMRStyle', not '{0}'"

            raise TypeError(msg.format(style.__class__.__name__))

        # Compute dimensions
        #
        height = style.left_img.get_height()

        # We need it a couple of times
        #
        left_width = style.left_img.get_width()

        mid_width = len(label) * clickndrag.gui.PIX_PER_CHAR

        width = left_width + mid_width + style.right_img.get_width()

        # Create background image
        # Default to SRCALPHA.
        #
        self.background = pygame.Surface((width, height),
                                         flags = pygame.SRCALPHA).convert_alpha()

        self.background.blit(style.left_img, (0, 0))

        # Python: this creates a copy
        #
        x = left_width

        mid_img_width = style.mid_img.get_width()

        while x < (left_width + mid_width):

            self.background.blit(style.mid_img, (x, 0))

            x += mid_img_width

        # Clear area for right edge
        #
        self.background.fill((0, 0, 0, 0, ),
                             rect = pygame.Rect((left_width + mid_width, 0),
                                                style.right_img.get_size()))

        self.background.blit(style.right_img, (left_width + mid_width, 0))

        # Now call base class.
        # This will also call redraw().
        #
        clickndrag.gui.Button.__init__(self,
                                       label,
                                       pygame.Rect((0, 0), (width, height)),
                                       callback)

        return

    def redraw(self):
        """Conditionally redraw the Button.
        """

        # Partly copied from Label.redraw()
        #
        if self.text != self.cached_text:

            # Copy, don't blit, taking care for transparency
            #
            self.image = self.background.copy()

            # Text is centered on rect.
            #
            fontsurf = clickndrag.gui.SMALL_FONT.render(self.text,
                                                        True,
                                                        (0, 0, 0))

            centered_rect = fontsurf.get_rect()

            # Get a neutral center of self.rect
            #
            centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

            self.image.blit(fontsurf, centered_rect)

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text

        return
