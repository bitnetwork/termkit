import functools
import importlib
import io
import os
import sys

from collections import namedtuple
from typing import Union, Iterable

import parse

from . import escape
from .style import Color

class Terminal:
  """
  Control a teletype terminal connected via a stream with escape codes.
  Most controlling methods operate directly on the stream.
  Many methods have no way of detecting support for the TTY, so exceptions won't be throw on fail.
  """
  def __init__(
    self,
    stdin: io.TextIOBase = sys.stdin,
    stdout: io.TextIOBase = sys.stdout,
  ):
    self.stdin = stdin
    self.stdout = stdout

    self.bold = False
    self.dim = False
    self.reverse = False
    self.underline = False
    self.italic = False
    self.conceal = False
    self.blink = False
    self.strike = False
    self.charset = False

  ##################################################################################################
  # Core Features
  ##################################################################################################

  def write(self, *args, **kwargs):
    self.stdout.write(*args, **kwargs)

  def bell(self):
    self.stdout.write(escape.BELL)

  def clear(self):
    self.stdout.write(escape.CLEAR)

  def clear_line(self):
    self.stdout.write(escape.CLEAR_LINE)

  def insert_line(self, row: int):
    self.stdout.write(escape.INSERT_LINE.format(row))

  def delete_line(self, row: int):
    self.stdout.write(escape.DELETE_LINE.format(row))

  def reset(self):
    self.stdout.write(escape.RESET)

  def soft_reset(self):
    self.stdout.write(escape.SOFT_RESET)

  def set_alternate_buffer(self, state: bool):
    self.stdout.write(escape.BUFFER[0 if state else 1])

  def set_keypad(self, state: bool):
    self.stdout.write(escape.KEYPAD[0 if state else 1])

  def status(self, status: str):
    self.stdout.write(escape.STATUS[0].format(status))

  def set_scroll_region(self, first: Union[None, int] = None, second: Union[None, int] = None):
    """Restrict the vertical region that scroll, insert_line and delete_line operate on."""
    if not any((first, second)):
      # Reset the scroll region first, especially if we are going to only reset one of the bounds
      # to it's natural position
      self.stdout.write(escape.SCROLL_REGION[1])

    if any((first, second)):
      self.stdout.write(escape.SCROLL_REGION[0].format(first or "", second or ""))

  def set_paste(self, state: bool):
    self.stdout.write(escape.PASTE[0 if state else 1])

  ##############################################################################
  # Cursor Logic
  ##############################################################################

  def move_by(self, x: int = 0, y: int = 0):
    """Move the cursor relatively with respect to it's current position."""
    output = ""
    if y > 0:
      output += escape.CURSOR_DOWN.format(y)
    elif y < 0:
      output += escape.CURSOR_UP.format(-y)

    if x > 0:
      output += escape.CURSOR_RIGHT.format(x)
    elif x < 0:
      output += escape.CURSOR_LEFT.format(-x)
    self.stdout.write(output)

  def move_to(self, row: int = 0, column: int = 0):
    """Move the cursor absolutely with respect to the terminal grid."""
    if column < 0:
      raise ValueError("Column cannot be negative (expected >=0, got {})".format(column))
    elif row < 0:
      raise ValueError("Row cannot be negative (expected >=0, got {})".format(row))
    self.stdout.write(escape.MOVE_CURSOR.format(row, column))

  def restore_position(self):
    """Restores the cursor position from a internal buffer."""
    self.stdout.write(escape.RESTORE_CURSOR)

  def save_position(self):
    """Saves the cursor position into a internal buffer."""
    self.stdout.write(escape.SAVE_CURSOR)

  def request_position(self):
    self.stdout.write(escape.REQUEST_CURSOR)

  def get_position(self):
    raise NotImplementedError
    # self.stdout.write(escape.REQUEST_CURSOR)
    # use event system to catch event, will probably have to use async, or we can pause the thread
    # and buffer events until we receive REPOR_CURSOR 

  def scroll(self, row_delta: int):
    """
    Scrolls the region clamped by set_scroll_region up or down, removing or adding blank lines as
    necessary.
    """
    if row_delta > 0:
      self.stdout.write(escape.SCROLL_UP.format(row_delta))
    elif row_delta < 0:
      self.stdout.write(escape.SCROLL_DOWN.format(-row_delta))

  ##############################################################################
  # Cursor Attributes
  ##############################################################################

  def set_cursor_visibility(self, state: bool):
    self.stdout.write(escape.CURSOR_VISIBILITY[0 if state else 1])

  def set_cursor_style(self, style: Union[str, None] = None, blink: bool = False):
    """
    Set the terminal cursor style.
    style can one of: "block", "underline", or "bar"."""
    # 0: blinking block.
    # 1: blinking block (default).
    # 2: steady block.
    # 3: blinking underline.
    # 4: steady underline.
    # 5: blinking bar
    # 6: steady bar
    styles = {
      "block": 2,
      "underline": 4,
      "bar": 6,
    }

    if style is None:
      self.stdout.write(escape.CURSOR_STYLE[1])
    else:
      self.stdout.write(escape.CURSOR_STYLE[0].format(styles[style] - int(blink)))

  def set_cursor_color(self, color: Union[Color, None] = None):
    if color is None:
      self.stdout.write(escape.CURSOR_COLOR[1])
    else:
      self.stdout.write(escape.CURSOR_COLOR[0].format(color.red, color.green, color.blue))

  ##############################################################################
  # Text Attributes
  ##############################################################################

  def set_bold(self, state: bool):
    self.stdout.write(escape.BOLD[1 if state else 0])

  def set_dim(self, state: bool):
    self.stdout.write(escape.DIM[1 if state else 0])

  def set_reverse(self, state: bool):
    self.stdout.write(escape.REVERSE[1 if state else 0])

  def set_underline(self, state: bool):
    self.stdout.write(escape.UNDERLINE[1 if state else 0])

  def set_italic(self, state: bool):
    self.stdout.write(escape.ITALIC[1 if state else 0])

  def set_conceal(self, state: bool):
    self.stdout.write(escape.CONCEAL[1 if state else 0])

  def set_blink(self, state: bool):
    self.stdout.write(escape.BLINK[1 if state else 0])

  def set_strike(self, state: bool):
    self.stdout.write(escape.STRIKE[1 if state else 0])

  def set_charset(self, state: bool):
    self.stdout.write(escape.CHARSET[1 if state else 0])

  def reset_style(self):
    self.stdout.write(escape.RESET_STYLE)

  ##############################################################################
  # Color
  ##############################################################################

  # def fg(self, color: Color):
  #   self.stdout.write(escape.)






  # def key_handler(self, func=None, *, keys=None):
  #   # Decorator function
  #   # Use an asterisk to lock the left-side args in place
  #   if func is None:
  #     # The function was called in the decorator so we need to return a copy of ourself as a wrapper
  #     # @key_handler(keys=[...]) or @key_handler()
  #     return functools.partial(key_handler, keys=keys)

  #   # The function directly pass in the decorator and this handler is acting like the wrapper
  #   # @key_handler

  #   # Do logic with keys
  #   # event_array.append(func)
  #   return func