"""Click'n'Drag Gprahical User Interface Module

   (c) Florian Berger <fberger@florian-berger.de
"""

# work started on 28. Oct 2010

import clickndrag
import pygame

class Label(clickndrag.Plane):
    """A clickndrag.Plane which displays a text.

       Additional attributes:

       Label.text
           The text to be written on the Label

       Label.cached_text
           Cache to catch changes

       Label.font
           Pygame Font instance

       Label.color
           The current background color for this Label

       Label.cached_color
           A cache for color changes

       Label.original_color
           The original color
    """

    def __init__(self, name, text, rect):
        """Initialise the Label.
           text is the text to be written on the Label.
        """

        # Call base class init
        #
        clickndrag.Plane.__init__(self, name, rect, drag = False, grab = False)

        self.color = self.cached_color = self.original_color = (127, 127, 127)

        self.text = text
        self.cached_text = None

        self.font = pygame.font.Font(None, int(self.rect.height * 2 / 3))

        self.redraw()

    def update(self):
        """Renew the text on the label, then call the base class method.
        """

        self.redraw()

        clickndrag.Plane.update(self)

    def redraw(self):
        """Redraw the Label if necessary.
        """

        if (self.text != self.cached_text
            or self.color != self.cached_color):

            self.image.fill(self.color)

            # Give background for speedup
            #
            fontsurf = self.font.render(self.text, True, (0, 0, 0), self.color)
            self.image.blit(fontsurf, (int(self.rect.width / 2 - fontsurf.get_width() / 2),
                                       int(self.rect.height / 2 - fontsurf.get_height() / 2)))

            self.cached_text = self.text
            self.cached_color = self.color

class Button(Label):
    """A clickndrag plane which displays a text and reacts on mouse clicks.

       Additional attributes:

       Button.callback
           The callback function to be called upon clicking.

       Button.argument
           The argument to call the function with.

       Button.clicked_counter
           Counted down when the button is clicked and displays a different color
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
        Label.__init__(self, name, label, rect)

        self.callback = callback
        self.argument = argument

        self.clicked_counter = 0

        self.redraw()

    def redraw(self):
        """Redraw the Button.
        """

        # First redraw base Label
        #
        Label.redraw(self)

        # Embossed button with a 1px border.
        # TODO: this is always redrawn. Replace with a condition.

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

    def update(self):
        """Change color if clicked, then call the base class method.
        """

        if self.clicked_counter:

            self.clicked_counter = self.clicked_counter - 1

            if not self.clicked_counter:

                # Just turned zero, restore original background
                #
                self.color = self.original_color

        Label.update(self)

    def clicked(self):
        """Called when there is a MOUSEDOWN event on this plane.
           Calls Button.callback(Button.argument).
        """

        self.clicked_counter = 4
        self.color = (63, 63, 63)

        self.redraw()

        if self.argument is None:
            self.callback()
        else:
            self.callback(self.argument)
