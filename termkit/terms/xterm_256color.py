"""Constant terminal module for xterm-256color"""

# Consider using namedtuple for existing tuples
# ex: Feature = namedtuple("Feature", ("enter", "exit"))
#              or with better wording ("enable", "disable"))
# or: Key = namedtuple("Key", ("stock", "shift", "ctrl", "ctrl-shift", "meta", "meta-shift", "meta-ctrl", "meta-ctrl-shift"))
# and for COLORMAP: Color = namedtuple("Color", ("red", "green", "blue"))

DESCRIPTION = "X11 terminal emulator with 256 colors"

COLUMNS = 80
LINES = 24
UNICODE = False

BELL = "\b"
CLEAR = "\x1b[H\x1b[2J"
CLEAR_LINE = "\x1b[G\x1b[2K"
INSERT_LINE = "\x1b[{row}L"
DELETE_LINE = "\x1b[{row}M"
RESET = "\x1bc\x1b[!p\x1b[?3;4l\x1b[4l\x1b>\x1b[m\x1b]104\x1b\\\x1b[1 q\x1b]112"
# (enter_feature, exit_feature)
ALTERNATE_BUFFER = ("\x1b[?1049h", "\x1b[?1049l")
KEYPAD = ("\x1b[?1h\x1b=", "\x1b[?1l\x1b>")
STATUS = ("\x1b]0;", "\u0007")
ALTERNATE_CHARSET = ("\x1b(0", "\x1b(B")
PASTE = ("\x1b[?1049h", "\x1b[?1049l")
KEY_PASTE = ("\x1b[200~", "\x1b[201~")
# (set_feature, reset_feature)
SCROLL_REGION = ("\x1b[{first};{second}r", "\x1b[r")
ALTERNATE_CHARSET = {
  "j": u"\u2518",
  "k": u"\u2510",
  "l": u"\u250c",
  "m": u"\u2514",
  "n": u"\u253c",
  "q": u"\u2500",
  "t": u"\u251c",
  "u": u"\u2524",
  "v": u"\u2534",
  "w": u"\u252c",
  "x": u"\u2502"
}

# Transforming these capabilities into tuples may confuse some
MOVE_CURSOR = "\x1b[{row};{column}H"
MOVE_COLUMN = "\x1b[{column}G"
MOVE_ROW = "\x1b[{row}d"
CURSOR_UP = "\x1b[{amount}A"
CURSOR_DOWN = "\x1b[{amount}B"
CURSOR_RIGHT = "\x1b[{amount}C"
CURSOR_LEFT = "\x1b[{amount}D"
SCROLL_UP = "\x1b[{amount}S"
SCROLL_DOWN = "\x1b[{amount}T"
SAVE_CURSOR = "\x1b7"
RESTORE_CURSOR = "\x1b8"
REQUEST_CURSOR = "\x1b[6n"
REPORT_CURSOR = "\x1b[{row};{column}R"

CURSOR_VISIBILITY = ("\x1b[?25h", "\x1b[?25l")
CURSOR_STYLE = "\x1b[{style} q"
CURSOR_COLOR = ("\x1b]12;#{red:x}{green:x}{blue:x}\x07", "\x1b]112")

# (enter_feature, exit_feature)
BOLD = ("\x1b[1m", "\x1b[22m")
DIM = ("\x1b[2m", "\x1b[22m")
REVERSE = ("\x1b[7m", "\x1b[27m")
UNDERLINE = ("\x1b[4m", "\x1b[24m")
ITALIC = ("\x1b[3m", "\x1b[23m")
CONCEAL = ("\x1b[8m", "\x1b[28m")
BLINK = ("\x1b[5m", "\x1b[25m")
STRIKETHROUGH = ("\x1b[9m", "\x1b[29m")
RESET_STYLE = "\x1b(B\x1b[m"

