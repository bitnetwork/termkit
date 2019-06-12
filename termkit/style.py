from collections import defaultdict, namedtuple
from math import sqrt
from typing import Dict, List, Tuple, Union

class Attribute:
  __slots__ = ("mask", )
  mask: int

  BOLD =      0b00000001
  DIM =       0b00000010
  REVERSE =   0b00000100
  UNDERLINE = 0b00001000
  ITALIC =    0b00010000
  CONCEAL =   0b00100000
  BLINK =     0b01000000
  STRIKE =    0b10000000

  def __init__(
    self,
    mask: int = None,
    *_,
    bold: bool = False,
    dim: bool = False,
    reverse: bool = False,
    underline: bool = False,
    italic: bool = False,
    conceal: bool = False,
    blink: bool = False,
    strike: bool = False,
  ):
    if mask is None:
      mask = bold*self.BOLD | dim*self.DIM | reverse*self.REVERSE | underline*self.UNDERLINE | italic*self.ITALIC \
        | conceal*self.CONCEAL | blink*self.BLINK | strike*self.STRIKE
    super().__setattr__("mask", mask)

  def __setattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field assignment")

  def __delattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field deletion")

  def __hash__(self):
    return hash(self.mask)

  def __eq__(self, other):
    if not isinstance(other, Attribute):
      return NotImplemented
    return self.mask == other.mask

  def __and__(self, other):
    if not isinstance(other, Attribute):
      return NotImplemented
    return self.__class__(self.mask & other.mask)

  def __or__(self, other):
    if not isinstance(other, Attribute):
      return NotImplemented
    return self.__class__(self.mask | other.mask)

  def __xor__(self, other):
    if not isinstance(other, Attribute):
      return NotImplemented
    return self.__class__(self.mask ^ other.mask)

  def __invert__(self):
    return self.__class__(~self.mask)

  def __int__(self):
    return self.mask

  @property
  def bold(self):
    return self.mask & self.BOLD == self.BOLD

  @property
  def dim(self):
    return self.mask & self.DIM == self.DIM

  @property
  def reverse(self):
    return self.mask & self.REVERSE == self.REVERSE

  @property
  def underline(self):
    return self.mask & self.UNDERLINE == self.UNDERLINE

  @property
  def italic(self):
    return self.mask & self.ITALIC == self.ITALIC

  @property
  def conceal(self):
    return self.mask & self.CONCEAL == self.CONCEAL

  @property
  def blink(self):
    return self.mask & self.BLINK == self.BLINK

  @property
  def strike(self):
    return self.mask & self.STRIKE == self.STRIKE
