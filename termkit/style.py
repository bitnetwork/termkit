import colorsys
import typing

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple, Union

# from termkit import escape

__all__ = [
  "ID_MAP", "NAME_MAP", "GAMMA", "gamma_expansion", "gamma_compression", "Color",
  "BOLD", "DIM", "REVERSE", "UNDERLINE", "ITALIC", "CONCEAL", "BLINK", "STRIKE", "CHARSET",
  "HYPERLINK",
]

# predefine the internal collections so they are visible to Colors, as they contain instances of Color
ID_MAP = []
NAME_MAP = []
GAMMA = 2.2

def gamma_expansion(channel: int, gamma=GAMMA) -> int:
  """Converts a non-linear color channel to a linear one"""
  return round((channel / 255) ** gamma * 255)

def gamma_compression(channel: int, gamma=GAMMA) -> int:
  """Converts a linear color channel to a non-linear one"""
  return gamma_expansion(channel, 1 / gamma)

@dataclass(init=True, eq=True, order=False, frozen=True)
class Color():
  """
  Abstraction of a quadratic space RGB color.

  >>> Color(red=255, green=0, blue=0)
  Color(red=255, green=0, blue=0)

  >>> Color(255, 0, 0)
  Color(red=255, green=0, blue=0)
  """

  red: int = 0
  green: int = 0
  blue: int = 0

  def __hex__(self) -> str:
    return f"0x{self.red:02x}{self.green:02x}{self.blue:02x}"

  def __iter__(self):
    return iter((self.red, self.green, self.blue))

  # def __add__(self, other):
    # defined later as
    # self.mix(other)

  def difference(self, other: "Color", gamma=GAMMA) -> float:
    """Computes the euclidean difference between two colors"""
    result = 0.0

    # find the linear average between the colors
    for self_channel, other_channel in zip(self, other):
      difference = gamma_expansion(self_channel, gamma=gamma) - gamma_expansion(other_channel, gamma=gamma)
      result += abs(difference)

    return result

  def closest_color(self, colors: Iterable["Color"], gamma=GAMMA) -> Tuple["Color", float]:
    """
    Finds the closest color in the color mapping.

    >>> Color(0, 0, 239).closest_color(ID_MAP)
    (Color(red=0, green=0, blue=255), 34.0)

    Downscale a color to the 16 color space
    >>> ID_MAP[60].closest_color(ID_MAP[:16])
    (Color(red=128, green=128, blue=128), 61.0)
    """
    # short circuit
    if self in colors:
      return (self, 0)

    # search in iterable
    sums = tuple((color, i) for i, color in enumerate(colors))
    return min(sums, key=lambda pair: self.difference(pair[0], gamma=gamma))

  def mix(self, other: "Color", gamma=GAMMA) -> "Color":
    """
    Mixes two colors, constructing a new color

    >>> NAME_MAP["red"].mix(NAME_MAP["blue"])
    Color(red=186, green=0, blue=186)

    >>> NAME_MAP["white"].mix(NAME_MAP["black"])
    Color(red=186, green=186, blue=186)
    """
    channels = []

    # find the linear average between the colors
    for self_channel, other_channel in zip(self, other):
      average = gamma_expansion(self_channel, gamma=gamma) + gamma_expansion(other_channel, gamma=gamma)
      average /= 2
      channels.append(gamma_compression(round(average), gamma=gamma))

    return self.__class__(*channels)

  __add__ = mix

# ID_MAP += [Color(*color[0]) for color in escape.COLORS]

# NAME_MAP += [color[1] for color in escape.COLORS]

# text attributes
BOLD =      0b0000000001
DIM =       0b0000000010
REVERSE =   0b0000000100
UNDERLINE = 0b0000001000
ITALIC =    0b0000010000
CONCEAL =   0b0000100000
BLINK =     0b0001000000
STRIKE =    0b0010000000
CHARSET =   0b0100000000
HYPERLINK = 0b1000000000

if __name__ == "__main__":
  import doctest
  doctest.testmod()