COLORS = 256
TRUECOLOR = True
# (reset_color, 8_color, 16_color, 256_color, truecolor)
# Note that 16_color takes the id starting at 0 unlike 8_color (subtract 8 from id)
SET_FOREGROUND = (
  "\x1b[39m",
  "\x1b[3{color}m",
  "\x1b[9{color}m",
  "\x1b[38;5;{color}m",
  "\x1b[38;2;{red};{blue};{green}m"
)
SET_BACKGROUND = (
  "\x1b[49m",
  "\x1b[4{color}m",
  "\x1b[10{color}m",
  "\x1b[48;5;{color}m",
  "\x1b[48;2;{red};{blue};{green}m"
)
COLOR_PAIR = ("\x1b]4;{color};rgb:{red:X}/{green:X}/{blue:X}\x1b\\", "\x1b]104\x1b\\")
# number = 16 + 36 * r + 6 * g + b
# https://stackoverflow.com/questions/27159322/rgb-values-of-the-colors-in-the-ansi-extended-colors-index-17-255
COLORMAP = (
  # (red, green, blue)
  (0, 0, 0), # 0 black
  (128, 0, 0), # 1 maroon
  (0, 128, 0), # 2 green
  (128, 128, 0), # 3 olive
  (0, 0, 128), # 4 navy
  (128, 0, 128), # 5 purple
  (0, 128, 128), # 6 teal
  (192, 192, 192), # 7 silver
  (128, 128, 128), # 8 grey
  (255, 0, 0), # 9 red
  (0, 255, 0), # 10 lime
  (255, 255, 0), # 11 yellow
  (0, 0, 255), # 12 blue
  (255, 0, 255), # 13 fuchsia
  (0, 255, 255), # 14 aqua
  (255, 255, 255), # 15 white
  (0, 0, 0), # 16 grey0
  (0, 0, 95), # 17 navyblue
  (0, 0, 135), # 18 darkblue
  (0, 0, 175), # 19 blue3
  (0, 0, 215), # 20 blue3
  (0, 0, 255), # 21 blue1
  (0, 95, 0), # 22 darkgreen
  (0, 95, 95), # 23 deepskyblue4
  (0, 95, 135), # 24 deepskyblue4
  (0, 95, 175), # 25 deepskyblue4
  (0, 95, 215), # 26 dodgerblue3
  (0, 95, 255), # 27 dodgerblue2
  (0, 135, 0), # 28 green4
  (0, 135, 95), # 29 springgreen4
  (0, 135, 135), # 30 turquoise4
  (0, 135, 175), # 31 deepskyblue3
  (0, 135, 215), # 32 deepskyblue3
  (0, 135, 255), # 33 dodgerblue1
  (0, 175, 0), # 34 green3
  (0, 175, 95), # 35 springgreen3
  (0, 175, 135), # 36 darkcyan
  (0, 175, 175), # 37 lightseagreen
  (0, 175, 215), # 38 deepskyblue2
  (0, 175, 255), # 39 deepskyblue1
  (0, 215, 0), # 40 green3
  (0, 215, 95), # 41 springgreen3
  (0, 215, 135), # 42 springgreen2
  (0, 215, 175), # 43 cyan3
  (0, 215, 215), # 44 darkturquoise
  (0, 215, 255), # 45 turquoise2
  (0, 255, 0), # 46 green1
  (0, 255, 95), # 47 springgreen2
  (0, 255, 135), # 48 springgreen1
  (0, 255, 175), # 49 mediumspringgreen
  (0, 255, 215), # 50 cyan2
  (0, 255, 255), # 51 cyan1
  (95, 0, 0), # 52 darkred
  (95, 0, 95), # 53 deeppink4
  (95, 0, 135), # 54 purple4
  (95, 0, 175), # 55 purple4
  (95, 0, 215), # 56 purple3
  (95, 0, 255), # 57 blueviolet
  (95, 95, 0), # 58 orange4
  (95, 95, 95), # 59 grey37
  (95, 95, 135), # 60 mediumpurple4
  (95, 95, 175), # 61 slateblue3
  (95, 95, 215), # 62 slateblue3
  (95, 95, 255), # 63 royalblue1
  (95, 135, 0), # 64 chartreuse4
  (95, 135, 95), # 65 darkseagreen4
  (95, 135, 135), # 66 paleturquoise4
  (95, 135, 175), # 67 steelblue
  (95, 135, 215), # 68 steelblue3
  (95, 135, 255), # 69 cornflowerblue
  (95, 175, 0), # 70 chartreuse3
  (95, 175, 95), # 71 darkseagreen4
  (95, 175, 135), # 72 cadetblue
  (95, 175, 175), # 73 cadetblue
  (95, 175, 215), # 74 skyblue3
  (95, 175, 255), # 75 steelblue1
  (95, 215, 0), # 76 chartreuse3
  (95, 215, 95), # 77 palegreen3
  (95, 215, 135), # 78 seagreen3
  (95, 215, 175), # 79 aquamarine3
  (95, 215, 215), # 80 mediumturquoise
  (95, 215, 255), # 81 steelblue1
  (95, 255, 0), # 82 chartreuse2
  (95, 255, 95), # 83 seagreen2
  (95, 255, 135), # 84 seagreen1
  (95, 255, 175), # 85 seagreen1
  (95, 255, 215), # 86 aquamarine1
  (95, 255, 255), # 87 darkslategray2
  (135, 0, 0), # 88 darkred
  (135, 0, 95), # 89 deeppink4
  (135, 0, 135), # 90 darkmagenta
  (135, 0, 175), # 91 darkmagenta
  (135, 0, 215), # 92 darkviolet
  (135, 0, 255), # 93 purple
  (135, 95, 0), # 94 orange4
  (135, 95, 95), # 95 lightpink4
  (135, 95, 135), # 96 plum4
  (135, 95, 175), # 97 mediumpurple3
  (135, 95, 215), # 98 mediumpurple3
  (135, 95, 255), # 99 slateblue1
  (135, 135, 0), # 100 yellow4
  (135, 135, 95), # 101 wheat4
  (135, 135, 135), # 102 grey53
  (135, 135, 175), # 103 lightslategrey
  (135, 135, 215), # 104 mediumpurple
  (135, 135, 255), # 105 lightslateblue
  (135, 175, 0), # 106 yellow4
  (135, 175, 95), # 107 darkolivegreen3
  (135, 175, 135), # 108 darkseagreen
  (135, 175, 175), # 109 lightskyblue3
  (135, 175, 215), # 110 lightskyblue3
  (135, 175, 255), # 111 skyblue2
  (135, 215, 0), # 112 chartreuse2
  (135, 215, 95), # 113 darkolivegreen3
  (135, 215, 135), # 114 palegreen3
  (135, 215, 175), # 115 darkseagreen3
  (135, 215, 215), # 116 darkslategray3
  (135, 215, 255), # 117 skyblue1
  (135, 255, 0), # 118 chartreuse1
  (135, 255, 95), # 119 lightgreen
  (135, 255, 135), # 120 lightgreen
  (135, 255, 175), # 121 palegreen1
  (135, 255, 215), # 122 aquamarine1
  (135, 255, 255), # 123 darkslategray1
  (175, 0, 0), # 124 red3
  (175, 0, 95), # 125 deeppink4
  (175, 0, 135), # 126 mediumvioletred
  (175, 0, 175), # 127 magenta3
  (175, 0, 215), # 128 darkviolet
  (175, 0, 255), # 129 purple
  (175, 95, 0), # 130 darkorange3
  (175, 95, 95), # 131 indianred
  (175, 95, 135), # 132 hotpink3
  (175, 95, 175), # 133 mediumorchid3
  (175, 95, 215), # 134 mediumorchid
  (175, 95, 255), # 135 mediumpurple2
  (175, 135, 0), # 136 darkgoldenrod
  (175, 135, 95), # 137 lightsalmon3
  (175, 135, 135), # 138 rosybrown
  (175, 135, 175), # 139 grey63
  (175, 135, 215), # 140 mediumpurple2
  (175, 135, 255), # 141 mediumpurple1
  (175, 175, 0), # 142 gold3
  (175, 175, 95), # 143 darkkhaki
  (175, 175, 135), # 144 navajowhite3
  (175, 175, 175), # 145 grey69
  (175, 175, 215), # 146 lightsteelblue3
  (175, 175, 255), # 147 lightsteelblue
  (175, 215, 0), # 148 yellow3
  (175, 215, 95), # 149 darkolivegreen3
  (175, 215, 135), # 150 darkseagreen3
  (175, 215, 175), # 151 darkseagreen2
  (175, 215, 215), # 152 lightcyan3
  (175, 215, 255), # 153 lightskyblue1
  (175, 255, 0), # 154 greenyellow
  (175, 255, 95), # 155 darkolivegreen2
  (175, 255, 135), # 156 palegreen1
  (175, 255, 175), # 157 darkseagreen2
  (175, 255, 215), # 158 darkseagreen1
  (175, 255, 255), # 159 paleturquoise1
  (215, 0, 0), # 160 red3
  (215, 0, 95), # 161 deeppink3
  (215, 0, 135), # 162 deeppink3
  (215, 0, 175), # 163 magenta3
  (215, 0, 215), # 164 magenta3
  (215, 0, 255), # 165 magenta2
  (215, 95, 0), # 166 darkorange3
  (215, 95, 95), # 167 indianred
  (215, 95, 135), # 168 hotpink3
  (215, 95, 175), # 169 hotpink2
  (215, 95, 215), # 170 orchid
  (215, 95, 255), # 171 mediumorchid1
  (215, 135, 0), # 172 orange3
  (215, 135, 95), # 173 lightsalmon3
  (215, 135, 135), # 174 lightpink3
  (215, 135, 175), # 175 pink3
  (215, 135, 215), # 176 plum3
  (215, 135, 255), # 177 violet
  (215, 175, 0), # 178 gold3
  (215, 175, 95), # 179 lightgoldenrod3
  (215, 175, 135), # 180 tan
  (215, 175, 175), # 181 mistyrose3
  (215, 175, 215), # 182 thistle3
  (215, 175, 255), # 183 plum2
  (215, 215, 0), # 184 yellow3
  (215, 215, 95), # 185 khaki3
  (215, 215, 135), # 186 lightgoldenrod2
  (215, 215, 175), # 187 lightyellow3
  (215, 215, 215), # 188 grey84
  (215, 215, 255), # 189 lightsteelblue1
  (215, 255, 0), # 190 yellow2
  (215, 255, 95), # 191 darkolivegreen1
  (215, 255, 135), # 192 darkolivegreen1
  (215, 255, 175), # 193 darkseagreen1
  (215, 255, 215), # 194 honeydew2
  (215, 255, 255), # 195 lightcyan1
  (255, 0, 0), # 196 red1
  (255, 0, 95), # 197 deeppink2
  (255, 0, 135), # 198 deeppink1
  (255, 0, 175), # 199 deeppink1
  (255, 0, 215), # 200 magenta2
  (255, 0, 255), # 201 magenta1
  (255, 95, 0), # 202 orangered1
  (255, 95, 95), # 203 indianred1
  (255, 95, 135), # 204 indianred1
  (255, 95, 175), # 205 hotpink
  (255, 95, 215), # 206 hotpink
  (255, 95, 255), # 207 mediumorchid1
  (255, 135, 0), # 208 darkorange
  (255, 135, 95), # 209 salmon1
  (255, 135, 135), # 210 lightcoral
  (255, 135, 175), # 211 palevioletred1
  (255, 135, 215), # 212 orchid2
  (255, 135, 255), # 213 orchid1
  (255, 175, 0), # 214 orange1
  (255, 175, 95), # 215 sandybrown
  (255, 175, 135), # 216 lightsalmon1
  (255, 175, 175), # 217 lightpink1
  (255, 175, 215), # 218 pink1
  (255, 175, 255), # 219 plum1
  (255, 215, 0), # 220 gold1
  (255, 215, 95), # 221 lightgoldenrod2
  (255, 215, 135), # 222 lightgoldenrod2
  (255, 215, 175), # 223 navajowhite1
  (255, 215, 215), # 224 mistyrose1
  (255, 215, 255), # 225 thistle1
  (255, 255, 0), # 226 yellow1
  (255, 255, 95), # 227 lightgoldenrod1
  (255, 255, 135), # 228 khaki1
  (255, 255, 175), # 229 wheat1
  (255, 255, 215), # 230 cornsilk1
  (255, 255, 255), # 231 grey100
  (8, 8, 8), # 232 grey3
  (18, 18, 18), # 233 grey7
  (28, 28, 28), # 234 grey11
  (38, 38, 38), # 235 grey15
  (48, 48, 48), # 236 grey19
  (58, 58, 58), # 237 grey23
  (68, 68, 68), # 238 grey27
  (78, 78, 78), # 239 grey30
  (88, 88, 88), # 240 grey35
  (98, 98, 98), # 241 grey39
  (108, 108, 108), # 242 grey42
  (118, 118, 118), # 243 grey46
  (128, 128, 128), # 244 grey50
  (138, 138, 138), # 245 grey54
  (148, 148, 148), # 246 grey58
  (158, 158, 158), # 247 grey62
  (168, 168, 168), # 248 grey66
  (178, 178, 178), # 249 grey70
  (188, 188, 188), # 250 grey74
  (198, 198, 198), # 251 grey78
  (208, 208, 208), # 252 grey82
  (218, 218, 218), # 253 grey85
  (228, 228, 228), # 254 grey89
  (238, 238, 238) # 255 grey93
)

