"""Click'n'Drag Setup Script

   (c) Florian Berger <fberger@florian-berger.de>
"""

# work started on 10. December 2010

import distutils.core

distutils.core.setup(name = "clickndrag",
                     version = "0.1.0a1",
                     author = "Florian Berger",
                     author_email = "fberger@florian-berger.de",
                     url = "http://florian-berger.de/software/clickndrag/",
                     description = "Click'n'Drag - A Hierarchical Surface Framework for Pygame",
                     license = "GPL",
                     packages = ["clickndrag"],
                     requires = ["pygame (>=1.9.1)"],
                     provides = ["clickndrag"],
                     scripts = ["examples/clickndrag-interactive.py"],
                     package_data = {"clickndrag" : ["doc/*"]})
