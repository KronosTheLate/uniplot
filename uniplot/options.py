from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np  # type: ignore


def _default_gridlines() -> List[float]:
    return [0.0]


def _default_lines() -> List[bool]:
    return [False]


@dataclass
class Options:
    # Color mode
    color: bool = False
    # Height of the plotting region, in lines
    height: int = 17
    # Interactive mode
    interactive: bool = False
    # Labels for the series
    legend_labels: Optional[List[str]] = None
    # Draw lines between points
    lines: List[bool] = field(default_factory=_default_lines)
    # Enforce a hard limit on the number of characters per line. This may override the `width` option if there is not enough space.
    line_length_hard_cap: Optional[int] = None
    # Title of the plot
    title: Optional[str] = None
    # Width of the plotting region, in characters
    width: int = 60
    # Vertical gridlines
    x_gridlines: List[float] = field(default_factory=_default_gridlines)
    # Maximum x value of the current view
    x_max: float = 1.0
    # Minimum x value of the current view
    x_min: float = 0.0
    # Units of x axis
    x_unit: str = ""
    # Horizontal gridlines
    y_gridlines: List[float] = field(default_factory=_default_gridlines)
    # Maximum y value of the current view
    y_max: float = 1.0
    # Minimum y value of the current view
    y_min: float = 0.0
    # Units of y axis
    y_unit: str = ""

    def __post_init__(self):
        # Validate values
        assert self.width > 0
        assert self.height > 0

        # Remember values for resetting later
        self._initial_bounds = (self.x_min, self.x_max, self.y_min, self.y_max)
        self._initial_width = self.width

    def shift_view_left(self) -> None:
        self.__shift_view_horizontal(factor=-1)

    def shift_view_right(self) -> None:
        self.__shift_view_horizontal(factor=1)

    def shift_view_up(self) -> None:
        self.__shift_view_vertical(factor=1)

    def shift_view_down(self) -> None:
        self.__shift_view_vertical(factor=-1)

    def zoom_in(self) -> None:
        self.__zoom_view(factor=1)

    def zoom_out(self) -> None:
        self.__zoom_view(factor=-1)

    def reset_view(self) -> None:
        (self.x_min, self.x_max, self.y_min, self.y_max) = self._initial_bounds

    def reset_width(self) -> None:
        self.width = self._initial_width

    ###########
    # private #
    ###########

    def __shift_view_horizontal(self, factor: int) -> None:
        # TODO Make the step aligned with the characters on the screen
        step: float = 0.1 * factor * (self.x_max - self.x_min)
        self.x_min = self.x_min + step
        self.x_max = self.x_max + step

    def __shift_view_vertical(self, factor: int) -> None:
        # TODO Make the step aligned with the characters on the screen
        step: float = 0.1 * factor * (self.y_max - self.y_min)
        self.y_min = self.y_min + step
        self.y_max = self.y_max + step

    def __zoom_view(self, factor: int) -> None:
        step = 0.1 * factor * (self.x_max - self.x_min)
        self.x_min = self.x_min + step
        self.x_max = self.x_max - step

        step = 0.1 * factor * (self.y_max - self.y_min)
        self.y_min = self.y_min + step
        self.y_max = self.y_max - step
