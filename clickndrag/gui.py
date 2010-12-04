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
           The original background color for this Label

       Label.current_color
           The current background color

       Label.cached_color
           A cache for color changes
    """

    def __init__(self, name, text, rect, color = (150, 150, 150)):
        """Initialise the Label.
           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.
        """

        # Call base class init
        #
        clickndrag.Plane.__init__(self, name, rect, draggable = False, grab = False)

        self.color = self.cached_color = self.current_color = color

        if text is not None:
            self.text = text
        else:
            self.text = ""

        self.cached_text = None

        try:
            self.font = pygame.font.Font("Vera.ttf", int(self.rect.height * 0.45))

        except:

            # Use default font
            #
            self.font = pygame.font.Font(None, int(self.rect.height * 2 / 3))

        self.redraw()

        return

    def update(self):
        """Renew the text on the label, then call the base class method.
        """

        self.redraw()

        clickndrag.Plane.update(self)

        return

    def redraw(self):
        """Redraw the Label if necessary.
        """

        if (self.text != self.cached_text
            or self.current_color != self.cached_color):

            self.image.fill(self.current_color)

            # Text is centered on rect.
            # Give background for speedup.
            #
            fontsurf = self.font.render(self.text, True, (0, 0, 0), self.current_color)

            centered_rect = fontsurf.get_rect()

            # Get a neutral center of self.rect
            #
            centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

            self.image.blit(fontsurf, centered_rect)

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text
            self.cached_color = self.current_color

        return

class Button(Label):
    """A clickndrag plane which displays a text and reacts on mouse clicks.

       Additional attributes:

       Button.callback
           The callback function to be called upon clicking.

       Button.clicked_counter
           Counted down when the button is clicked and displays a different color
    """

    def __init__(self, label, rect, callback, color = (150, 150, 150)):
        """Initialise the Button.
           label is the Text to be written on the button.
           rect is an instance of pygame.Rect giving the dimensions.
           callback is the function to be called when the Button is clicked.
        """

        # name is the alphanumeric-only-lower case-version of label
        #
        name = ''.join(filter(str.isalnum, label)).lower()

        # Call base class init
        #
        Label.__init__(self, name, label, rect, color)

        # Overwrite Plane base class attribute
        #
        self.clicked_callback = callback

        self.clicked_counter = 0

        self.redraw()

        return

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

        return

    def update(self):
        """Change color if clicked, then call the base class method.
        """

        if self.clicked_counter:

            self.clicked_counter = self.clicked_counter - 1

            if not self.clicked_counter:

                # Just turned zero, restore original background
                #
                self.current_color = self.color

        Label.update(self)

        return

    def clicked(self):
        """Called when there is a MOUSEDOWN event on this plane.
           Changes the Button color for some frames and calls the base class implementation.
        """

        self.clicked_counter = 4

        # Half-bright
        #
        self.current_color = list(map(lambda i: int(i * 0.5), self.current_color))

        self.redraw()

        # Call base class implementation which will call the callback
        #
        Label.clicked(self)

        return

class Container(clickndrag.Plane):
    """A Container for Planes.
       If a subplane is added via sub(), the container places it below any existing
       subplanes and resizes itself to fit the width and height of the subplanes.

       Additional attributes:

       Container.padding
           Space between subplanes and border, in pixels

       Container.color
           The original background color for this Container
    """

    def __init__(self, name, padding = 0, color = (150, 150, 150)):
        """Initialise.
           Container.image is initialised to a 0x0 px Surface.
        """

        # Call base class
        #
        clickndrag.Plane.__init__(self, name, pygame.Rect((0, 0), (0, 0)))

        self.padding = padding
        self.color = color

        return

    def redraw(self):
        """Redraw Container.image from the dimensions in Containter.rect.
           This also creates a new Container.rendersurface.
        """
        # Create Surface with background color and black border
        #
        self.image = pygame.Surface(self.rect.size)

        self.image.fill(self.color)

        pygame.draw.lines(self.image,
                          (0, 0, 0),
                          True,
                          ((0, 0),
                           (self.rect.width - 1, 0),
                           (self.rect.width - 1, self.rect.height - 1),
                           (0, self.rect.height - 1)))

        # Create a new rendersurface
        #
        self.rendersurface = pygame.Surface(self.rect.size)

        return

    def sub(self, plane):
        """Resize the container, update the position of plane and add it as a subplane.
        """

        # First add the subplane by calling the base class method.
        # This also cares for re-adding an already existing subplane.
        #
        clickndrag.Plane.sub(self, plane)

        # Containers have a 1px black border. Observe this when calculating width
        # and height.
        # Existing subplanes are already incorporated in self.rect.

        # Conditionally fit new width
        #
        if plane.rect.width > self.rect.width - 2 * self.padding - 2:

            self.rect.width = plane.rect.width + 2 * self.padding + 2

        # Mandatory fit new height, observe padding
        #
        if not self.rect.height:

            # No subplanes yet

            plane.rect.topleft = (0, 1 + self.padding)

            self.rect.height = plane.rect.height + 2 * self.padding + 2

        else:
            plane.rect.topleft = (0, self.rect.height - 1)

            self.rect.height = self.rect.height + plane.rect.height + self.padding

        # Re-center all subplanes.
        #
        for name in self.subplanes_list:
            rect = self.subplanes[name].rect
            rect.left = int((self.rect.width - rect.width) / 2)

        self.redraw()

        return

    def remove(self, plane_identifier):
        """Remove the subplane, then reposition remaining subplanes and resize the container.
        """

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
        top = 1 + self.padding

        for name in self.subplanes_list:
            rect = self.subplanes[name].rect
            rect.top = top
            top = top + rect.height + self.padding

        # Now shrink and redraw.
        #
        self.rect.height = self.rect.height - height_removed

        self.redraw()

        return

    def remove_all(self):
        """Remove all subplanes and shrink accordingly.
        """

        # Cave: loop while modifying loop item source. Create a new list.
        #
        for name in list(self.subplanes_list):

            self.remove(name)

        return

class Option(Label):
    """A subclass of Label which handles mouseclicks, to be used in an OptionList.
    """

    def clicked(self):
        """Highlight this option and register as parent.selected.
        """

        for name in self.parent.subplanes_list:

            plane = self.parent.subplanes[name]
            plane.current_color = plane.color

            # Force redraw in render()
            #
            plane.last_rect = None

        self.current_color = (191, 95, 0)

        # Force redraw in render()
        #
        self.last_rect = None

        self.parent.selected = self

        return

class OptionList(Container):
    """A list of options to select from.

       Options are subplanes of OptionList, named option0, option1, ..., optionN

       Additional attributes:

       OptionList.selected
           The selected Option
    """

    def __init__(self, name, option_list, callback):
        """Initialise the OptionList.
           option_list is a list of strings to be displayed as options.
           callback is a function to be called with the selected Option instance
           as argument once the selection is made.
        """

        # Call base class init
        #
        Container.__init__(self, name)

        # TODO: copied from Button.__init__. Maybe inherit from a third class 'Callback'?
        #
        self.callback = callback

        # Add options and OK button
        #
        for text in option_list:

            # TODO: hardcoded option width and height - replace with argument
            #
            option = Option("option" + str(option_list.index(text)),
                           text,
                           pygame.Rect((0, 0), (200, 30)))

            self.sub(option)

        button = Button("OK",
                        pygame.Rect((0, 0), (200, 30)),
                        self.selection_made)

        self.sub(button)

        self.option0.current_color = (191, 95, 0)
        self.selected = self.option0

        return

    def selection_made(self, plane):
        """Button callback called when the user confirmed an option from the OptionList.
           Calls OptionList.callback(self.selected) and destroys the OptionList.
        """

        self.callback(self.selected)

        self.destroy()

        return

class OkBox(Container):
    """A box which displays a message and an OK button.
       It is destroyed when OK is clicked.
    """

    def __init__(self, message):
        """Initialise.
        """

        # Base class __init__()
        # We need a unique random name an just use this instance's id.
        # TODO: prefix with some letters to make it usable via attribute calls
        #
        Container.__init__(self, str(id(self)), padding = 5)

        self.sub(Label("message",
                       message,
                       pygame.Rect((0, 0), (len(message) * 7, 30))))

        self.sub(Button("OK", pygame.Rect((0, 0), (50, 30)), self.ok))

        return

    def ok(self, plane):
        """Button clicked callback which destroys the OkBox.
        """

        self.destroy()

        return

class TextBox(Label):
    """A box where the user can type text.
    """

    def __init__(self, name, rect, color = (250, 250, 250)):
        """Initialise the TextBox.
        """

        # Call base class
        #
        Label.__init__(self, name, None, rect, color)

        return

    def keydown(self, keydown_event):
        """If prinable, add keydown_event.unicode to self.text.
        """

        if keydown_event.unicode.isprintable():

            self.text = self.text + keydown_event.unicode

        elif keydown_event.key == pygame.K_BACKSPACE:

            self.text = self.text[:-1]

        return

    def redraw(self):
        """Redraw the TextBox if necessary.
        """

        if (self.text != self.cached_text
            or self.current_color != self.cached_color):

            self.image.fill(self.current_color)

            # Give background for speedup.
            #
            fontsurf = self.font.render(self.text, True, (0, 0, 0), self.current_color)

            # Text is left-aligned on rect, except when it is larger than the
            # Label, in which case it is right-aligned.
            #
            if fontsurf.get_rect().width > self.rect.width:

                self.image.blit(fontsurf, (self.rect.width - fontsurf.get_rect().width, 0))

            else:
                self.image.blit(fontsurf, (0, 0))

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text
            self.cached_color = self.current_color

        return
