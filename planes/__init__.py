"""planes
   A Hierarchical Surface Framework for PyGame
   Copyright 2010-2013 by Florian Berger <fberger@florian-berger.de>
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

# Planned in mind at the Mosel valley in late July 2010
# Actual work started on 01. Oct 2010

# TODO: add Plane.offset(x, y) to offset all subplanes - without touching their rect -> only while rendering
# TODO: Surface.get_flags has all sorts of interesting information to optimise performance.
# TODO: Planes *so* needs live performance reporting. Maybe not via log file, but as some sort of a live display via TTY or socket.
# TODO: replace Plane.subplanes and Planes.subplanes_list with collections.OrderedDict and OrderedDict.keys()?

import pygame
import time
import random
import platform

VERSION = "0.6.1"

# Set up hi-res timer.
# Taken from exercises written for my Real-Time Interactive Systems course in 2013.
#
TIMER_FUNC = None

if platform.system().lower() == "windows":

    TIMER_FUNC = time.clock

else:
    TIMER_FUNC = time.time

class Plane:
    """A Plane is a surface in a hierarchy of surfaces.
       Concept-wise it bears some similarities to pygame.sprite.Sprite.

       Planes are currently not thread safe! Accessing a Plane from several
       threads may produce unexpected results and errors.

       Attributes:

       Plane.name
           Name of the plane.

       Plane.image
           The pygame.Surface for this Plane.

       Plane.rect
           The render position of this Plane on the parent Plane.

       Plane.parent
           The parent plane. Initially None.

       Plane.subplanes
           Dict of subplanes, identified by their name.

       Plane.subplanes_list
           A list of subplane names, in order of their addition

       Plane.draggable
           Boolean flag. If True, this Plane can be dragged and dropped.

       Plane.grab
           Boolean flag. If True, this Plane will remove dropped Planes from
           their parent Plane and make it a subplane of this one.
           Handled in Plane.dropped_upon()

       Plane.highlight
           Boolean flag. If True, the Plane be highlighted when the mouse cursor
           moves over it.

       Plane.last_image_id
           Caches object id of the image at last rendering for efficiency.

       Plane.last_rect
           Caches rect at last rendering for efficiency.

       Plane.left_click_callback
           Callback function when this plane has been clicked with the left
           mouse button.

       Plane.right_click_callback
           Callback function when this plane has been clicked with the right
           mouse button.

       Plane.up_click_callback
           Callback function when the mouse wheel has been moved up above this
           Plane.

       Plane.down_click_callback
           Callback function when the mouse wheel has been moved down above this
           Plane.

       Plane.dropped_upon_callback
           Callback function when a plane has been dropped upon this plane.

       Plane.mouseover_callback
           Callback function when the mouse cursor moves over this plane.

       Plane.mouseout_callback
           Callback function when the mouse cursor has left this plane.

       Plane.mouseover
           Flag indicating whether the mouse cursor is over this Plane.
           Initially False.

       Plane.sync_master_plane
          A Plane that this Plane's position will sync to. Initally None.

       Plane.offset
          A tuple (x, y) describing the offset to the sync master plane.
          Initially None.
    """

    # TODO: it should be possible to initialise a Plane with a Pygame Surface, for convenvience.
    #
    def __init__(self,
                 name,
                 rect,
                 draggable = False,
                 grab = False,
                 highlight = False,
                 left_click_callback = None,
                 right_click_callback = None,
                 up_click_callback = None,
                 down_click_callback = None,
                 dropped_upon_callback = None):
        """Initialize the Plane.
           name is the name of the plane which can also be used
           as an attribute.
           rect is an instance of pygame.Rect giving width, height
           and render position.
           draggable is a flag indicating whether this plane can be dragged.
           grab is a flag indicating whether other planes can be dropped
           on this one.
           clicked_callback and dropped_upon_callback, if given, must be
           functions.
           Planes are filled with solid black color by default.
        """

        self.name = name

        # We do not use the SRCALPHA flag because it considerably slows down the
        # rendering. If an application needs per-pixel alpha, it can always
        # substitute Plane.image with an RGBA Surface.
        #
        self.image = pygame.Surface(rect.size, flags = pygame.HWSURFACE)

        # Transparent by default, so let's paint it black
        #
        self.image.fill((0, 0, 0, 255))

        # Rect is relative to the parent plane, not to the display!
        #
        self.rect = rect

        self.draggable = draggable
        self.grab = grab

        self.highlight = highlight
        self.mouseover = False

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
        self.left_click_callback = left_click_callback
        self.right_click_callback = right_click_callback
        self.up_click_callback = up_click_callback
        self.down_click_callback = down_click_callback
        self.dropped_upon_callback = dropped_upon_callback

        # Master plane for synchronous movements
        #
        self.sync_master_plane = None
        self.offset = None

        return

    def sub(self, plane, insert_after = None):
        """Remove the Plane given from its current parent and add it as a subplane of this Plane.

           If insert_after is given, the new subplane will be inserted
           immediately after the subplane with that name in Plane.subplanes_list,
           else it will simply be appended.

           If a subplane with the same name already exists, it is silently
           replaced by the new plane.
        """

        if plane.parent is not None:

            plane.parent.remove(plane.name)

        if plane.name in self.subplanes_list:

            del self.subplanes_list[self.subplanes_list.index(plane.name)]

        if insert_after is not None and insert_after in self.subplanes_list:

            self.subplanes_list.insert(self.subplanes_list.index(insert_after) + 1,
                                       plane.name)

        else:
            self.subplanes_list.append(plane.name)

        self.subplanes[plane.name] = plane

        plane.parent = self

        # Reset to None to trigger a rendering
        #
        plane.last_rect = None

        return

    def remove(self, plane_identifier):
        """Remove subplane by name or Plane instance.
        """

        # Accept Plane name as well as Plane instance
        #
        if isinstance(plane_identifier, Plane):

            name = plane_identifier.name

        else:
            name = plane_identifier

        if name in self.subplanes_list:
            self.subplanes[name].parent = None
            del self.subplanes[name]
            del self.subplanes_list[self.subplanes_list.index(name)]

        # If there are still subplanes, then trigger a redraw of all of them
        # by setting their last_rect to None.
        #
        for plane in self.subplanes.values():

            plane.last_rect = None

        return

    def remove_all(self):
        """Convenience method to call Plane.remove() for all subplanes.
        """

        # Make a copy since subplanes_list will be changed by remove()
        #
        for name in list(self.subplanes_list):

            self.remove(name)

        return

    def __getattr__(self, name):
        """Access subplanes as attributes.
        """

        # The Python interpreter has already checked instance and class
        # attributes. If this fails, an appropriate KeyError will be raised.
        #
        return self.subplanes[name]

    def render(self, rendersurface, offset_rect):
        """Draw a composite surface of this plane and all subplanes, in order of their addition.

           rendersurface is a Pygame Surface to render to.

           offset_rect is a Pygame Rect giving the offset and the
           clipping area.
        
           This method will highlight subplanes that have the
           Plane.mousover flag set.
        """

        # TODO: Taking the time, of course, takes time. Use in assert() and debug only?
        #
        timestamp = TIMER_FUNC()

        STATS.total_pixels += self.rect.width * self.rect.height

        # Force-blit subplanes in order. Obey mouseover flag.
        # Unconditionally redraw everything.
        #
        # (The alternative would be to check for rect collisions to
        # see where the background can be restored by using image, or
        # caching inbetween rendering steps).

        # Make blits look like they only affect the current surface
        #
        rendersurface.set_clip(offset_rect)

        for subplane in (self.subplanes[name] for name in self.subplanes_list):

            # First blit the image, so it forms the background
            # for further blits of subplane-subplanes
            #
            rendersurface.blit(subplane.image,
                               subplane.rect.move(offset_rect.topleft))

            # Add a highlight on top if mouseover is set
            #
            if subplane.mouseover:

                overlay = subplane.image.copy()

                # Only premultiply Surfaces with the SRCALPHA flag,
                # will raise an exception otherwise.
                #
                if overlay.get_flags() & 0x00010000:

                    # Premultiply alpha channel to RGB.
                    # Otherwise invisible RGB values will be
                    # added by BLEND_ADD. Technique suggested
                    # by Rene Dudfield <renesd@gmail.com> on
                    # pygame-users@seul.org on 19 Dec 2011
                    #
                    overlay = pygame.image.fromstring(pygame.image.tostring(overlay,
                                                                            "RGBA_PREMULT"),
                                                      overlay.get_size(),
                                                      "RGBA")

                overlay.blit(overlay, (0, 0), special_flags = pygame.BLEND_MULT)
                overlay.blit(overlay, (0, 0), special_flags = pygame.BLEND_MULT)

                rendersurface.blit(overlay,
                                   subplane.rect.move(offset_rect.topleft),
                                   special_flags = pygame.BLEND_ADD)

            # Now recurse depth-first into subplanes of this
            # subplane

            subplanetimestamp = TIMER_FUNC()

            # TODO: bookkeeping: count rendered Planes - (but isn't that done by recursion?)

            subplane.render(rendersurface,
                            pygame.Rect((subplane.rect.x + offset_rect.x,
                                         subplane.rect.y + offset_rect.y),
                                        self.rect.size))

            # Do note take render times of subplanes into account
            #
            timestamp += TIMER_FUNC() - subplanetimestamp

        # Clean up for future draw operations
        #
        rendersurface.set_clip(None)

        self.last_image_id = id(self.image)

        STATS.plane_times.append(((TIMER_FUNC() - timestamp)* 1000,
                                  self.name,
                                  len(self.subplanes_list)))

        return
        
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

        return (return_plane, return_coordinates)

    def update(self):
        """Update hook. The default implementation calls update() on all subplanes.

           If Plane.sync_master_plane is not None, the position of this
           Plane will be synced to that of the master Plane, using
           Plane.offset.

           Compare pygame.sprite.Sprite.update.
        """

        # update() will be called for all planes.
        #
        STATS.total_planes += 1

        # Subplanes may be destroyed in update(). So, create a list copy in case
        # self.subplanes changes during iteration.
        #
        for plane in list(self.subplanes.values()):

            plane.update()

        if self.sync_master_plane is not None:

            self.rect.center = (self.sync_master_plane.rect.centerx + self.offset[0],
                                self.sync_master_plane.rect.centery + self.offset[1])

        return

    def del_image(self):
        """Convenience method, replacing this Plane's image with a transparent 1px x 1px Pygame Surface.

           Plane.rect is left as-is.
        
           Useful for container surfaces which have no background.
        """

        self.image = pygame.Surface((1, 1))

        self.image.set_alpha(0, pygame.RLEACCEL)
        
        return
        
    def clicked(self, button_name):
        """Called when there is a MOUSEDOWN event on this plane.
           If click callbacks are set, the appropriate one is called with this
           Plane as argument.
        """

        if button_name == "left" and self.left_click_callback is not None:

            self.left_click_callback(self)

        elif button_name == "right" and self.right_click_callback is not None:

            self.right_click_callback(self)

        elif button_name == "up" and self.up_click_callback is not None:

            self.up_click_callback(self)

        elif button_name == "down" and self.down_click_callback is not None:

            self.down_click_callback(self)

        return

    def dropped_upon(self, plane, coordinates):
        """If a plane is dropped on top of this one, call dropped_upon_callback() and conditionally grab it.

           If Plane.grab is True, the default implementation will remove the
           dropped Plane from its parent and make it a subplane of this one.

           If the dropped Plane is already a subplane of this one, its position
           is updated.

           If Plane.dropped_upon_callback is set, it is called with
           Plane.dropped_upon_callback(self, plane, coordinates)
        """

        if self.grab:

            plane.rect.center = coordinates

            if plane.name not in self.subplanes_list:

                plane.parent.remove(plane.name)

                self.sub(plane)

        if self.dropped_upon_callback is not None:
            self.dropped_upon_callback(self, plane, coordinates)

        return

    def destroy(self):
        """Remove this Plane from the parent plane, remove all subplanes and delete all pygame Surfaces.
        """

        if self.parent is not None:

            self.parent.remove(self.name)

        self.remove_all()

        self.image = self.rect = self.draggable =  self.grab = None

        self.unsync()

        return

    def sync(self, master_plane):
        """Save the Plane given as master Plane and the position offset to that Plane for position synchronisation in Plane.update().
        """

        self.sync_master_plane = master_plane

        # Using the offset between the centers of the Planes
        #
        self.offset = (self.rect.centerx - master_plane.rect.centerx,
                       self.rect.centery - master_plane.rect.centery)

        return

    def unsync(self):
        """Remove the position synchronisation to the sync master Plane.
        """

        self.sync_master_plane = self.offset = None

        return

    def mouseover_callback(self):
        """Callback function when the mouse cursor moves over this plane.
           The default implementation sets Plane.mouseover to True when
           Plane.highlight is set.
        """

        if self.highlight:

            self.mouseover = True

            # Set to None to trigger a rendering
            #
            self.last_rect = None

        return

    def mouseout_callback(self):
        """Callback function when the mouse cursor has left this plane.
           The default implementation sets Plan.mouseover to False.
        """

        # Not checking self.highlight here - it might have changed

        self.mouseover = False

        # Set to None to trigger a rendering
        #
        self.last_rect = None

        return

    def random_name(self):
        """Return a random string that is not in Plane.subplanes_list.
           This is a convenience function to produce names for subplanes.
        """

        name = None

        while name is None or name in self.subplanes_list:

            name = "subplane{0}".format(str(random.randint(0, 99999)))

        return name

    def __repr__(self):
        """Readable string representation.
        """

        parent_name = "None"

        if self.parent is not None:
            parent_name = self.parent.name


        repr_str = "<planes.Plane name='{0}' image={1} rect={2} parent='{3}' subplanes_list={4} draggable={5} grab={6} last_image_id={7} last_rect={8} left_click_callback={9} right_click_callback={10} dropped_upon_callback={11} sync_master_plane={12}>"

        return repr_str.format(self.name,
                               "{0}@{1}".format(self.image, id(self.image)),
                               self.rect,
                               parent_name,
                               self.subplanes_list,
                               self.draggable,
                               self.grab,
                               self.last_image_id,
                               self.last_rect,
                               self.left_click_callback,
                               self.right_click_callback,
                               self.dropped_upon_callback,
                               self.sync_master_plane)

class Display(Plane):
    """planes main screen class.
       A Display instance serves as the root Plane in planes.

       Additional attributes:

       Display.display
           The Pygame display Surface

       Display.dragged_plane
           The currently dragged plane

       Display.key_sensitive_plane
           The Plane to be notified of Pygame keyboard events. Initially None.

       Display.last_mouseover_plane
           The last Plane a mouseover condition was found for. Initially None.

       Display.mouse_buttons
           A dict mapping Pygame mouse button numbers to description strings.

       Display.show_stats
           Boolean flag to indicate whether to display performance statistics.
           Set in Display.process() by examining user input. Initially False.

       Display.font
           A pygame.font.Font instance using the system default font.
    """

    def __init__(self, resolution_tuple, fullscreen = False):
        """Calling pygame.display.set_mode().
           If fullscreen is True, the display will use the full screen.
        """

        # Init Pygame, just to be on the safe side.
        # pygame.init() can safely be called more than once.
        #
        pygame.init()

        # TODO: Use flags = pygame.HWSURFACE | pygame.DOUBLEBUF ?
        #
        flags = 0

        if fullscreen:

            flags = flags | pygame.FULLSCREEN

        try:
            self.display = pygame.display.set_mode(resolution_tuple, flags)

        except pygame.error:

            # Microsoft Windows SDL error: "No available video device"
            # For a list see
            # http://wiki.libsdl.org/FAQUsingSDL
            #
            import os

            os.environ['SDL_VIDEODRIVER'] = 'windib'

            self.display = pygame.display.set_mode(resolution_tuple, flags)

        Plane.__init__(self, "display", pygame.Rect((0, 0), resolution_tuple))

        self.draggable = False

        # Keep track of the dragged plane
        #
        self.dragged_plane = None

        self.key_sensitive_plane = None

        self.last_mouseover_plane = None

        self.mouse_buttons = {1: "left",
                              3: "right",
                              4: "up",
                              5: "down"}

        self.show_stats = False

        self.font = pygame.font.SysFont("Bitstream Vera Sans,DejaVu Sans,Verdana",
                                        14)

        # Convenience Surface for statistics display.
        # See Display.render()
        #
        self._stats_surface = pygame.Surface((320, 600))

        self._stats_surface.convert()

        # Make transparent. Currently has only a limited effect, since it might
        # be blitted over itself in render().
        #
        self._stats_surface.set_alpha(196, pygame.RLEACCEL)

        return

    def key_sensitive(self, plane):
        """Register the Plane given as sensitive to Pygame keyboard events.
           Display will call plane.keydown(KEYDOWN_event) when a key is
           pressed and the Plane has a parent.
           plane.activate() will be called when the plane is registered.
           plane.deactivate() will be called on the old plane.
        """

        # TODO: there should be a class containing keydown(), activate(), deactivate()

        if self.key_sensitive_plane:

            self.key_sensitive_plane.deactivate()

        self.key_sensitive_plane = plane

        self.key_sensitive_plane.activate()

        return

    def process(self, event_list):
        """Process a pygame event list.
           This is the main method of planes and should be called once per
           frame.
           It will also check mouseover conditions, even if event_list is empty.
        """

        # We will only process mouseovers when nothing else has happened.
        # So we set up a flag here.
        #
        nothing_happened = True

        for event in event_list:

            if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button in self.mouse_buttons.keys()):

                nothing_happened = False

                clicked_plane = self.get_plane_at(event.pos)[0]

                # Cant just compare to self in Python < 3.0.
                # Use id instead.
                #
                if id(clicked_plane) != id(self):

                    button_name = self.mouse_buttons[event.button]

                    # Notify plane instance
                    #
                    clicked_plane.clicked(button_name)

                    if button_name == "left" and clicked_plane.draggable:

                        # Use a copy for new coordinates etc.
                        #
                        self.dragged_plane = Plane("dragged_plane", clicked_plane.rect.copy())

                        # Drag a composite of the Plane and
                        # all subplanes
                        #
                        self.dragged_plane.image = clicked_plane.image.copy()

                        clicked_plane.render(self.dragged_plane.image,
                                             pygame.Rect((0, 0), clicked_plane.rect.size))

                        # Keep original for reference
                        #
                        self.dragged_plane.source = clicked_plane

                        # 2/3 transparency. Only visible when there
                        # are no per-pixel alphas.
                        #
                        self.dragged_plane.image.set_alpha(170, pygame.RLEACCEL)

            elif (event.type == pygame.MOUSEBUTTONUP
                  and event.button == 1):

                # Left button == 1, right button == 3

                nothing_happened = False

                if self.dragged_plane is not None:

                    target_plane, coordinates = self.get_plane_at(event.pos)

                    # Don't drop to self
                    # Cant compare Planes in Python < 3.0.
                    # Use id instead.
                    #
                    if id(target_plane) != id(self.dragged_plane.source):

                        target_plane.dropped_upon(self.dragged_plane.source, coordinates)

                    self.dragged_plane = None

                    # Render without dragged Plane and force-blit to Pygame
                    # display
                    #
                    self.render(force = True)

            # Hardwire F12 key to stats display.
            # Catch it before forwarding keys to key_sensitive_plane.
            #
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_F12):

                # Reverse
                #
                if self.show_stats:

                    self.show_stats = False

                else:
                    self.show_stats = True

                    # Print the planes hierarchy to STDOUT
                    # TODO: display on screen instead of STDOUT
                    #
                    def print_subplanes(plane, indent = 1):
                        """Helper method to print an indented list of subplanes.
                           To be called recursively.
                        """
                        if len(plane.subplanes_list):
                            for subplane in plane.subplanes.values():
                                print("|   " * (indent - 1) + "+---" + subplane.name)
                                print_subplanes(subplane, indent + 1)
                        return

                    print("---------------------\nPlanes hierarchy dump\n---------------------")
                    print(self.name)
                    print_subplanes(self)

            elif (event.type == pygame.KEYDOWN
                  and self.key_sensitive_plane is not None
                  and self.key_sensitive_plane.parent is not None):

                nothing_happened = False

                # TODO: remove a destroyed Plane from key_sensitive_plane

                # Notify the latest registered listener
                #
                self.key_sensitive_plane.keydown(event)

        # All events have been processed now. If nothing happened, process
        # mouseover.
        #
        if nothing_happened:

            try:

                mouseover_plane = self.get_plane_at(pygame.mouse.get_pos())[0]

            except pygame.error:

                # This most probably means that Pygame has been shut down in the
                # meantime.
                #
                return

            if id(mouseover_plane) == id(self.last_mouseover_plane):

                # Still over it. No action.
                #
                pass

            else:

                if self.last_mouseover_plane is not None:

                    self.last_mouseover_plane.mouseout_callback()

                if id(mouseover_plane) == id(self):

                    # Ignore the Display
                    #
                    self.last_mouseover_plane = None

                else:

                    mouseover_plane.mouseover_callback()

                    self.last_mouseover_plane = mouseover_plane

        return

    def render(self, force = False):
        """Call base class render(), then blit to the Pygame display if something has changed.
           If force is True, blit to Pygame display regardless.
        """

        starttime = time.clock()

        self.display.blit(self.image, (0, 0))

        rendered_something = Plane.render(self, self.display, self.rect)

        STATS.log_render_time(time.clock() - starttime)

        if rendered_something or force or self.dragged_plane is not None:

            if self.dragged_plane is not None:

                # For some reason MOUSEBUTTONUP is sometimes missed.
                # Check whether button is still pressed
                #
                if pygame.mouse.get_pressed() != (0, 0, 0):

                    # Dragged plane on top
                    #
                    self.dragged_plane.rect.center = pygame.mouse.get_pos()

                    self.display.blit(self.dragged_plane.image,
                                      self.dragged_plane.rect)

                else:
                    # Delete without dropping
                    #
                    self.dragged_plane = None

        if self.show_stats:

            # Font.render(text, antialias, color, background)

            antialias = True

            color = (255, 255, 255)

            background = (64, 64, 64)

            padding = 5

            lineheight = self.font.get_height() + padding

            self._stats_surface.fill(background)

            y = 3

            self._stats_surface.blit(self.font.render("planes {0} Runtime Statistics".format(VERSION),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Total planes: {0}".format(STATS.total_planes),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Total pixels: {0:.1f} M, {1:.2f} MB RGB video RAM".format(STATS.total_pixels / 1000000, STATS.total_pixels * 24 / 8 / 1024 / 1024),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Render time: {0:.1f} ms".format(STATS.render_time * 1000),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Mean render time: {0:.1f} ms".format(STATS.mean_render_time * 1000),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Mean rendering capacity: {0} renderings / s".format(STATS.renders_per_second),
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            y += lineheight

            self._stats_surface.blit(self.font.render("Accumulated subplane render times:",
                                                      antialias,
                                                      color,
                                                      background), (padding, y))

            STATS.plane_times.sort()
            STATS.plane_times.reverse()

            msg = "    {0}: {1:.1f} ms ({2} subplanes)"
                
            # Use top ten
            #
            for time_name_tuple in STATS.plane_times[:10]:

                y += lineheight

                self._stats_surface.blit(self.font.render(msg.format(time_name_tuple[1],
                                                                     time_name_tuple[0],
                                                                     time_name_tuple[2]),
                                                          antialias,
                                                          color,
                                                          background), (padding, y))

            self.display.blit(self._stats_surface, (10, 10))

            # Update and reset stats counter
            #
            STATS.update(self)

        return

class Stats:
    """A Stats instance stores and computes several runtime statistics.

       Attributes:

       Stats.total_planes
           Total number of planes.

       Stats.total_pixels
           Total number of pixels allocated for all planes.

       Stats.render_time
           Time of last call to Display.render().

       Stats.mean_render_time
           Mean of the time of the last 30 calls to Display.render().

       Stats.renders_per_second
           Given Stats.mean_render_time, how many renders could be carried out
           in one second in theory. Note that this is not the actual FPS, which
           is largely determined by the application deploying the planes module.

       Stats.plane_times
           A list of tuples (rendertime, name, subplane_count) giving
           the last render time of each plane.
    """

    # TODO: A Stats instance could be an iterator, yielding text Surfaces and rendering positions.

    def __init__(self):
        """Initialise.
        """

        self.total_planes = 0

        self.total_pixels = 0

        self.render_time = 0

        self._render_time_list = []

        self.mean_render_time = 0

        self.renders_per_second = 0

        self.plane_times = []

        return

    def update(self, display):
        """Actively update stats from the display instance given, and reset frame-to-frame counters.
        """

        self.total_planes = 0

        self.total_pixels = 0

        self.plane_times = []

        # self.render_time will be entirely handled from the outside and
        # needs no reset.

        if len(self._render_time_list):

            self.mean_render_time = sum(self._render_time_list) / len(self._render_time_list)

        if self.mean_render_time > 0:

            self.renders_per_second = int(1 / self.mean_render_time)

        return

    def log_render_time(self, render_time):
        """Set Stats.render_time to the time given, and register that time for computing the mean.
        """

        self. render_time = render_time

        self._render_time_list.append(render_time)

        # Keep it at 30 values
        #
        if len(self._render_time_list) > 30:

            self._render_time_list.pop(0)

        return

# As there will only ever be one Display instance, we can keep a global
# Stats instance and do not need to do it on a per-Display base.
#
STATS = Stats()
