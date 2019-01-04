from collections import namedtuple
import functools
import importlib
import os
import sys

import parse
import pkg_resources
import psutil

Coord = namedtuple("Coord", ("row", "column"))
Color = namedtuple("Color", ("red", "green", "blue"))
Feature = namedtuple("Feature", ("enable", "disable"))
Key = namedtuple(
  "Key",
  (
    "stock",
    "shift",
    "ctrl",
    "ctrlshift",
    "meta",
    "metashift",
    "metactrl",
    "metactrlshift"
  )
)

class Term:
  def __init__(self, name=None, process_tree=True, stdin=sys.stdin, stdout=sys.stdout):
    if name is None:
      name = detect_term(process_tree)

    self.name = name
    self.capabilities = get_capabilities(name)
    self.stdin = stdin
    self.stdout = stdout

  def __enter__(self):
    # Set raw mode
    pass

  def __exit__(self, ex_type, ex_value, ex_traceback):
    # Unset raw mode and stop listening to stdin
    pass

  def bell(self):
    self.stdout.write(self.capabilities.BELL)

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

def detect_term(process_tree=True):
  # Check the process parent tree for the terminal emulator
  if process_tree:
    try:
      term_list = list_terms()
      term_list.sort(key=len, reverse=True)

      # Loop over the process tree
      process_parent = psutil.Process().parent()
      while process_parent is not None:
        for term in term_list:
          if term in process_parent.name():
            return term
        process_parent = process_parent.parent()
    except psutil.Error:
      pass
  # Proceed to use other means
  return os.environ.get("TERM") or \
    "cygwin" if os.name == "nt" else \
    "xterm"

def get_capabilities(name):
  package_name = __name__.rsplit(".")[0]
  name = name.replace("-", "_") 
  try:
    # Module path is changed for debugging in repl.it, chage it back to ".terms." + name
    return importlib.import_module("terms." + name, package_name)
    # return importlib.import_module(".terms." + name, package_name)
  except ImportError:
    raise TermNotFound(name) from None

def list_terms():
  filelist = pkg_resources.resource_listdir(__name__, "terms")
  return [name.strip(".py").replace("_", "-") for name in filelist if name.endswith(".py")]

class TermNotFound(Exception):
  def __init__(self, name):
    super().__init__("No terminal named '{}'".format(name))
    self.term = name

class NotSupported(Exception):
  pass
  # def __init__(self):
  #   super().__init__()
