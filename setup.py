"""planes Setup Script

   Copyright 2010-2012 Florian Berger <fberger@florian-berger.de>
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

# work started on 10. December 2010

import distutils.core
import glob
import os.path
import planes

# TODO: add resources directory

LONG_DESCRIPTION = '''About
-----

planes is a hierarchical surface framework for PyGame.

The planes module introduces the "Plane" class which extends PyGame's
"Surface" functionality, offering a hierarchy of mouse-sensitive,
draggable Surfaces that can be used as sprites, windows, icons or other
interactive elements.

In addition, the planes.gui module uses planes to provide basic GUI
elements like container, label, text box, option list and button.

Prerequisites
-------------

Python >= 2.6 http://www.python.org

PyGame >= 1.9.1 http://pygame.org/

Installation
------------

Unzip the file, then at the command line run

::

    python setup.py install

Examples
--------

A showcase python script will be installed along with planes. Run

::

    planes_interactive.py

Documentation
-------------

API documentation is included and will be installed during install.

Links
-----

planes on Launchpad: https://launchpad.net/planes

planes on Freecode: http://freecode.com/projects/planes

planes on ohloh: https://www.ohloh.net/p/planes

planes on the Python Package Index: http://pypi.python.org/pypi/planes

planes on pygame.org: http://pygame.org/project-planes-2392-4051.html

Author
------

Florian Berger'''

distutils.core.setup(name = "planes",
                     version = planes.VERSION,
                     author = "Florian Berger",
                     author_email = "fberger@florian-berger.de",
                     url = "http://florian-berger.de/en/software/planes/",
                     description = "planes - A Hierarchical Surface Framework for Pygame",
                     long_description = LONG_DESCRIPTION,
                     license = "GPL",
                     packages = ["planes",
                                 "planes.gui"],
                     requires = ["pygame (>=1.9.1)"],
                     provides = ["planes",
                                 "planes.gui"],
                     scripts = ["examples/planes_interactive.py"],
                     package_data = {"planes" : ["Vera.ttf", "VeraBd.ttf"]},
                     data_files = [("share/doc/planes-{0}".format(planes.VERSION),
                                    glob.glob(os.path.join("doc", "*.*")) + ["NEWS"])])
