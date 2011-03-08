"""Click'n'Drag Gprahical User Interface Module

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Global variables:

   BACKGROUND_COLOR
       Defaults to (150, 150, 150).

   HIGHLIGHT_COLOR
       Defaults to (191, 95, 0).

   BIG_FONT
       A pygame.font.Font instance, large pointsize.

   SMALL_FONT
       A pygame.font.Font instance, small pointsize.
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

# work started on 28. Oct 2010

import clickndrag
import pygame
import os.path

BACKGROUND_COLOR = (150, 150, 150)
HIGHLIGHT_COLOR = (191, 95, 0)

# Initialise the font module. This can safely be called more than once.
#
pygame.font.init()

# Initialise font instances.
# Taken from fabula.PygameUserInterface.
#
try:
    BIG_FONT = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Vera.ttf"), 30)
    SMALL_FONT = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Vera.ttf"), 12)

except:
    # TODO: log used font: pygame.font.get_default_font()
    #print("Could not load {}".format(os.path.join(os.path.dirname(__file__), "Vera.ttf")))
    BIG_FONT = pygame.font.Font(None, 40)
    SMALL_FONT = pygame.font.Font(None, 20)

def draw_border(plane, color):
    """Draw a border around plane.
    """
    pygame.draw.lines(plane.image,
                      color,
                      True,
                      ((0, 0),
                       (plane.rect.width - 1, 0),
                       (plane.rect.width - 1, plane.rect.height - 1),
                       (0, plane.rect.height - 1)))

    return

class Label(clickndrag.Plane):
    """A clickndrag.Plane which displays a text.

       Additional attributes:

       Label.text
           The text to be written on the Label

       Label.cached_text
           Cache to catch changes

       Label.color
           The original background color for this Label

       Label.current_color
           The current background color

       Label.cached_color
           A cache for color changes
    """

    def __init__(self, name, text, rect, color = BACKGROUND_COLOR):
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
            fontsurf = SMALL_FONT.render(self.text, True, (0, 0, 0), self.current_color)

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

    def __init__(self, label, rect, callback, color = BACKGROUND_COLOR):
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

    def __init__(self, name, padding = 0, color = BACKGROUND_COLOR):
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

        draw_border(self, (0, 0, 0))

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

        self.current_color = HIGHLIGHT_COLOR

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

    def __init__(self, name, option_list, callback, width = 200, lineheight = 30):
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

            option = Option("option" + str(option_list.index(text)),
                           text,
                           pygame.Rect((0, 0), (width, lineheight)))

            self.sub(option)

        button = Button("OK",
                        pygame.Rect((0, 0), (width, lineheight)),
                        self.selection_made)

        self.sub(button)

        self.option0.current_color = HIGHLIGHT_COLOR
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
       To actually receive key events, the TextBox must be registered with the
       Display using Display.key_sensitive(TextBox).
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
            fontsurf = SMALL_FONT.render(self.text, True, (0, 0, 0), self.current_color)

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

class GetStringDialog(Container):
    """A combination of Container, Label, TextBox and Button that asks the user for a string.

       Additional attributes:

       GetStringDialog.callback
           The callback to be called callback(string) when the input is confirmed.
    """

    # TODO: this could be merged with OkBox into a class "ConfirmBox"

    def __init__(self, prompt, callback, display):
        """Open the GetStringDialog as a subplane of display.
        """

        # Initialise container
        #
        Container.__init__(self, "get_string_dialog", padding = 5)

        self.callback = callback

        self.sub(Label("prompt", prompt, pygame.Rect((0, 0), (200, 30))))

        textbox = TextBox("textbox", pygame.Rect((0, 0), (200, 30)))

        self.sub(textbox)

        display.key_sensitive(textbox)

        self.sub(Button("OK",
                        pygame.Rect((0, 0), (90, 30)),
                        self.ok))

        return

    def ok(self, plane):
        """Button callback to destroy the GetStringDialog and call GetStringDialog.callback(string).
           The callback should call render() and flip the display to remove the GetStringDialog from the screen.
        """

        callback = self.callback
        string = self.textbox.text

        self.destroy()

        callback(string)

        return

class ScrollingPlane(clickndrag.Plane):
    """This class implements a fixed-dimension plane with a scroll bar to scroll its content plane.
       Subplane structure:

       ScrollingPlane
       |
       +---content
       |   |
       |   +---content_plane from __init__()
       |
       +---scrollbar_container
           |
           +---scrollbar
    """

    def __init__(self, name, rect, content_plane, draggable = False, grab = False, clicked_callback = None, dropped_upon_callback = None):
        """Initalise.
           rect states the dimensions without the scroll bar.
        """

        rect.width = rect.width + 12

        # Call base class
        #
        clickndrag.Plane.__init__(self, name, rect, draggable, grab, clicked_callback, dropped_upon_callback)

        self.image.fill(BACKGROUND_COLOR)

        self.sub(clickndrag.Plane("content", pygame.Rect((0, 0),
                                                         (self.rect.width - 12, self.rect.height))))

        content_plane.rect.topleft = (0, 0)
        self.content.sub(content_plane)

        scrollbar_container = clickndrag.Plane("scrollbar_container",
                                               pygame.Rect((self.rect.width - 12, 0),
                                                           (12, self.rect.height)))

        scrollbar_container.image.fill(BACKGROUND_COLOR)
        draw_border(scrollbar_container, (0, 0, 0))

        def scrollbar_container_clicked(plane):
            """Clicked callback which repositions the content Plane and scrollbar according to the y-position of the mouse.
            """
            x, y = pygame.mouse.get_pos()

            new_y = y - self.rect.top

            # Align scrollbar at bottom
            #
            if new_y > self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2:
                new_y = self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2

            self.scrollbar_container.scrollbar.rect.top = new_y

            content_plane = self.content.subplanes[self.content.subplanes_list[0]]
            content_plane.rect.top = int(0 - new_y / self.rect.height * content_plane.rect.height)

            return

        scrollbar_container.clicked_callback = scrollbar_container_clicked

        self.sub(scrollbar_container)

        # Scrollbar height reflects the proportions
        #
        self.scrollbar_container.sub(clickndrag.Plane("scrollbar", pygame.Rect((2, 2),
                                                                          (8, int(self.rect.height / content_plane.rect.height * self.rect.height)))))

        # Half-bright color taken from Button.clicked()
        #
        self.scrollbar_container.scrollbar.image.fill(list(map(lambda i : int(i * 0.5), BACKGROUND_COLOR)))

        return
