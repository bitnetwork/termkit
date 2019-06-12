from typing import List, Tuple, Union

from . import Color, colors, Attribute 

class Cell():
  """
  Cell contains the fields representing the character, foreground color, background color, the attributes,
  and the attribute transparency, respectively.

  All fields have a default value indicating transparency, and that in the case of layering another layer,
  the layer should inherit the other's value.
  """

  __slots__ = ("char", "fg", "bg", "fx", "fxt")
  char: str
  fg: Union[Color, None]
  bg: Union[Color, None]
  fx: Attribute
  fxt: Attribute

  def __init__(
    self,
    char: Union[str, None] = None,
    fg: Union[Color, None] = None,
    bg: Union[Color, None] = None,
    fx: Attribute = Attribute(),
    fxt: Attribute = ~Attribute(),  # all transparent
  ):
    super().__setattr__("char", char)
    super().__setattr__("fg", fg)
    super().__setattr__("bg", bg)
    super().__setattr__("fx", fx)
    super().__setattr__("fxt", fxt)
  
  def __setattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field assignment")

  def __delattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field deletion")

  def __hash__(self):
    return hash(self.char) + hash(self.fg) + hash(self.bg) + hash(self.fx)  # fxt is negligible

  def __eq__(self, other):
    if not isinstance(other, Cell):
      return NotImplemented
    return self.char == other.char \
      and self.fg == other.fg \
      and self.bg == other.bg \
      and self.fx == other.fx \
      and self.fxt == other.fxt

  def __repr__(self):
    out = "<" + self.__class__.__name__
    if self.char is not None:
      out += f" char={self.char}"
    if self.fg is not None:
      out += f" fg={self.fg}"
    if self.bg is not None:
      out += f" bg={self.bg}"
    if self.fx is not None:
      out += f" fx={self.fx}"
    if self.fxt is not None:
      out += f" fxt={self.fxt}"
    return out

  def __add__(self, other):
    """Overwrite other over self, while inheriting transparency"""
    # maybe we should flip this around the other way
    if not isinstance(other, Cell):
      return NotImplemented

    char = other.char or self.char
    fg = other.fg or self.fg
    bg = other.bg or self.bg
    fx = (other.fx & ~other.fxt) | self.fx
    fxt = other.ftx | self.fxt
    return Cell(char, fg, bg, fx, fxt)

  def __sub__(self, other):
    """Compute differences in properties"""
    if not isinstance(other, Cell):
      return NotImplemented

    char = other.char or self.char
    fg = other.fg or self.fg
    bg = other.bg or self.bg
    fx = (other.fx & ~other.fxt) | self.fx
    fxt = other.ftx | self.fxt
    return Cell(char, fg, bg, fx, fxt)