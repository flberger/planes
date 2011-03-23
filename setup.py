"""Click'n'Drag Setup Script

   Copyright 2010 Florian Berger <fberger@florian-berger.de>
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

# work started on 10. December 2010

# clickndrag will not work with Python versions prior to 3.x.
#
import sys

if sys.version_info[0] != 3:
    raise Exception("clickndrag needs Python 3 to work. Your Python version is: " + sys.version)

import distutils.core
import glob
import os.path

VERSION = "0.3.0"

distutils.core.setup(name = "clickndrag",
                     version = VERSION,
                     author = "Florian Berger",
                     author_email = "fberger@florian-berger.de",
                     url = "http://florian-berger.de/software/clickndrag/",
                     description = "Click'n'Drag - A Hierarchical Surface Framework for Pygame",
                     license = "GPL",
                     packages = ["clickndrag"],
                     requires = ["pygame (>=1.9.1)"],
                     provides = ["clickndrag"],
                     scripts = ["examples/clickndrag-interactive.py"],
                     package_data = {"clickndrag" : ["Vera.ttf", "VeraBd.ttf"]},
                     data_files = [("share/doc/clickndrag-{}".format(VERSION),
                                    glob.glob(os.path.join("doc", "*.*")) + ["NEWS"])])
