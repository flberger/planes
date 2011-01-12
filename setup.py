"""Click'n'Drag Setup Script

   (c) Florian Berger <fberger@florian-berger.de>
"""

# work started on 10. December 2010

# clickndrag will not work with Python versions prior to 3.x.
#
import sys

if sys.version_info[0] != 3:
    raise Exception("clickndrag needs Python 3 to work. Your Python version is: " + sys.version)

import distutils.core
import glob
import os.path

VERSION = "0.1.0"

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
                     data_files = [("share/doc/clickndrag-{}".format(VERSION),
                                    glob.glob(os.path.join("doc", "*.*")))])
