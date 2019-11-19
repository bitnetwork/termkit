import os
import sys
sys.path += os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

import termkit as tk
import termkit.term as tkterm

tk.tty.set_raw()

term = tkterm.Terminal()
term.set_bold(True)
term.set_underline(True)
term.write("Hello World")

# clean up
term.reset_style()
tk.tty.set_cooked()