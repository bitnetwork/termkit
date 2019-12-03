import copy
import typing

from dataclasses import dataclass
from typing import List, Tuple, Union, Iterable

from .style import Color, BOLD, DIM, REVERSE, UNDERLINE, ITALIC, CONCEAL, BLINK, STRIKE, CHARSET, HYPERLINK
from .term import Terminal

@dataclass(init=True, eq=True, order=False, frozen=True)
class Cell():
  """
  Cell contains the fields representing the character, foreground color, background color and style
  attributes, respectively.

  All fields have a sentinel value indicating transparency, and that in the case of layering another layer,
  the layer should inherit the other's value. Otherwise, sentinel values are considered as empty values when
  outputting the final canvas.
  """

  char: str = ""  # empty string is transparent, all else overwrites
  fg: Union[Color, None] = None  # background color by default
  bg: Union[Color, None] = None
  fx: int = 0  # mask of attributes, all disabled by default

  def __or__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    char = self.char or other.char
    fg = self.fg or other.fg
    bg = self.bg or other.bg
    # since there is no significant use case when inheriting attributes makes any kind of rational
    # sense, it is statically implemented as taking only from the upper layer
    fx = self.fx
    return self.__class__(char, fg, bg, fx)

  def draw(self, term: Terminal):
    # there is no character to print, so short circuit and skip it
    if not self.char:
      term.move_by(x=1)
      return

    term.fg(self.fg)  # None resets the color
    term.bg(self.bg)

    # term.bold(bool(self.fx & BOLD))
    # term.dim(bool(self.fx & DIM))
    # term.reverse(bool(self.fx & REVERSE))
    # term.underline(bool(self.fx & UNDERLINE))
    # term.italic(bool(self.fx & ITALIC))
    # term.conceal(bool(self.fx & CONCEAL))
    # term.blink(bool(self.fx & BLINK))
    # term.strike(bool(self.fx & STRIKE))
    # term.charset(bool(self.fx & CHARSET))
    # term.hyperlink(bool(self.fx & HYPERLINK))

    term.write(self.char)

class Canvas():
  __slots__ = ("canvas")
  canvas: List[Cell]

  def __init__(self, rows=None, cols=None):
    self.canvas = []
    self.resize(rows=rows, cols=cols)

  def __iter__(self):
    return [cell for row in self.canvas for cell in row]

  def __or__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    rows = zip(copy.deepcopy(self.canvas), copy.deepcopy(other.canvas))
    canvas = [[s_cell | o_cell for s_cell, o_cell in zip(s_row, o_row)] for s_row, o_row in rows]

    new = self.__class__()
    new.canvas = canvas
    return new

  @property
  def rows(self) -> int:
    return len(self.canvas)

  @property
  def cols(self) -> int:
    if self.rows == 0:
      return 0
    return len(self.canvas[0])

  def resize(self, rows: int = None, cols: int = None, fill: Cell = Cell()):
    if rows is not None:
      diff = rows - self.rows
      if diff > 0:
        self.canvas += [[fill] * (cols or self.cols)] * diff
      elif diff < 0:
        del self.canvas[diff:]  # delete the trailing rows

    if cols is not None:
      diff = cols - self.cols
      if diff > 0:
        for row in self.canvas:
          row += [fill] * diff
      elif diff < 0:
        del row[diff:]  # delete the trailing columns

  def draw(self, term: Terminal, mode="relative"):
    for row in self.canvas:
      for cell in row:
        cell.draw(term)
      term.move_by(y=1)
      term.move_by(x=-self.cols)

  def diff(self, other):
    raise NotImplementedError

  def fill(self, fill: Cell):
    self.canvas = [[fill for _ in row] for row in self.canvas]


