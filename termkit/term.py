from collections import namedtuple
import functools
import importlib
import os
import sys

import parse

from . import constants

Vector = namedtuple("Vector", ["x", "y"])
Vector.__doc__ = """"""

class Terminal:
  capabilities = constants  # copy? dict? ignore & direct reference?

  def bell(self):
    self.stdout.write(constants.BELL)

  def clear(self):
    self.stdout.write(self.capabilities.CLEAR)

  def clear_line(self):
    self.stdout.write(self.capabilities.CLEAR_LINE)

  def delete_line(self, row):
    self.stdout.write(self.capabilities.DELETE_LINE.format(row=row))

  def get_position(self):
    # To-do: catch the key press
    raise NotImplementedError
    # self.stdout.write(self.capabilities.REQUEST_CURSOR)

  def insert_line(self, row):
    self.stdout.write(self.capabilities.INSERT_LINE.format(row=row))

  def key_handler(self, func=None, *, keys=None):
    # Decorator function
    # Use an asterisk to lock the left-side args in place
    if func is None:
      # The function was called in the decorator so we need to return a copy of ourself as a wrapper
      # @key_handler(keys=[...]) or @key_handler()
      return functools.partial(key_handler, keys=keys)

    # The function directly pass in the decorator and this handler is acting like the wrapper
    # @key_handler

    # Do logic with keys
    # event_array.append(func)
    return func

  def move(self, position, relative=False):
    if relative:
      self.move_by(position)
    else:
      self.move_to(position)

  def move_by(self, position):
    output = ""
    if position.row > 0:
      output += self.capabilities.CURSOR_DOWN.format(amount=position.row)
    elif position.row < 0:
      output += self.capabilities.CURSOR_UP.format(amount=position.row * -1)
    if position.column > 0:
      output += self.capabilities.CURSOR_RIGHT.format(amount=position.column)
    elif position.column < 0:
      output += self.capabilities.CURSOR_LEFT.format(amount=position.column * -1)
    self.stdout.write(output)

  def move_to(self, position):
    capability = self.capabilities.MOVE_CURSOR
    if position.row < 0:
      raise ValueError("Value 'row' is negative")
    elif position.column < 0:
      raise ValueError("Value 'column' is negative")
    self.stdout.write(capability.format(**position._asdict()))

  def reset(self):
    self.stdout.write(self.capabilities.RESET)

  def restore_position(self):
    self.stdout.write(self.capabilities.RESTORE_CURSOR)

  def save_position(self):
    self.stdout.write(self.capabilities.SAVE_CURSOR)

  def scroll(self, row_delta):
    if row_delta > 0:
      self.stdout.write(self.capabilities.SCROLL_UP.format(amount=row_delta))
    elif row_delta < 0:
      self.stdout.write(self.capabilities.SCROLL_DOWN.format(amount=row_delta * -1))

  def set_alternate_buffer(self, state):
    self.stdout.write(self.capabilities.ALTERNATE_BUFFER[0 if state else 1])

  def set_alternate_charset(self, state):
    self.stdout.write(self.capabilities.ALTERNATE_CHARSET[0 if state else 1])

  def set_cursor_style(self, style):
    # To-do: figure out what the styles map to again
    raise NotImplementedError

  def set_cursor_color(self, color=None):
    if color is None:
      self.stdout.write(self.capabilities.RESET_CURSOR_COLOR)
    else:
      self.stdout.write(self.capabilities.SET_CURSOR_COLOR.format(**color._asdict()))

  def set_keypad(self, state):
    self.stdout.write(self.capabilities.KEYPAD[0 if state else 1])

  def set_paste(self, state):
    self.stdout.write(self.capabilities.PASTE[0 if state else 1])

  def set_scroll_region(self, first=None, second=None):
    if first is None or second is None:
      # Reset the scroll region
      self.stdout.write(self.capabilities.SCROLL_REGION[1])
    else:
      self.stdout.write(self.capabilities.SCROLL_REGION[0].format(first=first, second=second))

  def set_status(self, status):
    self.stdout.write(self.capabilities.STATUS[0] + status + self.capabilities.STATUS[1])

  def set_visibility(self, state):
    self.stdout.write(self.capabilities.CURSOR_VISIBILITY[0 if state else 1])

  def translate_charset(self, character):
    # To-do: do a reverse lookup this implementation is wrong
    raise NotImplementedError
    # return self.capabilities.ALTERNATE_CHARSET.get(character) or character
