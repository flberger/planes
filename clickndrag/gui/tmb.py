"""tmb - clickndrag.gui widgets with top-mid-bottom backgrounds.

   Copyright 2012 Florian Berger <fberger@florian-berger.de>

   Module doctests:

   >>> display = clickndrag.Display((500, 300))
   >>> display.image.fill((128, 128, 128))
   <rect(0, 0, 500, 300)>
   >>> ok_box = TMBOkBox("Welcome to a TMBOkBox!", C_256_STYLE)
   >>> ok_box.rect.center = display.rect.center
   >>> display.sub(ok_box)
   >>> clock = pygame.time.Clock()
   >>> while True:
   ...     if not len(display.subplanes_list):
   ...         raise SystemExit
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

# TODO: GetStringDialog
# TODO: OptionSelector

import clickndrag.gui.lmr
import pygame
import os.path

class TMBStyle:
    """This class encapsulates the top, mid and bottom images to be used as widget background.

       Attributes:

       LMRStyle.top_img
           A Pygame Surface, holding the top edge of the background image.

       LMRStyle.mid_img
           A Pygame Surface, holding the middle part of the background image.
           A widget might repeat this image to fit the desired width.

       LMRStyle.bottom_img
           A Pygame Surface, holding the bottom edge of the background image.
    """

    def __init__(self, top_img, mid_img, bottom_img):
        """Initialise.
           top_img, mid_img and bottom_img are the respective image file names.
        """

        # TODO: convert_alpha() should be called as soon as a display is available.

        self.top_img = pygame.image.load(top_img)

        self.mid_img = pygame.image.load(mid_img)

        self.bottom_img = pygame.image.load(bottom_img)

        return

# Create some default styles
#
C_256_STYLE = TMBStyle(os.path.join(os.path.dirname(__file__), "resources", "container-256px-t.png"),
                       os.path.join(os.path.dirname(__file__), "resources", "container-256px-m.png"),
                       os.path.join(os.path.dirname(__file__), "resources", "container-256px-b.png"))

C_128_STYLE = TMBStyle(os.path.join(os.path.dirname(__file__), "resources", "container-128px-t.png"),
                       os.path.join(os.path.dirname(__file__), "resources", "container-128px-m.png"),
                       os.path.join(os.path.dirname(__file__), "resources", "container-128px-b.png"))


class TMBContainer(clickndrag.gui.Container):
    """A clickndrag.gui.Container with fixed width and TMB background.

       Additional attributes:

       TMBContainer.style
           An instance of TMBStyle.

       TMBContainer.background
           A Pygame Surface, holding the rendered background.
           Initially None, repainted in TMBContainer.sub().
    """

    def __init__(self, name, style, padding = 0):
        """Initialise.

           style is an instance of TMBStyle.
        """

        if not isinstance(style, TMBStyle):

            msg = "'style' argument must be of class 'TMBStyle', not '{0}'"

            raise TypeError(msg.format(style.__class__.__name__))

        # Call base
        #
        clickndrag.gui.Container.__init__(self, name, padding)

        self.style = style

        self.background = None

        # Initialise rect width. This is fixed to the background width.
        #
        self.rect.width = self.style.top_img.get_width()

        return

    def sub(self, plane):
        """Resize the container, update the position of plane and add it as a subplane.
           This will also repaint TMBContainer.background.
        """

        # Adapted from gui.Container method

        # First add the subplane by calling the base class method.
        # This also cares for re-adding an already existing subplane.
        #
        clickndrag.Plane.sub(self, plane)

        # Existing subplanes are already incorporated in self.rect.

        # We need it a couple of times
        #
        top_height = self.style.top_img.get_height()

        # Mandatory fit new height, observe padding
        #
        if not self.rect.height:

            # No subplanes yet

            plane.rect.topleft = (0, top_height)

            # No padding at the bottom
            #
            self.rect.height = top_height + plane.rect.height + self.style.bottom_img.get_height()

        else:
            # Padding between elements
            #
            plane.rect.topleft = (0, self.rect.height - self.style.bottom_img.get_height() + self.padding)

            self.rect.height = self.rect.height + self.padding + plane.rect.height

        # Center subplane.
        #
        plane.rect.centerx = self.rect.centerx

        # Recreate background
        # Default to SRCALPHA.
        #
        self.background = pygame.Surface(self.rect.size,
                                         flags = pygame.SRCALPHA).convert_alpha()

        self.background.blit(self.style.top_img, (0, 0))

        # Python: this creates a copy
        #
        y = top_height

        mid_img_height = self.style.mid_img.get_height()

        top_mid_height = self.rect.height - self.style.bottom_img.get_height()

        while y < (top_mid_height):

            self.background.blit(self.style.mid_img, (0, y))

            y += mid_img_height

        # Clear area for bottom edge
        #
        self.background.fill((128, 128, 128, 0),
                             rect = pygame.Rect((0, top_mid_height),
                                                self.style.bottom_img.get_size()))

        self.background.blit(self.style.bottom_img, (0, top_mid_height))

        self.redraw()

        return

    def redraw(self):
        """Redraw TMBContainer.image using TMBContainer.background.
           This also creates a new TMBContainer.rendersurface.
        """

        self.image = self.background.copy()

        self.rendersurface = self.image.copy()

        return

    def remove(self, plane_identifier):
        """Remove the subplane, then reposition remaining subplanes and resize the container.
        """

        # Adapted from gui.Container method

        # Accept Plane name as well as Plane instance
        #
        if isinstance(plane_identifier, clickndrag.Plane):

            name = plane_identifier.name

        else:
            name = plane_identifier

        # Save the height of the removed plane
        #
        height_removed = self.subplanes[name].rect.height + self.padding

        clickndrag.Plane.remove(self, name)

        # Reposition remaining subplanes.
        #
        top = self.style.top_img.get_height()

        for name in self.subplanes_list:
            rect = self.subplanes[name].rect
            rect.top = top
            top = top + rect.height + self.padding

        # Now shrink and redraw.
        #
        self.rect.height = self.rect.height - height_removed

        self.redraw()

        return

class TMBOkBox(TMBContainer, clickndrag.gui.OkBox):
    """A box which displays a message and an OK button over a TMB background.
       It is destroyed when OK is clicked.
       The message will be wrapped at newline characters.
    """

    def __init__(self, message, style, button_style = clickndrag.gui.lmr.WHITE_STYLE):
        """Initialise.

           style is an instance of TMBStyle.
        """

        # Base class __init__()
        # We need a unique random name an just use this instance's id.
        # TODO: prefix with some letters to make it usable via attribute calls
        #
        TMBContainer.__init__(self, str(id(self)), style, padding = 5)

        # Adapted from clickndrag.gui.OkBox
        #
        linecount = 0

        for line in message.split("\n"):

            self.sub(clickndrag.gui.Label("message-line_{0}".format(linecount),
                                          line,
                                          pygame.Rect((0, 0),
                                                      (len(line) * clickndrag.gui.PIX_PER_CHAR, 30)),
                                          background_color = (128, 128, 128, 0)))

            linecount = linecount + 1

        self.sub(clickndrag.gui.lmr.LMRButton("OK", 50, self.ok, button_style))

        return
