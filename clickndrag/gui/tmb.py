"""tmb - Top-Mid-Bottom Background Styles for clickndrag.gui widgets.

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

# TODO: Container
# TODO: GetStringDialog
# TODO: OkBox
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

        self.top_img = pygame.image.load(top_img).convert_alpha()

        self.mid_img = pygame.image.load(mid_img).convert_alpha()

        self.bottom_img = pygame.image.load(bottom_img).convert_alpha()

        return