# (click_mouse, drag_mouse, move_mouse, exit_mouse)
MOUSE = (
  "\x1b[?1000;1006h",
  "\x1b[?1002;1006h",
  "\x1b[?1003;1006h",
  "\x1b[?1000;1002;1003;1006l"
)
# (pressed, released)
KEY_MOUSE = (
  "\x1b[<{button};{row};{columns}m",
  "\x1b[<{button};{row};{columns}M"
)

# (no mod, shift, ctrl, ctrl-shift, meta, meta-shift, meta-ctrl, meta-ctrl-shift)
# nested tuple indicates mutiple keycodes
KEY_UP = (
  ("\x1b[A", "\x1bOA"),
  "\x1b[1;2A",
  "\x1b[1;5A",
  None,
  None,
  None,
  None,
  None
)
KEY_DOWN = (
  ("\x1b[B", "\x1bOB"),
  "\x1b[1;2B",
  "\x1b[1;5B",
  None,
  None,
  None,
  None,
  None
)
KEY_RIGHT = (
  ("\x1b[C", "\x1bOC"),
  "\x1b[1;2C",
  "\x1b[1;5C",
  None,
  None,
  None,
  None,
  None
)
KEY_LEFT = (
  ("\x1b[D", "\x1bOD"),
  "\x1b[1;2D",
  "\x1b[1;5D",
  None,
  None,
  None,
  None,
  None
)
KEY_RETURN = (
  "\r",
  None,
  "\n",
  None,
  None,
  None,
  None,
  None
)
KEY_BACKSPACE = (
  "\u007f",
  None,
  "\b",
  None,
  None,
  None,
  None,
  None
)
KEY_DELETE = (
  "\x1b[3~",
  None,
  "\x1b[3;5~",
  None,
  None,
  None,
  None,
  None
)
KEY_TAB = (
  "\t",
  "\x1b[Z",
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_ESCAPE = (
  "\x1b",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_INSERT = (
  "\x1b[2~",
  None,
  "\x1b[2;5~",
  None,
  None,
  None,
  None,
  None
)
KEY_HOME = (
  ("\x1b[H", "\x1bOH"),
  None,
  "\x1b[1;5H",
  None,
  None,
  None,
  None,
  None
)
KEY_END = (
  ("\x1b[F", "\x1bOF"),
  None,
  "\x1b[1;5F",
  None,
  None,
  None,
  None,
  None
)
KEY_PAGE_LAST = (
  "\x1b[5~",
  None,
  "\x1b[5;5~",
  None,
  None,
  None,
  None,
  None
)
KEY_PAGE_NEXT = (
  "\x1b[6~",
  None,
  "\x1b[6;5~",
  None,
  None,
  None,
  None,
  None
)
KEY_F1 = (
  "\x1bOP",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F2 = (
  "\x1bOQ",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F3 = (
  "\x1bOR",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F4 = (
  "\x1bOS",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F5 = (
  "\x1b[15~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F6 = (
  "\x1b[17~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F7 = (
  "\x1b[18~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F8 = (
  "\x1b[19~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F9 = (
  "\x1b[20~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F10 = (
  "\x1b[21~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F11 = (
  "\x1b[23~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)
KEY_F12 = (
  "\x1b[24~",
  None,
  None,
  None,
  None,
  None,
  None,
  None
)