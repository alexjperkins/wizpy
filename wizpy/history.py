import collections
from typing import Dict

from . menu import IMenu


class MenuHistory:
    def __init__(self):
        self._history = collections.deque()
        self._future = collections.deque()
        self._current = None

    def push(self, *, menu: IMenu) -> None:
        if self._current is not None:
            self._history.append(self._current)

        self._current = menu
        return None

    def pop(self) -> IMenu:
        self._future.appendleft(self._current)
        self._current = self._history.pop()
        return self._current

    def go_forward(self) -> IMenu:
        if self._future:
            self.push(menu=self._future.popleft())

        return self._current

    def go_back(self) -> IMenu:
        if self._history:
            self.pop()

        return self._current

    @property
    def current(self) -> IMenu:
        return self._current
