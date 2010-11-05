"""Run an interactive Click'n'Drag-Session.

   Start this script with 'python -i' or import it as a module
   
   (c) Florian Berger <fberger@florian-berger.de>
"""

# work started on 04. November 2010

import sys

# Add current and parent directory. One of them is supposed to contain the
# clickndrag package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import clickndrag
import clickndrag.gui
import threading

print("creating window")

window = clickndrag.Display((400, 300))
pygame.display.set_caption("Click'n'Drag Interactive Live Test")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)

def mainloop(fps):
    """Runs a pygame / clickndrag main loop.
       fps is the framerate.
    """

    clock = pygame.time.Clock()

    print("about to start main loop")

    while True:
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                print("got pygame.QUIT, terminating in mainloop()")
                pygame.quit()
                raise SystemExit

        window.process(events)
        window.update()
        window.render()

        pygame.display.flip()

        # Slow down to fps given
        #
        clock.tick(fps)

mainloop_thread = threading.Thread(target = mainloop,
                                   name = "mainloop",
                                   args = (25,))
print("starting mainloop thread")

mainloop_thread.start()

help = """If you have started this script with 'python -i' or imported it as a
module, you can now interact with clickndrag. Use the 'window' object.

Plane(name, rect, drag=False, grab=False)

Plane.image               - The pygame.Surface for a Plane
Plane.rect                - The render position on the parent plane
Plane.subplanes           - Dict of subplanes
Plane.draggable           - Flags for Plane configuration
Plane.grab_dropped_planes - Flags for Plane configuration

Plane.sub(Plane)          - Add plane as a subplane of this Plane.

red, green, blue, yellow, white - Color tuples for your convenience
print(help)               - Print this help text
"""

print(help)
