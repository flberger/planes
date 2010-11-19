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
import code

print("creating window")

window = clickndrag.Display((400, 300))
window.grab_dropped_planes = True
window.image.fill((127, 127, 127))
pygame.display.set_caption("Click'n'Drag Interactive Live Test")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)

def click(*args):
    print("Click! args: {}".format(args))

plane = clickndrag.Plane("plane",
                         pygame.Rect((200, 50), (100, 100)),
                         drag = True)

plane.image.fill(yellow)

button = clickndrag.gui.Button("Button",
                               pygame.Rect((50, 50), (100, 50)),
                               click)

container = clickndrag.gui.Container("container", padding = 10)
container.rect.topleft = (250, 50)

clock = pygame.time.Clock()
fps = clock.get_fps

helptext = """---------------------------------------------------------------------------
You can now interact with clickndrag.

window                          - Root window, instance of clickndrag.Display
plane, button                   - Test instances, try window.sub(plane)
red, green, blue, yellow, white - Color tuples for your convenience
fps()                           - print current framerate
click()                         - A convenience callback function

Plane(name, rect, drag=False, grab=False)

Plane.image               - The pygame.Surface for a Plane
Plane.rect                - The render position on the parent plane
Plane.subplanes           - Dict of subplanes
Plane.draggable           - Flags for Plane configuration
Plane.grab_dropped_planes - Flags for Plane configuration

Plane.sub(Plane)          - Add plane as a subplane of this Plane.

print(helptext)           - Print this help text
---------------------------------------------------------------------------
"""

def mainloop(fps):
    """Runs a pygame / clickndrag main loop.
       fps is the framerate.
       This must be run in the main thread, otherwise pygame.event will not
       receive any events under MS Windows.
    """

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

def run_interactive_console(locals_dict):

    ic = code.InteractiveConsole(locals_dict)

    ic.interact(helptext)

if __name__ == "__main__":

    interactive_console_thread = threading.Thread(target = run_interactive_console,
                                                  name = "interactive_console",
                                                  args = (locals(),))

    print("starting interactive console thread")

    interactive_console_thread.start()

    print("starting main loop in main thread")

    mainloop(60)
