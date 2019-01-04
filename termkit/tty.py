"""
An enhanced cross platform tty module which properly implements raw & cooked mode and offers a class
to encapsulate a buffer within the methods.
"""

import io
import os
import sys

# Additional platform specific modules included elsewhere:
# import ctypes
# from ctypes import wintypes
# import msvcrt
# import termios

class UnsupportedOperation(Exception):
  pass

class TTYBase(io.TextIOWrapper):
  def __del__(self):
    # Do not close the buffer as a failsafe and override TextIOWrapper's method
    pass

  def __enter__(self):
    self.raw_mode()

  def __exit__(self, ex_type, ex_value, ex_traceback):
    self.cooked_mode()

  def raw_mode(self):
    # Read recieves input character by character
    # Do not process system signals (^C, ^Z, ect)
    # Do not echo input
    raise NotImplementedError()

  def cooked_mode(self):
    # Read recieves input as a line seperated by a delimiter
    # Let the shell process signals
    # Echo input
    raise NotImplementedError()

  def get_term_name(self):
    raise NotImplementedError

  def get_term_size(self):
    raise NotImplementedError

class TTYWrapper(TTYBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if not self.isatty():
      # Maybe throw an exception here
      raise UnsupportedOperation("Buffer is not a tty")

  def raw_mode(self):
    raw_mode(self.fileno())

  def cooked_mode(self):
    cooked_mode(self.fileno())

  def get_term_name(self):
    get_term_name()

  def get_term_size(self):
    get_term_size(self.fileno())

def raw_mode(fd=None):
  if fd is None:
    fd = sys.stdin.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fd)

    # Disable ctrl-c, disable CR translation, disable stripping 8th bit (unicode)
    mode[IFLAG] &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)  # Unset
    # Disable output processing
    mode[OFLAG] &= ~termios.OPOST  # Unset
    # Set character size to 8 bits (unicode), disable parity checking (error checking)
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)  # Unset
    mode[CFLAG] |= termios.CS8  # Set
    # Disable echo, disable canonical mode (line mode), disable input processing, disable signals
    mode[LFLAG] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)  # Unset

    termios.tcsetattr(fd, termios.TCSANOW, mode)
  elif os.name == "nt":
    mode = get_console_mode(fd)
    mode |= (PROCESSED_INPUT)  # Set flags
    mode &= ~(LINE_INPUT | ECHO_INPUT | QUICK_EDIT_MODE)  # Unset flags
    set_console_mode(fd, mode)
  else:
    raise UnsupportedOperation("Platform {} not supported".format(repr(os.name)))

def cooked_mode(fd=None):
  if fd is None:
    fd = sys.stdin.fileno()

  if os.name == "posix":
    import termios
    mode = termios.tcgetattr(fd)

    # Enable ctrl-c, enable CR translation, disable input parity checking (error checking), disable
    # stripping 8th bit (unicode)
    mode[IFLAG] |= termios.BRKINT | termios.IXON # Set
    mode[IFLAG] &= ~(termios.ICRNL | termios.INPCK | termios.ISTRIP)  # Unset
    # Enable output processing
    mode[OFLAG] |= termios.OPOST  # Unset
    # Set character size to 8 bits (unicode), disable output parity checking (error checking)
    mode[CFLAG] &= ~(termios.CSIZE | termios.PARENB)  # Unset
    mode[CFLAG] |= termios.CS8  # Set
    # Enable echo, enable canonical mode (line mode), enable input processing, enable signals
    mode[LFLAG] |= termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG  # Unset

    termios.tcsetattr(fd, termios.TCSANOW, mode)
  elif os.name == "nt":
    mode = get_console_mode(fd)
    mode |= LINE_INPUT | ECHO_INPUT | QUICK_EDIT_MODE  # Set flags
    mode &= ~(PROCESSED_INPUT)  # Unset flags
    set_console_mode(fd, mode)
  else:
    raise UnsupportedOperation("Platform {} not supported".format(repr(os.name)))

