"""Click'n'Drag
   A Hierarchical Surface Framework for PyGame
   (c) Florian Berger <fberger@florian-berger.de>
"""

# Planned in mind at the Mosel valley in late July 2010
# Actual work started on 01. Oct 2010

import pygame

class Plane:
    """A Plane is a surface in a hierarchy of surfaces.
       It shares some properties with pygame.sprite.Sprite.
    """

    def __init__(self, name, rect):
        """Initialize the Plane.
        """

        self.name = name

        self.image = pygame.Surface(rect.size)

        # Rect is relative to the parent plane, not to the display!
        #
        self.rect = rect

        # Plane.image is the image of this very plane.
        # Plane.rendersurface is the composite of this
        # plane and all subplanes.
        # To save space, it is initalized to Plane.image.
        # A surface is only created when there are subsurfaces.
        #
        self.rendersurface = self.image

        self.subplanes = {}

        # Parent stores the parent plane.
        # Upon creation, there is none.
        #
        self.parent = None

        self.draggable = True
        self.grab_dropped_planes = False

    def sub(self, plane):
        """Add plane as a subplane of this Plane.
        """

        self.subplanes[plane.name] = plane
        plane.parent = self

        # Now that there is a subplane, if not already done so,
        # create an actual rendersurface for this plane.
        #
        if self.rendersurface == self.image:
            self.rendersurface = pygame.Surface(self.rect.size)

    def __getattr__(self, name):
        """Access subplanes as attributes.
        """

        return(self.subplanes[name])

    def render(self):
        """Draw a composite surface of this plane and all subplanes.
        """

        # We only need to render if self.rendersurface does not point
        # to self.image.
        #
        if self.rendersurface != self.image:

            # First blit this plane's image
            #
            self.rendersurface.blit(self.image, (0, 0))

            if len(self.subplanes.keys()):

                # Then render and blit all subplanes
                #
                for plane in self.subplanes.values():
                    plane.render()
                    self.rendersurface.blit(plane.rendersurface, plane.rect)

    def get_plane_at(self, coordinates):
        """Return the (sub)plane and the succeeding parent coordinates at the given coordinates.
        """

        # It's probaly me.
        #
        return_plane = self
        return_coordinates = coordinates

        # TODO: First come, first served. What about multiple planes at one point?
        #
        for plane in self.subplanes.values():

            if plane.rect.collidepoint(coordinates):

                return_coordinates = (coordinates[0] - plane.rect.left, coordinates[1] - plane.rect.top)

                return_plane, return_coordinates = plane.get_plane_at(return_coordinates)

        return((return_plane, return_coordinates))

    def update(self):
        """Update hook.
           The default implementation calls update() on all subplanes.
           See pygame.sprite.Sprite.update.
        """

        for plane in self.subplanes.values():

            plane.update()

    def clicked(self):
        """Called when there is a MOUSEDOWN event on this plane.
           The default implementation does nothing.
        """

        pass

    def dropped_upon(self, plane, coordinates):
        """Called when a plane is dropped on top of this one.
        """

        if self.grab_dropped_planes:

            del plane.parent.subplanes[plane.name]

            self.sub(plane)

            plane.rect.center = coordinates

class Display(Plane):
    """Click'n'Drag main screen class.
       A Display instance serves as the root Plane in clickndrag.
    """

    def __init__(self, resolution_tuple):
        """Calling pygame.display.set_mode.
        """

        Plane.__init__(self, "display", pygame.Rect((0, 0), resolution_tuple))

        # In this case the rendersurface is the pygame display
        #
        self.rendersurface = pygame.display.set_mode(resolution_tuple)

        self.draggable = False

        # Keep track of the dragged plane
        #
        self.dragged_plane = None

    def process(self, event_list):
        """Process a pygame event list.
        """

        for event in event_list:

            if (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1):

                clicked_plane = self.get_plane_at(event.pos)[0]

                if clicked_plane != self:

                    # Notify plane instance
                    #
                    clicked_plane.clicked()

                    if clicked_plane.draggable:

                        # Use a copy for new coordinates etc.
                        #
                        self.dragged_plane = Plane("dragged_plane", clicked_plane.rect.copy())
                        self.dragged_plane.rendersurface = clicked_plane.rendersurface.copy()

                        # Keep original for reference
                        #
                        self.dragged_plane.source = clicked_plane

                        # 2/3 transparency
                        #
                        self.dragged_plane.rendersurface.set_alpha(170, pygame.RLEACCEL)

            elif (event.type == pygame.MOUSEBUTTONUP
            and event.button == 1):

                if self.dragged_plane != None:

                    target_plane, coordinates = self.get_plane_at(event.pos)

                    # Don't drop to self
                    #
                    if target_plane != self.dragged_plane.source:

                        target_plane.dropped_upon(self.dragged_plane.source, coordinates)

                    self.dragged_plane = None

    def render(self):
        """Plane.render plus drawing of the dragged plane.
        """

        Plane.render(self)

        # Dragged plane on top
        #
        if self.dragged_plane != None:

            self.dragged_plane.rect.center = pygame.mouse.get_pos()

            self.rendersurface.blit(self.dragged_plane.rendersurface, self.dragged_plane.rect)
