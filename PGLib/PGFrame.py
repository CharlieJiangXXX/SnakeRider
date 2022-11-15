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
                 base: bool = False):
        self._parent = parent

        self.size = size
        self._relPos = (0, 0)
        self.pos = (x, y)
        self._objects = PGGroup()
        if base:
            self._parentObjects = self._objects
        else:
            self._parentObjects = self._parent.group
        self._frames = []

        if self._parent and not base:
            self._parent.add_object(self, x, y)

    def name(self):
        return "PGFrame"

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    # Mainly for internal use. Use resize instead.

    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._size = size

    # shrink function

    # Pair with update_pos()
    @property
    def abs_pos(self) -> tuple[int, int]:
        return self._pos

    @property
    def pos(self) -> tuple[int, int]:
        return self._relPos

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self._relPos = pos
        self._pos = (pos[0] + self._parent.pos[0], pos[1] + self._parent.pos[1])
        if self._pos[0] + self.size[0] > self._parent.pos[0] + self._parent.size[0]:
            self._pos = (self._parent.pos[0] + self._parent.size[0] - self.size[0], self._pos[1])
            self._relPos = (self._parent.size[0] - self.size[0], self._pos[1])
        if self._pos[1] + self.size[1] > self._parent.pos[1] + self._parent.size[1]:
            self._pos = (self._pos[0], self._parent.pos[1] + self._parent.size[1] - self.size[1])
            self._relPos = (self._pos[0], self._parent.size[1] - self.size[1])
        try:
            for object in self._objects:
                object.update_pos()
            for frame in self._frames:
                frame.update_pos()
        except AttributeError:
            return

    def update_pos(self):
        self.pos = self.pos

    @property
    def center(self) -> tuple[int, int]:
        return self._pos[0] + self._size[0] // 2, self._pos[1] + self._size[1] // 2

    @center.setter
    def center(self, center: tuple[int, int]) -> None:
        self.pos = (center[0] - self._size[0] // 2, center[1] - self._size[1] // 2)

    def set_pos_prop(self, x: float, y: float) -> None:
        self.pos = (int((self._parent.size[0] - self._size[0]) * x),
                    int((self._parent.size[1] - self._size[1]) * y))

    def set_center_prop(self, x: float, y: float) -> None:
        self.center = (int((self._parent.size[0] - self._size[0]) * x),
                       int((self._parent.size[1] - self._size[1]) * y))

    # angle
    # scale
    # alpha
    # animations

    @property
    def group(self) -> PGGroup:
        return self._objects

    def add_object(self, obj: Union[PGObject, PGFrame], x: int = 0, y: int = 0):
        if obj.size[0] > self.size[0]:
            self.size = (obj.size[0], self.size[0])
        if obj.size[1] > self.size[1]:
            self.size = (obj.size[1], self.size[1])
        obj.pos = (x, y)
        obj._parent = self

        if obj.name() == "PGObject":
            self._objects.add(obj)
            self._parentObjects.add(obj)
        else:
            self._frames.append(obj)

    def remove_object(self, obj: Union[PGObject, PGFrame]):
        if obj.name() == "PGObject":
            self._objects.remove(obj)
            self._parentObjects.add(obj)
        else:
            self._frames.remove(obj)

    def connect_click(self, action: Callable, *args, **kwargs) -> None:
        for object in self._objects:
            object.connect_click(action, *args, **kwargs)
        for frame in self._frames:
            frame.connect_click(action, *args, **kwargs)

    def connect_hover(self, action: Callable, *args, **kwargs) -> None:
        for object in self._objects:
            object.connect_hover(action, *args, **kwargs)
        for frame in self._frames:
            frame.connect_hover(action, *args, **kwargs)

    # @function process_events
    # @abstract Process all pygame events of its objects.
    # @discussion This must be overridden if other objects have events as well.

    def process_events(self, event: pygame.event.Event) -> None:
        self._objects.process_events(event)
        for frame in self._frames:
            frame.process_events(event)