def get_term_name():
  # Check the environment first
  term = os.environ.get("REALTERM") or os.environ.get("TERM")

  if os.name == "posix":
    return term
  if os.name == "nt":
    if term is not None:
      return term

    # https://en.wikipedia.org/wiki/Windows_10_version_history#Version_1511_(November_Update)
    # Version 1511 (build >= 10586) was the first to have support for ansi escape sequences
    # However it appears that complete support started around build 16257
    version = sys.getwindowsversion()
    if version.major >= 10 and version.build >= 16257:
      return "cygwin-256color"  # Let's just make a new capability with all these nice features
    return "cygwin"

def get_term_size(fd=None):
  try:
    return os.get_terminal_size(fd)
  except OSError:
    return os.terminal_size((None, None))

if os.name == "posix":
  IFLAG = 0  # Input flags
  OFLAG = 1  # Output flags
  CFLAG = 2  # Control flags
  LFLAG = 3  # Local flags
  ISPEED = 4  # Input speed
  OSPEED = 5  # Input speed
  CC = 6  # Special characters
elif os.name == "nt":
  # Input bitmask flags
  PROCESSED_INPUT = 0x1  # System signal processing (^C)
  LINE_INPUT = 0x2  # Raw/line break mode
  ECHO_INPUT = 0x4
  WINDOW_INPUT = 0x8
  MOUSE_INPUT = 0x10
  INSERT_MODE = 0x20
  QUICK_EDIT_MODE = 0x40  # Edit/select mode
  VIRTUAL_TERMINAL_INPUT = 0x200  # Process ansi key sequences (only win 10)

  # Output bitmask flags
  PROCESSED_OUTPUT = 0x1  # Basic processing for BS, tab, bell, CR, LF
  WRAP_AT_EOL_OUTPUT = 0x2  # May be favorable to disable this
  VIRTUAL_TERMINAL_PROCESSING = 0x4  # Required to process ansi sequences (only win 10)
  NEWLINE_AUTO_RETURN = 0x8  # Setting flags disables the feature (only win 10)

  def get_console_mode(fd):
    import ctypes
    from ctypes import wintypes
    import msvcrt

    def zero_check(result, _, args):
      if not result:
        error = ctypes.get_last_error()
        if error:
          raise ctypes.WinError(error)
      return args

    kernel = ctypes.windll.kernel32
    handle = msvcrt.get_osfhandle(fd)
    mode = wintypes.DWORD()  # A empty pointer to be later updated

    kernel.GetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.LPDWORD)
    kernel.GetConsoleMode.errcheck = zero_check    # hConsoleHandle, lpMode
    kernel.GetConsoleMode(handle, ctypes.byref(mode))  # Mode passed by reference and is now updated
    return mode.value

  def set_console_mode(fd, mode):
    import ctypes
    from ctypes import wintypes
    import msvcrt

    def zero_check(result, _, args):
      if not result:
        error = ctypes.get_last_error()
        if error:
          raise ctypes.WinError(error)
      return args

    kernel = ctypes.windll.kernel32
    handle = msvcrt.get_osfhandle(fd)

    kernel.SetConsoleMode.errcheck = zero_check
    kernel.SetConsoleMode(handle, mode)  # No reference required

  def vt_mode(enable=True, fdin=None, fdout=None):
    if fdin is None:
      fdin = sys.stdin.fileno()
    if fdout is None:
      fdout = sys.stdout.fileno()

    input_mode = get_console_mode(fdin)
    output_mode = get_console_mode(fdout)

    if enable:
      input_mode |= VIRTUAL_TERMINAL_INPUT
      output_mode |= VIRTUAL_TERMINAL_PROCESSING | NEWLINE_AUTO_RETURN
    else:
      input_mode &= ~VIRTUAL_TERMINAL_INPUT
      output_mode &= ~(VIRTUAL_TERMINAL_PROCESSING | NEWLINE_AUTO_RETURN)

    set_console_mode(fdin, input_mode)
    set_console_mode(fdout, output_mode)

if __name__ == "__main__":
  try:
    raw_mode()
    sys.stdout.write("Now in raw mode, listening for input, ctrl-c to stop & reset\n\r")
    while True:
      text = sys.stdin.read(1)
      sys.stdout.write("{} found\n\r".format(repr(text)))

      if "\x03" in text:  # Ctrl-c
        break
  finally:
    sys.stdout.write("Cleaning up and exiting\n\r")
    cooked_mode()
    