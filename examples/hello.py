import os
import sys
sys.path += os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

import termkit as tk
import termkit.term as tkterm
from termkit import Canvas, Cell, Color

tk.tty.set_raw()  # set the tty to raw mode to receive input character by character
term = tkterm.Terminal()  # attaches by default to sys.stdin and sys.stdout

try:
  # set text style to bold + italic + underline and color to cyan
  term.bold(True)
  term.italic(True)
  term.underline(True)
  term.fg(Color(blue=255, green=255))

  term.write("Hello World")  # output text

  term.reset_style()  # reset the style attributes
  term.fg()  # reset color to default

  term.write("\n")  # add a newline at the bottom
  term.move_to(column=0)  # ensure we're at column 0
  term.flush()

  # grid = Canvas(8, 40)
  # grid.fill(Cell("a", fg=Color(red=255), bg=Color(blue=15)))
  # overlay = Canvas(4, 10)
  # overlay.fill(Cell("", fg=Color(blue=255), bg=Color(0,0,1)))
  # (overlay | grid).draw(term)
  # term.reset_style()
  # term.flush()

  while True:
    char = term.read()
    term.write("{}\n".format(repr(char)))
    if char == "q" or char == "\x03":  # q or ctrl-c
      break

finally:
  # clean up
  term.reset_style()
  tk.tty.set_cooked()