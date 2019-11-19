import ctypes
import msvcrt
import sys

from ctypes import wintypes

# Input bitmask flags
PROCESSED_INPUT = 0x1  # System signal processing (^C)
LINE_INPUT = 0x2  # Raw/cooked mode
ECHO_INPUT = 0x4
WINDOW_INPUT = 0x8  # Window size changes are written to the stream
MOUSE_INPUT = 0x10  # Enable mouse events via console api
INSERT_MODE = 0x20
QUICK_EDIT_MODE = 0x40  # Edit/select mode
VIRTUAL_TERMINAL_INPUT = 0x200  # Process input virtual terminal key sequences (win 10)

# Output bitmask flags
PROCESSED_OUTPUT = 0x1  # Basic processing for BS, tab, bell, CR, LF
WRAP_AT_EOL_OUTPUT = 0x2  # Line wrapping
VIRTUAL_TERMINAL_PROCESSING = 0x4  # Process output virtual terminal sequences (win 10)
DISABLE_NEWLINE_AUTO_RETURN = 0x8  # Setting flags disables automatic newline on flush (win 10)

def set_console_mode(fd, mode):
  def zero_check(result, _, args):
    if not result:
      error = ctypes.get_last_error()
      if error:
        raise ctypes.WinError(error)
    return args

  kernel = ctypes.windll.kernel32
  handle = msvcrt.get_osfhandle(fd)  # Get file handle

  kernel.GetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.DWORD)
  kernel.SetConsoleMode.errcheck = zero_check
  kernel.SetConsoleMode(handle, mode)

def get_console_mode(fd):
  def zero_check(result, _, args):
    if not result:
      error = ctypes.get_last_error()
      if error:
        raise ctypes.WinError(error)
    return args

  kernel = ctypes.windll.kernel32
  handle = msvcrt.get_osfhandle(fd)  # Get file handle
  mode = wintypes.DWORD()  # Pointer instance

  kernel.GetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.LPDWORD)
  kernel.GetConsoleMode.errcheck = zero_check
  kernel.GetConsoleMode(handle, ctypes.byref(mode))  # Mode passed by reference
  return mode.value

def vt_mode(enable=True, fdin=None, fdout=None):
  if fdin is None:
    fdin = sys.stdin.fileno()
  if fdout is None:
    fdout = sys.stdout.fileno()

  input_mode = get_console_mode(fdin)
  output_mode = get_console_mode(fdout)

  if enable:
    input_mode |= VIRTUAL_TERMINAL_INPUT
    output_mode |= VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN
  else:
    input_mode &= ~VIRTUAL_TERMINAL_INPUT
    output_mode &= ~(VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN)

  set_console_mode(fdin, input_mode)
  set_console_mode(fdout, output_mode)