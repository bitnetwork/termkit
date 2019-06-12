"""
An enhanced cross platform tty module which properly implements raw & cooked mode and offers a class
to encapsulate a buffer within the methods.
"""

import io
import os
import sys

from collections import namedtuple

# Additional platform specific modules included elsewhere:
# import termios
# import winios

class TTY(namedtuple("TTY", ["stdin", "stdout"])):
  __slots__ = ()

  def raw_mode(self):
    return raw_mode(self.stdin.fileno(), self.stdout.fileno())

  def cooked_mode(self):
    return cooked_mode(self.stdin.fileno(), self.stdout.fileno())
  

if os.name == "posix":
  IFLAG = 0  # Input flags
  OFLAG = 1  # Output flags
  CFLAG = 2  # Control flags
  LFLAG = 3  # Local flags
  ISPEED = 4  # Input speed
  OSPEED = 5  # Input speed
  CC = 6  # Special characters

def raw_mode(fdin=None, fdout=None):
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fdin)

    # Disable ctrl-c, disable CR translation, disable stripping 8th bit (unicode)
    mode[IFLAG] &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
    # Disable output processing
    mode[OFLAG] &= ~termios.OPOST
    # Set character size to 8 bits (unicode), disable parity checking (error checking)
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)
    mode[CFLAG] |= termios.CS8
    # Disable echo, disable canonical mode (line mode), disable input processing, disable signals
    mode[LFLAG] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    termios.tcsetattr(fdin, termios.TCSANOW, mode)
  elif os.name == "nt":
    import winios
    mode_in = winios.get_console_mode(fdin)
    mode_out = winios.get_console_mode(fdout)

    # Disable signals, disable line mode, disable echo, disbale edit mode
    mode_in |= winios.VIRTUAL_TERMINAL_INPUT
    mode_in &= ~(winios.PROCESSED_INPUT | winios.LINE_INPUT | winios.ECHO_INPUT | winios.QUICK_EDIT_MODE)
    # Enable core output processing, enable vt output sequences, disable automatic newline on flush
    mode_out |= winios.PROCESSED_OUTPUT | winios.VIRTUAL_TERMINAL_PROCESSING | winios.NEWLINE_AUTO_RETURN

    winios.set_console_mode(fdin, mode_in)
    winios.set_console_mode(fdout, mode_out)
  else:
    raise UnsupportedOperation("raw_mode")

def cooked_mode(fdin=None, fdout=None):
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fdin)

    # Enable ctrl-c, enable CR translation, disable input parity checking (error checking), disable
    # stripping 8th bit (unicode)
    mode[IFLAG] |= termios.BRKINT | termios.IXON
    mode[IFLAG] &= ~(termios.ICRNL | termios.INPCK | termios.ISTRIP)
    # Enable output processing
    mode[OFLAG] |= termios.OPOST
    # Set character size to 8 bits (unicode), disable output parity checking (error checking)
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)
    mode[CFLAG] |= termios.CS8
    # Enable echo, enable canonical mode (line mode), enable input processing, enable signals
    mode[LFLAG] |= termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG

    termios.tcsetattr(fdin, termios.TCSANOW, mode)
  elif os.name == "nt":
    import winios
    mode_in = winios.get_console_mode(fdin)
    mode_out = winios.get_console_mode(fdout)

    # Disable signals, disable line mode, disable echo, disbale edit mode
    mode_in |= winios.VIRTUAL_TERMINAL_INPUT | winios.PROCESSED_INPUT | winios.LINE_INPUT \
      | winios.ECHO_INPUT | winios.QUICK_EDIT_MODE
    # Enable core output processing, enable vt output sequences, disable automatic newline on flush
    mode_out |= winios.PROCESSED_OUTPUT | winios.VIRTUAL_TERMINAL_PROCESSING
    mode_out &= ~winios.NEWLINE_AUTO_RETURN

    winios.set_console_mode(fdin, mode_in)
    winios.set_console_mode(fdout, mode_out)
  else:
    raise UnsupportedOperation("cooked_mode")

def get_term_name():
  # Check the environment first
  term = os.environ.get("REALTERM") or os.environ.get("TERM")

  if os.name == "nt":
    if term is None:
      # https://en.wikipedia.org/wiki/Windows_10_version_history#Version_1511_(November_Update)
      # Version 1511 (build >= 10586) was the first to have support for ansi escape sequences
      # However it appears that complete support started around build 16257
      version = sys.getwindowsversion()
      if version.major >= 10 and version.build >= 16257:
        return "cygwin-256color"  # Let's just make a new capability with all these nice features
      return "cygwin"
  return term

def get_term_size(fdin=None, fdout=None):
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  try:
    return os.get_terminal_size(fd)
  except OSError:
    return os.terminal_size((None, None))

if __name__ == "__main__":
  try:
    raw_mode(sys.stdin.fileno())
    sys.stdout.write("Now in raw mode, listening for input, ctrl-c to stop & reset\n\r")
    while True:
      text = sys.stdin.read(1)
      sys.stdout.write("{} {} {} {}\r\n".format(
        repr(text),
        oct(ord(text)),
        str(ord(text)),
        hex(ord(text))
      ))

      if any(char in text for char in ("\x03", "\x04")):  # ^C or ^D
        break

      if "\x1a" in text:  # ^Z
        # Raise an exception to show terminal is not left in garbage state in case of exception
        raise Exception("Bad thing happened")
  finally:
    sys.stdout.write("Cleaning up and exiting\n\r")
    cooked_mode(sys.stdin.fileno())
