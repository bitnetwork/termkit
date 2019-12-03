import functools
import importlib
import io
import os
import sys

from collections import namedtuple
from typing import Union, Iterable, List

import parse

from . import escape
from . import style

from .escape import Key
from .style import Color

__all__ = ["Terminal"]

# TODO: write support detection for color, truecolor, and terminal size
# NOTE: we can print the 256 color sequence, then the truecolor one, and terminals which only
#       recognise the 256 one will ignore the truecolor one
# https://stackoverflow.com/questions/40931467/how-can-i-manually-get-my-terminal-to-return-its-character-size?noredirect=1&lq=1
# https://stackoverflow.com/questions/31619962/vt100-ansi-escape-sequences-getting-screen-size-conditional-ansi#31894026

class Terminal:
  """
  Control a teletype terminal connected via a stream with escape codes.
  Most controlling methods operate directly on the stream.
  Many methods have no simple way of detecting support for the TTY, so
  exceptions generally won't be raised if there is no support. Often times,
  many attributes are failsafe by design, in that they won't display on
  unsupported devices.
  """
  def __init__(
    self,
    stdin: io.TextIOBase = sys.stdin,
    stdout: io.TextIOBase = sys.stdout,
    *_,
    colors: int = 8,
    truecolor: bool = False,
  ):
    self.stdin = stdin
    self.stdout = stdout
    self.colors = colors
    self.truecolor = truecolor

  def write(self, *args, **kwargs):
    self.stdout.write(*args, **kwargs)

  # Terminal function
  def bell(self):
    self.stdout.write(escape.BELL)

  def clear(self):
    self.stdout.write(escape.CLEAR)

  def reset(self):
    self.stdout.write(escape.RESET)

  def soft_reset(self):
    self.stdout.write(escape.SOFT_RESET)

  # Terminal attributes
  # TODO: Implement some context managers for some of these, perhaps either as a separate method or
  # as a return if no state is provided or perhaps use/make a decorator
  # TODO: maybe shorten some of these method names
  def buffer(self, state: bool):
    self.stdout.write(escape.BUFFER[0 if state else 1])

  def keypad(self, state: bool):
    self.stdout.write(escape.KEYPAD[0 if state else 1])

  def status(self, status: str):
    self.stdout.write(escape.STATUS[0].format(status))

  def paste(self, state: bool):
    self.stdout.write(escape.PASTE[0 if state else 1])

  # Cursor manipulation
  def move_to(self, row: Union[int, None] = None, column: Union[int, None] = None):
    """
    Move the cursor absolutely with respect to the terminal grid.
    A value of None indicates no movement in that direction.
    """
    # TODO: implement horizontal & vertical absolute position codes in
    if column is not None and column < 0:
      raise ValueError("Column cannot be negative (expected >=0, got {})".format(column))
    elif row is not None and row < 0:
      raise ValueError("Row cannot be negative (expected >=0, got {})".format(row))

    if all((column, row)):
      self.stdout.write(escape.MOVE_CURSOR.format(row=row, column=column))
    elif column is not None:
      self.stdout.write(escape.MOVE_COLUMN.format(column=column))
    elif row is not None:
      self.stdout.write(escape.MOVE_ROW.format(row=row))
    # else row is None and column is None:
      # pass

  def move_by(self, x: int = 0, y: int = 0):
    """Move the cursor relatively with respect to it's current position."""
    output = ""
    if y > 0:
      output += escape.CURSOR_DOWN.format(amount=y)
    elif y < 0:
      output += escape.CURSOR_UP.format(amount=-y)

    if x > 0:
      output += escape.CURSOR_RIGHT.format(amount=x)
    elif x < 0:
      output += escape.CURSOR_LEFT.format(amount=-x)
    self.stdout.write(output)

  def save_pos(self):
    """Saves the cursor position into a internal buffer."""
    self.stdout.write(escape.SAVE_CURSOR)

  def restore_pos(self):
    """Restores the cursor position from a internal buffer."""
    self.stdout.write(escape.RESTORE_CURSOR)

  def request_pos(self):
    self.stdout.write(escape.REQUEST_CURSOR)

  def get_pos(self):
    raise NotImplementedError
    # TODO: use event system to catch event, will probably have to use async, or we can block the
    # thread and buffer events until we receive REPORT_CURSOR

  # TODO: consider writing get_size which calls like move_to(999, 999) then calls get_pos()
  # TODO: figure out a way to either poll or receive updates for get_size

  # Cursor attributes
  def cursor_visibility(self, state: bool):
    self.stdout.write(escape.CURSOR_VISIBILITY[0 if state else 1])

  def cursor_style(self, style: Union[str, None] = None, blink: bool = False):
    """
    Set the terminal cursor style.
    Style is any of "block", "underline", "bar" or None to reset it.
    """
    styles = {
      "block": 2,
      "underline": 4,
      "bar": 6,
    }

    if style is None:
      self.stdout.write(escape.CURSOR_STYLE[1])
    else:
      self.stdout.write(escape.CURSOR_STYLE[0].format(style=styles[style] - int(blink)))

  def cursor_color(self, color: Union[Color, None] = None):
    if color is None:
      self.stdout.write(escape.CURSOR_COLOR[1])
    else:
      self.stdout.write(escape.CURSOR_COLOR[0].format(
        red=color.red,
        green=color.green,
        blue=color.blue
      ))

  # Line manipulation
  def clear_line(self):
    self.stdout.write(escape.CLEAR_LINE)

  def insert_line(self, row: int):
    self.stdout.write(escape.INSERT_LINE.format(row=row))

  def delete_line(self, row: int):
    self.stdout.write(escape.DELETE_LINE.format(row=row))

  # Scrollfeed manipulation
  def scroll(self, row_delta: int):
    """
    Scrolls the region clamped by set_scroll_region up or down, removing or adding blank lines as
    necessary.
    """
    if row_delta > 0:
      self.stdout.write(escape.SCROLL_UP.format(amount=row_delta))
    elif row_delta < 0:
      self.stdout.write(escape.SCROLL_DOWN.format(amount=-row_delta))

  def scroll_region(self, first: Union[None, int] = None, second: Union[None, int] = None):
    """Restrict the vertical region that scroll, insert_line and delete_line operate on."""
    if not all((first, second)):
      # Reset the scroll region first, especially if we are going to only reset one of the bounds
      # to it's natural position
      self.stdout.write(escape.SCROLL_REGION[1])

    if any((first, second)):
      self.stdout.write(escape.SCROLL_REGION[0].format(first=first or "", second=second or ""))

  # Text Attributes
  # TODO: maybe turn these into properties with getters & setters
  # TODO: store local state
  def bold(self, state: bool):
    self.stdout.write(escape.BOLD[0 if state else 1])

  def dim(self, state: bool):
    self.stdout.write(escape.DIM[0 if state else 1])

  def reverse(self, state: bool):
    self.stdout.write(escape.REVERSE[0 if state else 1])

  def underline(self, state: bool):
    self.stdout.write(escape.UNDERLINE[0 if state else 1])

  def italic(self, state: bool):
    self.stdout.write(escape.ITALIC[0 if state else 1])

  def conceal(self, state: bool):
    self.stdout.write(escape.CONCEAL[0 if state else 1])

  def blink(self, state: bool):
    self.stdout.write(escape.BLINK[0 if state else 1])

  def strike(self, state: bool):
    self.stdout.write(escape.STRIKE[0 if state else 1])

  def charset(self, state: bool):
    self.stdout.write(escape.CHARSET[0 if state else 1])

  def hyperlink(self, state: bool):
    self.stdout.write(escape.HYPERLINK[0 if state else 1])

  def reset_style(self):
    self.stdout.write(escape.RESET_STYLE)

  # Color
  # NOTE: we can print the 256 color sequence, then the truecolor one, and terminals which only
  #       recognise the 256 one will ignore the truecolor one
  def fg(self, color: Union[Color, int, None] = None):
    if color is None:
      self.stdout.write(escape.RESET_FGCOLOR)

    elif type(color) is int:
      if self.colors >= 256:
        self.stdout.write(escape.FGCOLOR_256.format(color=color))
      elif self.colors >= 16:
        if color >= 8:
          # 16 color code only takes in digits from 0-7
          self.stdout.write(escape.FGCOLOR_16.format(color=color - 8))
        else:
          self.stdout.write(escape.FGCOLOR_8.format(color=color))
      elif self.colors >= 8:
        self.stdout.write(escape.FGCOLOR_8.format(color=color))

    # truecolor
    else:
      # NOTE: this list operation may be expensive, constant such that self.colors doesn't change,
      #       shared between the self.bg call. consider caching the result of this on the instance
      #       level or any time self.colors is changed. also consider implementing this along side
      #       with the local map for COLOR_PAIR described below
      # NOTE: if we print the standard sequence, then the truecolor one, we retain backwards
      #       compatibility
      _, closest_id = color.closest_color(
        [c[0] for c in escape.COLORS]
      )
      self.fg(closest_id)
      self.stdout.write(escape.FGCOLOR_TRUE.format(
        red=color.red,
        green=color.green,
        blue=color.blue
      ))

  def bg(self, color: Union[Color, int, None]):
    if color is None:
      self.stdout.write(escape.RESET_BGCOLOR)

    elif type(color) is int:
      if self.colors >= 256:
        self.stdout.write(escape.BGCOLOR_256.format(color=color))
      elif self.colors >= 16:
        if color >= 8:
          # 16 color code only takes in digits from 0-7
          self.stdout.write(escape.BGCOLOR_16.format(color=color - 8))
        else:
          self.stdout.write(escape.BGCOLOR_8.format(color=color))
      elif self.colors >= 8:
        self.stdout.write(escape.BGCOLOR_8.format(color=color))

    # truecolor
    else:
      _, closest_id = color.closest_color(
        [c[0] for c in escape.COLORS]
      )
      self.bg(closest_id)
      self.stdout.write(escape.BGCOLOR_TRUE.format(
        red=color.red,
        green=color.green,
        blue=color.blue
      ))

  # TODO: consider implementing COLOR_PAIR and a local per-instance mutable ID_MAP

  # Mouse modes
  def mouse(self, click: bool = False, drag: bool = False, move: bool = False):
    self.stdout.write(escape.RESET_MOUSE)
    if click:
      self.stdout.write(escape.CLICK_MOUSE)
    if drag:
      self.stdout.write(escape.DRAG_MOUSE)
    if move:
      self.stdout.write(escape.MOVE_MOUSE)

  # Input handling
  # for stdin attached to a tty, we can poll characters faster than we can process it, so we may
  # be able to peek the buffer and sleep for an amount of time to see if anything has updated.
  # the tty is almost guaranteed to send multi character sequences complete in a single flush,
  # which means that we won't have to process it character by character, and we can immediately
  # parse it into tokens.
  # the simplest way to do this is to peek the internal buffer for content, which will block the
  # thread if there is no data, or will dump the all of the buffer contents. because of the above,
  # we can use this as a source of getting those "packets" of characters
  def readb(self, size: int = -1) -> bytes:
    contents = self.stdin.buffer.peek()  # block the thread until there is at least 1 character
    if size > len(contents) or size <= 0:
      return self.stdin.buffer.read(len(contents))
    return self.stdin.buffer.read(size)

  def read(self, size: int = -1) -> str:
    return self.readb(size).decode(self.stdin.encoding)

  def flush(self, *args, **kwargs):
    self.stdout.flush(*args, **kwargs)

  def parse_keys(self, raw: str) -> List[Key]:
    out = []
    keys = sorted(escape.KEYS, key=len)
    while len(raw) > 0:
      for key in keys:
        if raw.startswith(key):
          out += key

  def collect_events(self):
    raise NotImplementedError

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