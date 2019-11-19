from dataclasses import dataclass
import typing
from typing import List, Tuple, Union

from .style import Color, BOLD, DIM, REVERSE, UNDERLINE, ITALIC, CONCEAL, BLINK, STRIKE, CHARSET

@dataclass(init=True, eq=True, order=False, frozen=True)
class Cell():
  """
  Cell contains the fields representing the character, foreground color, background color, the attributes,
  and the attribute transparency, respectively.

  All fields have a sentinel value indicating transparency, and that in the case of layering another layer,
  the layer should inherit the other's value. Otherwise, sentiel values are considered as empty values when
  outputing the final canvas.
  """

  # empty string is transparent, all else overwrites
  char: str = ""
  # background color by default
  fg: Union[Color, None] = None
  bg: Union[Color, None] = None
  # mask of attributes, all disabled by default
  # since there is no significant use case when inheriting attributes makes any kind of rational sense,
  # it is statically implemented as taking only from the upper layer
  fx: int = 0

  # def __hash__(self):
    # return hash(self.char) + hash(self.fg) + hash(self.bg) + hash(self.fx) + hash(self.fxt)

  # def __eq__(self, other):
  #   if not isinstance(other, Cell):
  #     return NotImplemented
  #   return self.char == other.char \
  #     and self.fg == other.fg \
  #     and self.bg == other.bg \
  #     and self.fx == other.fx

  # def __repr__(self):
  #   out = "<" + self.__class__.__name__
  #   if self.char is not None:
  #     out += f" char={repr(self.char)}"
  #   if self.fg is not None:
  #     out += f" fg={repr(self.fg)}"
  #   if self.bg is not None:
  #     out += f" bg={repr(self.bg)}"
  #   if self.fx != 0:
  #     out += f" fx={bin(self.fx)}"
  #   if self.fxt < STRIKE << 1:  # highest bit + 1
  #     out += f" fxt={bin(self.fxt)}"
  #   return out + ">"

  def __add__(self, other):
    """Overwrite other over self, while inheriting transparency"""
    # maybe we should flip this around the other way
    """"""
    if not isinstance(other, Cell):
      return NotImplemented
    self.underlay(other)

  def __sub__(self, other):
    """Compute differences in properties"""
    if not isinstance(other, Cell):
      return NotImplemented
    self.damage(other)

  def overlay(self, other: "Cell") -> "Cell":
    """
    Overwrite self with values from other, filling transparency with self.

    <observer>
    <other>
    <self>
    
    >>> Cell().overlay(fx=BOLD)
    <Cell fx=0b1>

    This should never be bold and that attribute is opaque
    >>> Cell(fx=BOLD|ITALIC).overlay(fxt=~BOLD)
    <Cell fx=ITALIC fxt=-0b10>
    """
    # prioritize other's values first
    char = other.char or self.char
    fg = other.fg or self.fg
    bg = other.bg or self.bg

    # if the fxt bit is set for that attribute, ingore the set value and assume transparent
    # furthermore, if the transparent layer's fx is not transparent, use that value and clear the fxt bit
    # alternatively, if the fxt bit is not set, assume that the set value is opaque
    fx = other.fx & ~other.fxt  # don't recognise transparent bits as leigt
    fx |= self.fx & other.fxt  # only use bits marked as transparent, and if possible, make them opaque
    fxt = other.ftx
    fxt &= ~(self.fxt & other.fxt)  # retain the bits that remained transparent
    return Cell(char, fg, bg, fx, fxt)

  def underlay(self, other: "Cell") -> "Cell":
    """Overwrite other with values from self, filling transparency with other"""
    return other.overlay(self)
    # char = self.char or other.char
    # fg = self.fg or other.fg
    # bg = self.bg or other.bg
    # # if the fxt bit is set for that attribute, ingore the set value and assume transparent
    # fx = self.fx & ~self.fxt | other.fx
    # fxt = self.fxt | other.fxt
    # return Cell(char, fg, bg, fx, fxt)

  def damage(self, other: "Cell"):
    raise NotImplementedError()

class Canvas():
  __slots__ = ("canvas")
  canvas: List[Cell]

  def __init__(self, rows=None, cols=None):
    self.canvas = []
    self.resize(rows=rows, cols=cols)

  @property
  def rows(self):
    return len(self.canvas)

  @property
  def cols(self):
    if self.rows == 0:
      return 0
    return len(self.canvas[0])

  def resize(self, rows: int = None, cols: int = None, fill: Cell = Cell()):
    if rows is not None:
      diff = rows - self.rows
      if diff > 0:
        self.canvas.extend([fill] * (cols or self.cols))
      elif diff < 0:
        del self.canvas[diff:]  # delete the trailing rows

    if cols is not None:
      diff = cols - self.cols
      if diff > 0:
        for row in self.canvas:
          row.extend([fill] * diff)
      elif diff < 0:
        del row[diff:]  # delete the training columns


