#
# MIT License
#
# Copyright (c) 2022 cjiang. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from PGLib.PGObject import *


class PGFrame:
    def __init__(self, parent: Union[PGScene, PGFrame], size: tuple[int, int], x: int, y: int,
                 bg: pygame.Surface = None, base: bool = False):
        self._parent = parent

        self.size = size
        self.pos = (x, y)
        if base:
            self._objects = PGGroup()
        else:
            self._objects = self._parent.group
        self._frames = []
        self._background = None
        self._backgroundSet = False
        self.background = bg

        if self._parent and not base:
            self._parent.add_object(self, x, y)

    def name(self):
        return "PGFrame"

    @property
    def background(self) -> pygame.Surface:
        return self._background

    @background.setter
    def background(self, bg: pygame.Surface = None) -> None:
        if bg:
            self._background = bg
            self._backgroundSet = True
        else:
            self._background = pygame.Surface(pygame.display.get_surface().get_size()).convert_alpha()
            self._background.fill((0, 0, 0))

    def background_set(self) -> bool:
        return self._backgroundSet

    def update_background(self) -> None:
        self._objects.clear(pygame.display.get_surface(), self._background)
        for frame in self._frames:
            frame.update_background()

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self._pos = (pos[0] + self._parent.pos[0], pos[1] + self._parent.pos[1])
        x = self._pos[0]
        y = self._pos[1]
        if self._pos[0] + self.size[0] > self._parent.pos[0] + self._parent.size[0]:
            x = self._parent.pos[0] + self._parent.size[0] - self.size[0]
        if self._pos[1] + self.size[1] > self._parent.pos[1] + self._parent.size[1]:
            y = self._parent.pos[1] + self._parent.size[1] - self.size[1]
        self._pos = (x, y)

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    # Mainly for internal use. Use resize instead.

    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._size = size

    @property
    def center(self) -> tuple[int, int]:
        return self._pos[0] + self._size[0] // 2, self._pos[1] + self._size[1] // 2

    @center.setter
    def center(self, center: tuple[int, int]) -> None:
        self.pos = (center[0] - self._size[0] // 2, center[1] - self._size[1] // 2)

    @property
    def group(self) -> PGGroup:
        return self._objects

    def add_object(self, obj: Union[PGObject, PGFrame], x: int = 0, y: int = 0):
        if obj.size[0] > self.size[0]:
            self.size = (obj.size[0], self.size[0])
        if obj.size[1] > self.size[1]:
            self.size = (obj.size[1], self.size[1])
        obj.pos = (x, y)

        self._objects.add(obj) if obj.name() == "PGObject" else self._frames.append(obj)

    def remove_object(self, obj: Union[PGObject, PGFrame]):
        self._objects.remove(obj) if obj.name() == "PGObject" else self._frames.remove(obj)

    # @function process_events
    # @abstract Process all pygame events of its objects.
    # @discussion This must be overridden if other objects have events as well.

    def process_events(self, event: pygame.event.Event) -> None:
        self._objects.process_events(event)
        for frame in self._frames:
            frame.process_events(event)

    # @function update
    # @abstract Update all objects in the scene.
    # @discussion Must be overridden if there are other objects (such as fader, background).

    def update(self) -> None:
        self._objects.update()
        for frame in self._frames:
            frame.update()

    def draw(self) -> None:
        pygame.display.update(self._objects.draw(pygame.display.get_surface()))
        for frame in self._frames:
            frame.draw()

