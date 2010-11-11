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

       Attributes:
       
       Plane.name
           Name of the plane

       Plane.image
           The pygame.Surface for this Plane

       Plane.rendersurface
           A pygame.Surface displaying the composite of this plane and all
           subplanes.

       Plane.rect
           The render position on the parent plane

       Plane.parent
           Pointer to the parent plane.

       Plane.subplanes
           Dict of subplanes

       Plane.subplanes_list
           A list of subplane names, in order of their addition

       Plane.draggable
           If True, this Plane can be dragged and dropped.

       Plane.grab_dropped_planes
          If True, this Plane will remove dropped Planes from
          their parent Plane and make it a subplane of this one.
          Handled in Plane.dropped_upon()
    """

    def __init__(self, name, rect, drag = False, grab = False):
        """Initialize the Plane.
           name is the name of the plane which can also be used
           as an attribute.
           rect is an instance of pygame.Rect giving width, height
           and render position.
           drag is a flag indicating whether this plane can be dragged.
           grab is a flag indicating whether other planes can be dropped
           on this one.
           Planes are filled with solid black color by default.
        """

        self.name = name

        # We need to initialise with the slow SRCALPHA, but otherwise we would
        # not be able to blit images with per-pixel alpha
        #
        self.image = pygame.Surface(rect.size, flags = pygame.SRCALPHA)

        # Transparent by default, so let's paint it black
        #
        self.image.fill((0, 0, 0, 255))

        # Plane.image is the image of this very plane.
        # Plane.rendersurface is the composite of this
        # plane and all subplanes.
        # To save space, it is initalized to Plane.image.
        # A surface is only created when there are subsurfaces.
        #
        self.rendersurface = self.image

        # Rect is relative to the parent plane, not to the display!
        #
        self.rect = rect

        self.draggable = drag
        self.grab_dropped_planes = grab

        # Parent stores the parent plane.
        # Upon creation, there is none.
        #
        self.parent = None

        self.subplanes = {}
        self.subplanes_list = []

    def sub(self, plane):
        """Add plane as a subplane of this Plane.
        """

        self.subplanes_list.append(plane.name)
        self.subplanes[plane.name] = plane
        plane.parent = self

        # Now that there is a subplane, if not already done so,
        # create an actual rendersurface for this plane.
        #
        if self.rendersurface == self.image:
            self.rendersurface = pygame.Surface(self.rect.size)

    def remove(self, *names):
        """Without arguments, remove all subplanes. With strings as arguments, remove them by name.
        """

        if not names:

            for name in self.subplanes_list:
                self.subplanes[name].parent = None

            self.subplanes = {}
            self.subplanes_list = []

        else:
            for name in names:
                if name in self.subplanes_list:
                    self.subplanes[name].parent = None
                    del self.subplanes[name]
                    del self.subplanes_list[self.subplanes_list.index(name)]

    def __getattr__(self, name):
        """Access subplanes as attributes.
        """

        return(self.subplanes[name])

    def render(self):
        """Draw a composite surface of this plane and all subplanes, in order of their addition.
        """

        # We only need to render if self.rendersurface does not point
        # to self.image.
        #
        if self.rendersurface != self.image:

            # Is this correct? Maybe the user has updated the image, but
            # when there are no subplanes, there is no need to render.
            # Except for the 'display' root Plane, of course: overwriting
            # the rendersurface would make it invisible and inaccessible.
            #
            if not self.subplanes and self.name != 'display':

                # Fix the pointer
                #
                self.rendersurface = self.image

            else:

                # Observe alpha! First clear the rendersurface.
                #
                self.rendersurface.fill((0, 0, 0, 0))
                
                # Then blit this plane's image
                #
                self.rendersurface.blit(self.image, (0, 0))

                if self.subplanes_list:

                    # Then render and blit all subplanes
                    #
                    for name in self.subplanes_list:
                        plane = self.subplanes[name]
                        plane.render()
                        self.rendersurface.blit(plane.rendersurface, plane.rect)

    def get_plane_at(self, coordinates):
        """Return the (sub)plane and the succeeding parent coordinates at the given coordinates.
           Subplanes are tested in reverse order of their addition (i.e. latest first).
        """

        # It's probaly me.
        #
        return_plane = self
        return_coordinates = coordinates

        for name in self.subplanes_list:

            plane = self.subplanes[name]

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
           If Plane.grab_dropped_planes is True, the default implementation
           will remove the dropped Plane from its parent and make it a
           subplane of this one.
        """

        if self.grab_dropped_planes:

            plane.parent.remove(plane.name)

            plane.rect.center = coordinates

            self.sub(plane)

    def destroy(self):
        """Remove this Plane from the parent plane and delete all pygame Surfaces.
        """

        if self.parent is not None:
            self.parent.remove(self.name)
            self.parent = None

        self.image = self.rendersurface = None
        self.subplanes = self.subplanes_list = None
        self.rect = self.draggable =  self.grab_dropped_planes = None

    def __repr__(self):
        """Readable string representation.
        """

        parent_name = "None"

        if self.parent is not None:
            parent_name = self.parent.name
            
        return("<clickndrag.Plane name='{}' image={} rendersurface={} rect={} parent='{}' subplanes_list={} draggable={} grab_dropped_planes={}>".format(self.name,
                                                      "{}@{}".format(self.image, id(self.image)),
                                                      "{}@{}".format(self.rendersurface, id(self.rendersurface)),
                                                      self.rect,
                                                      parent_name,
                                                      self.subplanes_list,
                                                      self.draggable,
                                                      self.grab_dropped_planes))

class Display(Plane):
    """Click'n'Drag main screen class.
       A Display instance serves as the root Plane in clickndrag.

       Additional attributes:

       Display.dragged_plane
           The currently dragged plane
    """

    def __init__(self, resolution_tuple):
        """Calling pygame.display.set_mode.
        """

        # Init Pygame, just to be on the safe side.
        # pygame.init() can safely be called more than once.
        #
        pygame.init()

        try:
            display = pygame.display.set_mode(resolution_tuple)

        except pygame.error:

            # Microsoft Windows SDL error: "No available video device"
            # For a list see
            # http://www.libsdl.org/cgi/docwiki.cgi/SDL_envvars
            #
            import os

            os.environ['SDL_VIDEODRIVER']='windib'

            display = pygame.display.set_mode(resolution_tuple)

        Plane.__init__(self, "display", pygame.Rect((0, 0), resolution_tuple))

        # In this case the rendersurface is the pygame display
        #
        self.rendersurface = display

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

            return

    def render(self):
        """Plane.render plus drawing of the dragged plane.
        """

        Plane.render(self)

        # Dragged plane on top
        #
        if self.dragged_plane != None:

            self.dragged_plane.rect.center = pygame.mouse.get_pos()

            self.rendersurface.blit(self.dragged_plane.rendersurface, self.dragged_plane.rect)
