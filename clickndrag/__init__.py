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

       Planes are not thread safe! Accessing a Plane from several threads may
       produce unexpected results and errors.

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

       Plane.last_image_id
          Caches object id of the image at last rendering for efficiency.

       Plane.last_rect
          Caches rect at last rendering for efficiency.

       Plane.clicked_callback
          Callback function when this plane has been clicked

       Plane.dropped_upon_callback
          Callback function when a plane has been dropped upon this plane
    """

    def __init__(self,
                 name,
                 rect,
                 drag = False,
                 grab = False,
                 clicked_callback = None,
                 dropped_upon_callback = None):
        """Initialize the Plane.
           name is the name of the plane which can also be used
           as an attribute.
           rect is an instance of pygame.Rect giving width, height
           and render position.
           drag is a flag indicating whether this plane can be dragged.
           grab is a flag indicating whether other planes can be dropped
           on this one.
           clicked_callback and dropped_upon_callback, if given, must be
           functions.
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

        # Caches for efficient rendering
        #
        self.last_image_id = id(self.image)

        # Initialize to None to trigger a rendering
        #
        self.last_rect = None

        # Save callbacks
        #
        self.clicked_callback = clicked_callback
        self.dropped_upon_callback = dropped_upon_callback

    def sub(self, plane):
        """Remove the Plane from its current parent and add it as a subplane of this Plane.
        """

        if plane.parent is not None:

            plane.parent.remove(plane.name)

        self.subplanes_list.append(plane.name)
        self.subplanes[plane.name] = plane
        plane.parent = self

        # Reset to None to trigger a rendering
        #
        plane.last_rect = None

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

            # We do not need to worry about rendering here: once all subplanes
            # are gone, render() will point the rendersurface to image and
            # redraw.

        else:
            for name in names:
                if name in self.subplanes_list:
                    self.subplanes[name].parent = None
                    del self.subplanes[name]
                    del self.subplanes_list[self.subplanes_list.index(name)]

            # If there are still subplanes, then trigger a redraw of all of them
            # by setting their last_rect to None.
            #
            for plane in self.subplanes.values():
                plane.last_rect = None                

    def __getattr__(self, name):
        """Access subplanes as attributes.
        """

        return(self.subplanes[name])

    def render(self):
        """Draw a composite surface of this plane and all subplanes, in order of their addition.
           Returns True if anything has been rendered (i.e. if
           Plane.rendersurface has changed), False otherwise.
        """

        # We only need to render if self.rendersurface does not point
        # to self.image.
        #
        if self.rendersurface == self.image:

            return False

        else:
            # Is this correct? Maybe the user has updated the image, but
            # when there are no subplanes, there is no need to render.
            #
            if not self.subplanes:

                # Fix the pointer
                #
                self.rendersurface = self.image

                return True

            else:
                # At this point, we know that rendersurface differs from image
                # and that there are subplanes.

                # If the image of this plane or any subplane has changed or if
                # a subplane has moved: redraw everything.
                # (The alternative would be to check for rect collisions to see
                # where the background can be restored by using image, or
                # caching inbetween rendering steps).
                # TODO: This doesn't catch draw and blit operations outside render()!
                #
                subplane_changed = False

                for name in self.subplanes_list:

                    plane = self.subplanes[name]

                    if plane.render():

                        subplane_changed = True

                    elif plane.rect != plane.last_rect:

                        subplane_changed = True

                        # We need a copy!
                        #
                        plane.last_rect = pygame.Rect(plane.rect)

                if id(self.image) != self.last_image_id or subplane_changed:

                    # Observe alpha! First clear the rendersurface.
                    #
                    self.rendersurface.fill((0, 0, 0, 0))
                    
                    # Then blit this plane's image
                    #
                    self.rendersurface.blit(self.image, (0, 0))

                    # Subplanes are already rendered. Force-blit them in order.
                    #
                    for name in self.subplanes_list:

                        self.rendersurface.blit(self.subplanes[name].rendersurface,
                                                self.subplanes[name].rect)

                    self.last_image_id = id(self.image)

                    return True

                else:
                    return False

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
           If Plane.clicked_callback is set, it is called with this Plane as
           argument.
        """

        if self.clicked_callback is not None:
            self.clicked_callback(self)

        return

    def dropped_upon(self, plane, coordinates):
        """Called when a plane is dropped on top of this one.
           If Plane.grab_dropped_planes is True, the default implementation
           will remove the dropped Plane from its parent and make it a
           subplane of this one.
           If the dropped Plane is already a subplane of this one, its position
           is updated.
           If Plane.dropped_upon_callback is set, it is called with plane and
           coordinates as arguments.
        """

        if self.grab_dropped_planes:

            plane.rect.center = coordinates

            if plane.name not in self.subplanes_list:

                plane.parent.remove(plane.name)

                self.sub(plane)

        if self.dropped_upon_callback is not None:
            self.dropped_upon_callback(plane, coordinates)

        return

    def destroy(self):
        """Remove this Plane from the parent plane, remove all subplanes and delete all pygame Surfaces.
        """

        if self.parent is not None:
            self.parent.remove(self.name)
            self.parent = None

        self.remove()

        self.image = self.rendersurface = None
        self.rect = self.draggable =  self.grab_dropped_planes = None

    def __repr__(self):
        """Readable string representation.
        """

        parent_name = "None"

        if self.parent is not None:
            parent_name = self.parent.name
            
        return("<clickndrag.Plane name='{}' image={} rendersurface={} rect={} parent='{}' subplanes_list={} draggable={} grab_dropped_planes={} last_image_id={} last_rect={}>".format(self.name,
                                                      "{}@{}".format(self.image, id(self.image)),
                                                      "{}@{}".format(self.rendersurface, id(self.rendersurface)),
                                                      self.rect,
                                                      parent_name,
                                                      self.subplanes_list,
                                                      self.draggable,
                                                      self.grab_dropped_planes,
                                                      self.last_image_id,
                                                      self.last_rect))

class Display(Plane):
    """Click'n'Drag main screen class.
       A Display instance serves as the root Plane in clickndrag.

       Additional attributes:

       Display.display
           The Pygame display Surface

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
            self.display = pygame.display.set_mode(resolution_tuple)

        except pygame.error:

            # Microsoft Windows SDL error: "No available video device"
            # For a list see
            # http://www.libsdl.org/cgi/docwiki.cgi/SDL_envvars
            #
            import os

            os.environ['SDL_VIDEODRIVER']='windib'

            self.display = pygame.display.set_mode(resolution_tuple)

        Plane.__init__(self, "display", pygame.Rect((0, 0), resolution_tuple))

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

                if self.dragged_plane is not None:

                    target_plane, coordinates = self.get_plane_at(event.pos)

                    # Don't drop to self
                    #
                    if target_plane != self.dragged_plane.source:

                        target_plane.dropped_upon(self.dragged_plane.source, coordinates)

                    self.dragged_plane = None

                    # Render without dragged Plane and force-blit to Pygame
                    # display
                    #
                    self.render(force = True)

            return

    def render(self, force = False):
        """Call base class render(), then blit to the Pygame display if something has changed.
           If force is True, blit to Pygame display regardless.
        """

        # Test for Plane.render() first to trigger the rendering
        #
        if Plane.render(self) or force or self.dragged_plane is not None:

            self.display.blit(self.rendersurface, (0, 0))

            if self.dragged_plane is not None:

                # Dragged plane on top
                #
                self.dragged_plane.rect.center = pygame.mouse.get_pos()

                self.display.blit(self.dragged_plane.rendersurface,
                                  self.dragged_plane.rect)
