"""Click'n'Drag Gprahical User Interface Module

   (c) Florian Berger <fberger@florian-berger.de
"""

# work started on 28. Oct 2010

import clickndrag
import pygame

class Button(clickndrag.Plane):
    """A clickndrag plane which displays a text and reacts on mouse clicks.

       Additional attributes:

       Button.callback
           The callback function to be called upon clicking.

       Button.argument
           The argument to call the function with.
    """

    def __init__(self, label, rect, callback, argument = None):
        """Initialise the Button.
           label is the Text to be written on the button.
           rect is an instance of pygame.Rect giving the dimensions.
           callback is the function to be called when the Button is clicked.
           argument is the argument the function will be called with.
        """

        # name is the alphanumeric-only-lower case-version of label
        #
        name = ''.join(filter(str.isalnum, label)).lower()

        # Call base class init
        #
        clickndrag.Plane.__init__(self, name, rect, drag = False, grab = False)

        self.callback = callback
        self.argument = argument

        # Gray embossed button with a 1px border.
        #
        self.image.fill((127, 127, 127))

        self.image.lock()

        # width is 1px by default
        #
        pygame.draw.lines(self.image,
                          (63, 63, 63),
                          False,
                          [(1, self.rect.height - 1),
                           (self.rect.width - 1, self.rect.height - 1),
                           (self.rect.width - 1, 1)])

        pygame.draw.lines(self.image,
                          (190, 190, 190),
                          False,
                          [(0, self.rect.height - 2),
                           (0, 0),
                           (self.rect.width - 2, 0)])

        self.image.unlock()

        # Print label
        #
        font = pygame.font.Font(None, self.rect.height - 4)

        # Give background for speedup
        #
        fontsurf = font.render(label, True, (0, 0, 0), (127, 127, 127))
        self.image.blit(fontsurf, (int(self.rect.width / 2 - fontsurf.get_width() / 2),
                                   int(self.rect.height / 2 - fontsurf.get_height() / 2)))


    def clicked(self):
        """Called when there is a MOUSEDOWN event on this plane.
           Calls Button.callback(Button.argument).
        """

        self.callback(self.argument)
