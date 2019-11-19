"""
An enhanced cross platform tty module which properly implements raw,
rare (cbreak) and cooked modes, and some other helpers relating to the tty.
Unlike python's builtin tty module, this module properly sets raw and has
compatibility for the Windows Console.
"""

import os
import sys

from collections import namedtuple
from io import UnsupportedOperation

# Additional platform specific modules included elsewhere:
# import termios
# from termkit import wincon

__all__ = ["set_cooked", "set_rare", "set_raw"]

# termios specific flags
IFLAG = 0  # Input flags
OFLAG = 1  # Output flags
CFLAG = 2  # Control flags
LFLAG = 3  # Local flags
ISPEED = 4  # Input speed
OSPEED = 5  # Input speed
CC = 6  # Special characters

def set_cooked(fdin: int = None, fdout: int = None):
  """
  Sets the tty attached to the file descriptor into cooked mode:
  The terminal performs input & output processing, sends input on a line by 
  line basis, translates keys into program signals, and echos user input.
  """
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fdin)

    # Enable ctrl-c
    mode[IFLAG] |= termios.BRKINT
    # Disable CR translation, disable stripping 8th bit (unicode), disable parity
    mode[IFLAG] &= ~(termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)

    # Enable output processing
    mode[OFLAG] |= termios.OPOST

    # Disable parity
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)
    # Set character size to 8 bits (unicode)
    mode[CFLAG] |= termios.CS8

    # Enable echo, enable canonical (line) mode, enable input processing, enable signals
    mode[LFLAG] |= termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG

    termios.tcsetattr(fdin, termios.TCSANOW, mode)
  
  elif os.name == "nt":
    from . import wincon
    mode_in = wincon.get_console_mode(fdin)
    mode_out = wincon.get_console_mode(fdout)

    # Enable VT special input keys, enable signals, enable line mode
    mode_in |= wincon.VIRTUAL_TERMINAL_INPUT | wincon.PROCESSED_INPUT | wincon.LINE_INPUT
    # Enable echo, enable edit mode
    mode_in |= wincon.ECHO_INPUT | wincon.QUICK_EDIT_MODE

    # Enable core output processing, enable VT output sequences
    mode_out |= wincon.PROCESSED_OUTPUT | wincon.VIRTUAL_TERMINAL_PROCESSING
    # Enable automatic newline on flush
    mode_out &= ~wincon.DISABLE_NEWLINE_AUTO_RETURN

    wincon.set_console_mode(fdin, mode_in)
    wincon.set_console_mode(fdout, mode_out)

  else:
    raise UnsupportedOperation("cooked_mode")

def set_rare(fdin: int = None, fdout: int = None):
  """
  Sets the tty attached to the file descriptor into rare (cbreak) mode:
  The terminal performs input and output processing, sends input on a character
  by character basis, and translates keys into program signals.
  """
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fdin)

    # Enable ctrl-c
    mode[IFLAG] |= termios.BRKINT
    # Disable CR translation, disable stripping 8th bit (unicode), disable parity
    mode[IFLAG] &= ~(termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)

    # Enable output processing
    mode[OFLAG] |= termios.OPOST

    # Disable parity
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)
    # Set character size to 8 bits (unicode)
    mode[CFLAG] |= termios.CS8

    # Disable echo, disable canonical mode (line mode)
    mode[LFLAG] &= ~(termios.ECHO | termios.ICANON)
    # Enable input processing, enable signals
    mode[LFLAG] |= termios.IEXTEN | termios.ISIG

    termios.tcsetattr(fdin, termios.TCSANOW, mode)
  elif os.name == "nt":
    from . import wincon
    mode_in = wincon.get_console_mode(fdin)
    mode_out = wincon.get_console_mode(fdout)

    # Enable VT special input keys, enable signals
    mode_in |= wincon.VIRTUAL_TERMINAL_INPUT | wincon.PROCESSED_INPUT
    # Disable line mode, disable echo, disable edit mode
    mode_in &= ~(wincon.LINE_INPUT | wincon.ECHO_INPUT | wincon.QUICK_EDIT_MODE)
    
    # Enable core output processing, enable VT output sequences
    mode_out |= wincon.PROCESSED_OUTPUT | wincon.VIRTUAL_TERMINAL_PROCESSING
    # Disable automatic newline on flush
    mode_out |= wincon.DISABLE_NEWLINE_AUTO_RETURN

    wincon.set_console_mode(fdin, mode_in)
    wincon.set_console_mode(fdout, mode_out)
  else:
    raise UnsupportedOperation("raw_mode")

def set_raw(fdin: int = None, fdout: int = None):
  """
  Sets the tty attached to the file descriptor into raw mode:
  The terminal performs no input or output processing, and sends input on a
  character by character basis.
  """
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fdin)

    # Disable ctrl-c, disable CR translation, disable stripping 8th bit (unicode), disable parity
    mode[IFLAG] &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)

    # Disable output processing
    mode[OFLAG] &= ~termios.OPOST

    # Disable parity
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)
    # Set character size to 8 bits (unicode)
    mode[CFLAG] |= termios.CS8

    # Disable echo, disable canonical mode (line mode), disable input processing, disable signals
    mode[LFLAG] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    termios.tcsetattr(fdin, termios.TCSANOW, mode)
  elif os.name == "nt":
    from . import wincon
    mode_in = wincon.get_console_mode(fdin)
    mode_out = wincon.get_console_mode(fdout)

    # Enable VT special input keys
    mode_in |= wincon.VIRTUAL_TERMINAL_INPUT
    # Disable signals, disable line mode, disable echo
    mode_in &= ~(wincon.PROCESSED_INPUT | wincon.LINE_INPUT | wincon.ECHO_INPUT)
    # Disable edit mode
    mode_in &= ~wincon.QUICK_EDIT_MODE
    
    # Enable core output processing, enable VT output sequences
    mode_out |= wincon.PROCESSED_OUTPUT | wincon.VIRTUAL_TERMINAL_PROCESSING
    # Disable automatic newline on flush
    mode_out |= wincon.DISABLE_NEWLINE_AUTO_RETURN

    wincon.set_console_mode(fdin, mode_in)
    wincon.set_console_mode(fdout, mode_out)
  else:
    raise UnsupportedOperation("raw_mode")

def get_term_size(fdin: int = None, fdout: int = None):
  if fdin is None and fdout is None:
    fdin = sys.stdin.fileno()
    fdout = sys.stdout.fileno()

  # raises OSError
  return os.get_terminal_size(fdin if fdin is not None else fdout)