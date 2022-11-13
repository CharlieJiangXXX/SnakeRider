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

from PGLib.PGGame import *


# TO-DO: Add minimize/maximize/close tray

class PGPopUpScene(PGScene):
    def __init__(self, game: PGGame, size: tuple[int, int], img: pygame.Surface = None):
        super().__init__(game, None)
        if not img:
            img = pygame.Surface(size)
            img.fill((0, 0, 0))
        else:
            img = pygame.transform.smoothscale(img, size)
        self._frameSetup = 0
        self._frame = PGObject(self, img=img)
        self._frame.center = pygame.display.get_surface().get_rect().center
        self._frameSetup = 1
        self._tempGroup = None

    def add_object(self, obj: PGObject):
        if self._frameSetup != 0:
            obj.pos = (self._frame.x + obj.x, self._frame.y + obj.y)
            if obj.x + obj.rect.width > self._frame.x + self._frame.rect.width:
                obj.x = self._frame.x + self._frame.rect.width - obj.rect.width
            if obj.y + obj.rect.height > self._frame.y + self._frame.rect.height:
                obj.y = self._frame.y + self._frame.rect.height - obj.rect.height
        self._objects.add(obj)

    def activate(self, trans_in: str = "none", trans_out: str = "fade_half") -> None:
        super().activate("none", "fade_half")
        self._frame.scale = 0.1
        self._frame.zoom(1)

    def draw(self) -> None:
        if self._frameSetup == 1:
            if not self._tempGroup:
                self._tempGroup = PGGroup(self._frame)
            pygame.display.update(self._tempGroup.draw(pygame.display.get_surface()))
            if self._frame.scale == 1:
                self._frameSetup = 2
            return
        elif self._frameSetup == 2:
            super().draw()

    def process_events(self, event: pygame.event.Event) -> None:
        if self._frameSetup == 2:
            super().process_events(event)

    def transition_out(self) -> bool:
        return self._frame.scale == 0

    def finish(self, trans_in: str = "fade_half", trans_out: str = "handled_internally") -> None:
        for s in self._objects.sprites():
            s.zoom(0)
        super().finish("fade_half", "handled_internally")
