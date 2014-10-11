#!/usr/bin/python3

"""planes GUI Widgets Demo

   Copyright (c) 2014 Florian Berger <mail@florian-berger.de>
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

# work started on 11. October 2014

import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import planes.gui
import planes.gui.lmr
import planes.gui.tmb
import traceback

def add_Label(parent_plane, x, y):
    """Add a Label.
    """

    parent_plane.sub(planes.gui.Label(parent_plane.random_name(), "Label", pygame.Rect((x, y), (100, 50))))

    return

def add_OutlinedText(parent_plane, x, y):
    """Add an OutlinedText.
    """

    outlined_text = planes.gui.OutlinedText(parent_plane.random_name(), "OutlinedText")

    outlined_text.rect.left = x
    outlined_text.rect.top = y

    parent_plane.sub(outlined_text)

    return

def add_Button(parent_plane, x, y):
    """Add a Button.
    """

    parent_plane.sub(planes.gui.Button("Button", pygame.Rect((x, y), (100, 50)), None))

    return

def add_TextBox(parent_plane, x, y):
    """Add a TextBox.
    """

    textbox = planes.gui.TextBox(parent_plane.random_name(), pygame.Rect((x, y), (100, 50)))

    textbox.text = "TextBox"

    def get_focus(plane):

        # NOTE: Assuming parent_plane is the display
        #
        parent_plane.key_sensitive(textbox)

        return

    textbox.left_click_callback = get_focus

    parent_plane.sub(textbox)

    return

# TODO:
#def add_Container(parent_plane, x, y):
#    """Add a Container.
#    """
#
#    return

# TODO:
#def add_GetStringDialog(parent_plane, x, y):
#    """Add a GetStringDialog.
#    """
#
#    return

# TODO:
#def add_FadingContainer(parent_plane, x, y):
#    """Add a FadingContainer.
#    """
#
#    return

def add_OptionList(parent_plane, x, y):
    """Add an OptionList.
    """

    option_list = planes.gui.OptionList(parent_plane.random_name(), ["First option", "Second option", "Third option"])

    option_list.rect.left = x
    option_list.rect.top = y

    parent_plane.sub(option_list)

    return

# TODO:
#def add_OptionSelector(parent_plane, x, y):
#    """Add an OptionSelector.
#    """
#
#    return

# TODO:
#def add_OkBox(parent_plane, x, y):
#    """Add an OkBox.
#    """
#
#    return

# TODO:
#def add_ScrollingPlane(parent_plane, x, y):
#    """Add a ScrollingPlane.
#    """
#
#    return

def add_PlusMinusBox(parent_plane, x, y):
    """Add a PlusMinusBox.
    """

    plus_minus_box = planes.gui.PlusMinusBox(parent_plane.random_name(), 3)

    plus_minus_box.rect.left = x
    plus_minus_box.rect.top = y

    def get_focus(plane):

        # NOTE: Assuming parent_plane is the display
        #
        parent_plane.key_sensitive(plus_minus_box.textbox)

        return

    plus_minus_box.textbox.left_click_callback = get_focus

    parent_plane.sub(plus_minus_box)

    return

def add_ProgressBar(parent_plane, x, y):
    """Add a ProgressBar.
    """

    parent_plane.sub(planes.gui.ProgressBar(parent_plane.random_name(), pygame.Rect((x, y), (100, 50)), 42, text = "ProgressBar"))

    return

# TODO:
#def add_TMBContainer(parent_plane, x, y):
#    """ Add a TMBContainer.
#    """
#
#    return

# TODO:
#def add_TMBOkBox(parent_plane, x, y):
#    """ Add a TMBOkBox.
#    """
#
#    return

# TODO:
#def add_TMBOptionSelector(parent_plane, x, y):
#    """ Add a TMBOptionSelector.
#    """
#
#    return

# TODO:
#def add_TMBGetStringDialog(parent_plane, x, y):
#    """ Add a TMBGetStringDialog.
#    """
#
#    return

# TODO:
#def add_TMBFadingContainer(parent_plane, x, y):
#    """ Add a TMBFadingContainer.
#    """
#
#    return

def add_LMRButton(parent_plane, x, y):
    """ Add an LMRButton.
    """

    lmr_button = planes.gui.lmr.LMRButton("LMRButton", 100, None)

    lmr_button.rect.left = x
    lmr_button.rect.top = y
    
    parent_plane.sub(lmr_button)

    return

def add_LMROptionList(parent_plane, x, y):
    """ Add an LMROptionList.
    """

    lmr_option_list = planes.gui.lmr.LMROptionList(parent_plane.random_name(), ["First option", "Second Option", "Third Option"], 200)

    lmr_option_list.rect.left = x
    lmr_option_list.rect.top = y

    parent_plane.sub(lmr_option_list)

    return

def add_LMRPlusMinusBox(parent_plane, x, y):
    """ Add a LMRPlusMinusBox.
    """

    lmr_plus_minus_box = planes.gui.lmr.LMRPlusMinusBox(parent_plane.random_name(), 3)

    lmr_plus_minus_box.rect.left = x
    lmr_plus_minus_box.rect.top = y

    def get_focus(plane):

        # NOTE: Assuming parent_plane is the display
        #
        parent_plane.key_sensitive(lmr_plus_minus_box.textbox)

        return

    lmr_plus_minus_box.textbox.left_click_callback = get_focus

    parent_plane.sub(lmr_plus_minus_box)

    return

def mainloop(display, framerate):
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

        display.process(events)
        display.update()
        display.render()

        pygame.display.flip()

        # Slow down to framerate given
        #
        clock.tick(framerate)

    return

def main():
    """Main method.
    """

    window = planes.Display((800, 600))

    window.image.fill((127, 127, 127))

    pygame.display.set_caption("planes Widgets Demo")

    widget_creators = [add_Label,
                       add_OutlinedText,
                       add_Button,
                       add_TextBox,
                       add_OptionList,
                       add_PlusMinusBox,
                       add_ProgressBar,
                       add_LMRButton,
                       add_LMROptionList,
                       add_LMRPlusMinusBox]

    x = 10
    y = 10

    for creator_function in widget_creators:

        creator_function(window, x, y)

        x += 220

        if x > 700:

            x = 10

            y += 150

    print("starting main loop in main thread")

    try:
        mainloop(window, 60)

    except:
        print("Exception in mainloop():")
        print(traceback.format_exc())
        pygame.quit()
        raise SystemExit

    return

if __name__ == "__main__":

    main()
