"""
This module contains terminal escape sequences for most of the common actions. The goal is to
support most of the common terminal emulators, especially xterm and VTE.

Most of the sequences in file may silently fail on unsupported emulators, which means we don't have
to sniff for feature support. In addition the goal is to support a large variety of emulators with
the same escape sequences, so some definitions may be redundant.

Also some support must be known on a per terminal basis and is impractical to be detected (example:
color support, unicode, window size), so it is left for higher up modules to fill in those gaps.
"""

from collections import namedtuple

Feature = namedtuple("Feature", ["set", "reset"])
Feature.__doc__ = """"""
Key = namedtuple("Key", ["key", "value", "shift", "meta", "ctrl"], defaults=(False,) * 3)
Key.__doc__ = """"""

BELL = "\b"
CLEAR = "\x1b[2J\x1b[H"  # Clear the screen then move the cursor to home position (0, 0) 
SOFT_RESET = (
  "\x1b[!p"  # Soft terminal reset
  "\x1b[?3;4l"  # 80 column mode, jump scroll
  "\x1b>"  # Normal keypad
  "\x1b[m"  # Reset all style attributes
  "\x1b(B"  # Set charset #0 as ASCII
  "\x1b)0"  # Set charset #1 as Special Character and Line Drawing
  "\x0f"  # (^O) Switch to charset #0
  "\x1b]104\x1b\\"  # Reset color palate
  "\x1b[1 q"  # Reset cursor style
  "\x1b]112"  # Reset cursor color
)
RESET = (
  "\x1bc"  # Full reset
  "\x1b[3J"  # Clear screen and scrollback buffer
  "\x1b[!p"  # Soft terminal reset
  "\x1b[?3;4l"  # 80 column mode, jump scroll
  "\x1b>"  # Normal keypad
  "\x1b[m"  # Reset all text attributes
  "\x1b(B"  # Set charset #0 as ASCII
  "\x1b)0"  # Set charset #1 as Special Character and Line Drawing
  "\x0f"  # (^O) Switch to charset #0
  "\x1b]104\x1b\\"  # Reset color palate
  "\x1b[1 q"  # Reset cursor style
  "\x1b]112"  # Reset cursor color
)

# Terminal attributes
BUFFER = Feature("\x1b[?1049h", "\x1b[?1049l")
KEYPAD = Feature("\x1b[?1h\x1b=", "\x1b[?1l\x1b>")
STATUS = Feature("\x1b]0;{text}\x1b\\", "")  # There is no way to reset the status line
PASTE = Feature("\x1b[?2004h", "\x1b[?2004l")

# Cursor manipulation
MOVE_CURSOR = "\x1b[{row};{column}H"
MOVE_COLUMN = "\x1b[{column}G"
MOVE_ROW = "\x1b[{row}d"
CURSOR_UP = "\x1b[{amount}A"
CURSOR_DOWN = "\x1b[{amount}B"
CURSOR_RIGHT = "\x1b[{amount}C"
CURSOR_LEFT = "\x1b[{amount}D"
SAVE_CURSOR = "\x1b7"
RESTORE_CURSOR = "\x1b8"
REQUEST_CURSOR = "\x1b[6n"
REPORT_CURSOR = "\x1b[{row};{column}R"

# Cursor attributes
CURSOR_VISIBILITY = Feature("\x1b[?25h", "\x1b[?25l")
CURSOR_STYLE = Feature("\x1b[{style} q", "\x1b[ q")
CURSOR_COLOR = Feature("\x1b]12;rgb:{red:X}/{green:X}/{blue:X}\x1b\\", "\x1b]112\x1b\\")

# Line manipulation
INSERT_LINE = "\x1b[{row}L"
DELETE_LINE = "\x1b[{row}M"
CLEAR_LINE = "\x1b[G\x1b[2K"  # Move the cursor to column 1 then clear the line

# Scrollfeed manipulation
SCROLL_UP = "\x1b[{amount}S"
SCROLL_DOWN = "\x1b[{amount}T"
SCROLL_REGION = Feature("\x1b[{first};{second}r", "\x1b[r")

# Text attributes
# https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda

BOLD = Feature("\x1b[1m", "\x1b[22m")
DIM = Feature("\x1b[2m", "\x1b[22m")
REVERSE = Feature("\x1b[7m", "\x1b[27m")
UNDERLINE = Feature("\x1b[4m", "\x1b[24m")
ITALIC = Feature("\x1b[3m", "\x1b[23m")
CONCEAL = Feature("\x1b[8m", "\x1b[28m")
BLINK = Feature("\x1b[5m", "\x1b[25m")
STRIKE = Feature("\x1b[9m", "\x1b[29m")
CHARSET = Feature("\x1b(0\x0f", "\x1b(B\x0f")
HYPERLINK = Feature("\x1b]8;;{link}\x1b\\", "\x1b]8;;\x1b\\")  # older terminals do not like this
RESET_STYLE = "\x1b(B\x1b[m"
CHARSET_TABLE = (
  ("j", u"\u2518"),
  ("k", u"\u2510"),
  ("l", u"\u250c"),
  ("m", u"\u2514"),
  ("n", u"\u253c"),
  ("q", u"\u2500"),
  ("t", u"\u251c"),
  ("u", u"\u2524"),
  ("v", u"\u2534"),
  ("w", u"\u252c"),
  ("x", u"\u2502"),
)

# Color
# NOTE: 16_color takes the id starting at 0 unlike 8_color (subtract 8 from id)
FGCOLOR_8 = "\x1b[3{color}m"  # color = 0-7
FGCOLOR_16 = "\x1b[9{color}m"  # color = 0-7 (real values of 8-15)
FGCOLOR_256 = "\x1b[38;5;{color}m"  # color = 0-255
FGCOLOR_TRUE = "\x1b[38;2;{red};{blue};{green}m"  # red, blue, green = 0-255
RESET_FGCOLOR = "\x1b[39m"
BGCOLOR_8 = "\x1b[4{color}m"  # color = 0-7
BGCOLOR_16 = "\x1b[10{color}m"  # color = 0-7 (real values 8-15)
BGCOLOR_256 = "\x1b[48;5;{color}m"  # color = 0-255
BGCOLOR_TRUE = "\x1b[48;2;{red};{blue};{green}m"  # red, blue, green = 0-255
RESET_BGCOLOR = "\x1b[49m"
COLOR_PAIR = Feature("\x1b]4;{color};rgb:{red:x}/{green:x}/{blue:x}\x1b\\", "\x1b]104\x1b\\")

# Color map
# id_number = 16 + 36*r + 6*g + b
# https://stackoverflow.com/questions/27159322/rgb-values-of-the-colors-in-the-ansi-extended-colors-index-17-255
COLORS = [
  ((0, 0, 0), "black"),  # 0
  ((128, 0, 0), "maroon"),  # 1
  ((0, 128, 0), "green"),  # 2
  ((128, 128, 0), "olive"),  # 3
  ((0, 0, 128), "navy"),  # 4
  ((128, 0, 128), "purple"),  # 5
  ((0, 128, 128), "teal"),  # 6
  ((192, 192, 192), "silver"),  # 7
  ((128, 128, 128), "grey"),  # 8
  ((255, 0, 0), "red"),  # 9
  ((0, 255, 0), "lime"),  # 10
  ((255, 255, 0), "yellow"),  # 11
  ((0, 0, 255), "blue"),  # 12
  ((255, 0, 255), "fuchsia"),  # 13
  ((0, 255, 255), "aqua"),  # 14
  ((255, 255, 255), "white"),  # 15
  ((0, 0, 0), "grey0"),  # 16
  ((0, 0, 95), "navyblue"),  # 17
  ((0, 0, 135), "darkblue"),  # 18
  ((0, 0, 175), "blue3"),  # 19
  ((0, 0, 215), "blue3"),  # 20
  ((0, 0, 255), "blue1"),  # 21
  ((0, 95, 0), "darkgreen"),  # 22
  ((0, 95, 95), "deepskyblue4"),  # 23
  ((0, 95, 135), "deepskyblue4"),  # 24
  ((0, 95, 175), "deepskyblue4"),  # 25
  ((0, 95, 215), "dodgerblue3"),  # 26
  ((0, 95, 255), "dodgerblue2"),  # 27
  ((0, 135, 0), "green4"),  # 28
  ((0, 135, 95), "springgreen4"),  # 29
  ((0, 135, 135), "turquoise4"),  # 30
  ((0, 135, 175), "deepskyblue3"),  # 31
  ((0, 135, 215), "deepskyblue3"),  # 32
  ((0, 135, 255), "dodgerblue1"),  # 33
  ((0, 175, 0), "green3"),  # 34
  ((0, 175, 95), "springgreen3"),  # 35
  ((0, 175, 135), "darkcyan"),  # 36
  ((0, 175, 175), "lightseagreen"),  # 37
  ((0, 175, 215), "deepskyblue2"),  # 38
  ((0, 175, 255), "deepskyblue1"),  # 39
  ((0, 215, 0), "green3"),  # 40
  ((0, 215, 95), "springgreen3"),  # 41
  ((0, 215, 135), "springgreen2"),  # 42
  ((0, 215, 175), "cyan3"),  # 43
  ((0, 215, 215), "darkturquoise"),  # 44
  ((0, 215, 255), "turquoise2"),  # 45
  ((0, 255, 0), "green1"),  # 46
  ((0, 255, 95), "springgreen2"),  # 47
  ((0, 255, 135), "springgreen1"),  # 48
  ((0, 255, 175), "mediumspringgreen"),  # 49
  ((0, 255, 215), "cyan2"),  # 50
  ((0, 255, 255), "cyan1"),  # 51
  ((95, 0, 0), "darkred"),  # 52
  ((95, 0, 95), "deeppink4"),  # 53
  ((95, 0, 135), "purple4"),  # 54
  ((95, 0, 175), "purple4"),  # 55
  ((95, 0, 215), "purple3"),  # 56
  ((95, 0, 255), "blueviolet"),  # 57
  ((95, 95, 0), "orange4"),  # 58
  ((95, 95, 95), "grey37"),  # 59
  ((95, 95, 135), "mediumpurple4"),  # 60
  ((95, 95, 175), "slateblue3"),  # 61
  ((95, 95, 215), "slateblue3"),  # 62
  ((95, 95, 255), "royalblue1"),  # 63
  ((95, 135, 0), "chartreuse4"),  # 64
  ((95, 135, 95), "darkseagreen4"),  # 65
  ((95, 135, 135), "paleturquoise4"),  # 66
  ((95, 135, 175), "steelblue"),  # 67
  ((95, 135, 215), "steelblue3"),  # 68
  ((95, 135, 255), "cornflowerblue"),  # 69
  ((95, 175, 0), "chartreuse3"),  # 70
  ((95, 175, 95), "darkseagreen4"),  # 71
  ((95, 175, 135), "cadetblue"),  # 72
  ((95, 175, 175), "cadetblue"),  # 73
  ((95, 175, 215), "skyblue3"),  # 74
  ((95, 175, 255), "steelblue1"),  # 75
  ((95, 215, 0), "chartreuse3"),  # 76
  ((95, 215, 95), "palegreen3"),  # 77
  ((95, 215, 135), "seagreen3"),  # 78
  ((95, 215, 175), "aquamarine3"),  # 79
  ((95, 215, 215), "mediumturquoise"),  # 80
  ((95, 215, 255), "steelblue1"),  # 81
  ((95, 255, 0), "chartreuse2"),  # 82
  ((95, 255, 95), "seagreen2"),  # 83
  ((95, 255, 135), "seagreen1"),  # 84
  ((95, 255, 175), "seagreen1"),  # 85
  ((95, 255, 215), "aquamarine1"),  # 86
  ((95, 255, 255), "darkslategray2"),  # 87
  ((135, 0, 0), "darkred"),  # 88
  ((135, 0, 95), "deeppink4"),  # 89
  ((135, 0, 135), "darkmagenta"),  # 90
  ((135, 0, 175), "darkmagenta"),  # 91
  ((135, 0, 215), "darkviolet"),  # 92
  ((135, 0, 255), "purple"),  # 93
  ((135, 95, 0), "orange4"),  # 94
  ((135, 95, 95), "lightpink4"),  # 95
  ((135, 95, 135), "plum4"),  # 96
  ((135, 95, 175), "mediumpurple3"),  # 97
  ((135, 95, 215), "mediumpurple3"),  # 98
  ((135, 95, 255), "slateblue1"),  # 99
  ((135, 135, 0), "yellow4"),  # 100
  ((135, 135, 95), "wheat4"),  # 101
  ((135, 135, 135), "grey53"),  # 102
  ((135, 135, 175), "lightslategrey"),  # 103
  ((135, 135, 215), "mediumpurple"),  # 104
  ((135, 135, 255), "lightslateblue"),  # 105
  ((135, 175, 0), "yellow4"),  # 106
  ((135, 175, 95), "darkolivegreen3"),  # 107
  ((135, 175, 135), "darkseagreen"),  # 108
  ((135, 175, 175), "lightskyblue3"),  # 109
  ((135, 175, 215), "lightskyblue3"),  # 110
  ((135, 175, 255), "skyblue2"),  # 111
  ((135, 215, 0), "chartreuse2"),  # 112
  ((135, 215, 95), "darkolivegreen3"),  # 113
  ((135, 215, 135), "palegreen3"),  # 114
  ((135, 215, 175), "darkseagreen3"),  # 115
  ((135, 215, 215), "darkslategray3"),  # 116
  ((135, 215, 255), "skyblue1"),  # 117
  ((135, 255, 0), "chartreuse1"),  # 118
  ((135, 255, 95), "lightgreen"),  # 119
  ((135, 255, 135), "lightgreen"),  # 120
  ((135, 255, 175), "palegreen1"),  # 121
  ((135, 255, 215), "aquamarine1"),  # 122
  ((135, 255, 255), "darkslategray1"),  # 123
  ((175, 0, 0), "red3"),  # 124
  ((175, 0, 95), "deeppink4"),  # 125
  ((175, 0, 135), "mediumvioletred"),  # 126
  ((175, 0, 175), "magenta3"),  # 127
  ((175, 0, 215), "darkviolet"),  # 128
  ((175, 0, 255), "purple"),  # 129
  ((175, 95, 0), "darkorange3"),  # 130
  ((175, 95, 95), "indianred"),  # 131
  ((175, 95, 135), "hotpink3"),  # 132
  ((175, 95, 175), "mediumorchid3"),  # 133
  ((175, 95, 215), "mediumorchid"),  # 134
  ((175, 95, 255), "mediumpurple2"),  # 135
  ((175, 135, 0), "darkgoldenrod"),  # 136
  ((175, 135, 95), "lightsalmon3"),  # 137
  ((175, 135, 135), "rosybrown"),  # 138
  ((175, 135, 175), "grey63"),  # 139
  ((175, 135, 215), "mediumpurple2"),  # 140
  ((175, 135, 255), "mediumpurple1"),  # 141
  ((175, 175, 0), "gold3"),  # 142
  ((175, 175, 95), "darkkhaki"),  # 143
  ((175, 175, 135), "navajowhite3"),  # 144
  ((175, 175, 175), "grey69"),  # 145
  ((175, 175, 215), "lightsteelblue3"),  # 146
  ((175, 175, 255), "lightsteelblue"),  # 147
  ((175, 215, 0), "yellow3"),  # 148
  ((175, 215, 95), "darkolivegreen3"),  # 149
  ((175, 215, 135), "darkseagreen3"),  # 150
  ((175, 215, 175), "darkseagreen2"),  # 151
  ((175, 215, 215), "lightcyan3"),  # 152
  ((175, 215, 255), "lightskyblue1"),  # 153
  ((175, 255, 0), "greenyellow"),  # 154
  ((175, 255, 95), "darkolivegreen2"),  # 155
  ((175, 255, 135), "palegreen1"),  # 156
  ((175, 255, 175), "darkseagreen2"),  # 157
  ((175, 255, 215), "darkseagreen1"),  # 158
  ((175, 255, 255), "paleturquoise1"),  # 159
  ((215, 0, 0), "red3"),  # 160
  ((215, 0, 95), "deeppink3"),  # 161
  ((215, 0, 135), "deeppink3"),  # 162
  ((215, 0, 175), "magenta3"),  # 163
  ((215, 0, 215), "magenta3"),  # 164
  ((215, 0, 255), "magenta2"),  # 165
  ((215, 95, 0), "darkorange3"),  # 166
  ((215, 95, 95), "indianred"),  # 167
  ((215, 95, 135), "hotpink3"),  # 168
  ((215, 95, 175), "hotpink2"),  # 169
  ((215, 95, 215), "orchid"),  # 170
  ((215, 95, 255), "mediumorchid1"),  # 171
  ((215, 135, 0), "orange3"),  # 172
  ((215, 135, 95), "lightsalmon3"),  # 173
  ((215, 135, 135), "lightpink3"),  # 174
  ((215, 135, 175), "pink3"),  # 175
  ((215, 135, 215), "plum3"),  # 176
  ((215, 135, 255), "violet"),  # 177
  ((215, 175, 0), "gold3"),  # 178
  ((215, 175, 95), "lightgoldenrod3"),  # 179
  ((215, 175, 135), "tan"),  # 180
  ((215, 175, 175), "mistyrose3"),  # 181
  ((215, 175, 215), "thistle3"),  # 182
  ((215, 175, 255), "plum2"),  # 183
  ((215, 215, 0), "yellow3"),  # 184
  ((215, 215, 95), "khaki3"),  # 185
  ((215, 215, 135), "lightgoldenrod2"),  # 186
  ((215, 215, 175), "lightyellow3"),  # 187
  ((215, 215, 215), "grey84"),  # 188
  ((215, 215, 255), "lightsteelblue1"),  # 189
  ((215, 255, 0), "yellow2"),  # 190
  ((215, 255, 95), "darkolivegreen1"),  # 191
  ((215, 255, 135), "darkolivegreen1"),  # 192
  ((215, 255, 175), "darkseagreen1"),  # 193
  ((215, 255, 215), "honeydew2"),  # 194
  ((215, 255, 255), "lightcyan1"),  # 195
  ((255, 0, 0), "red1"),  # 196
  ((255, 0, 95), "deeppink2"),  # 197
  ((255, 0, 135), "deeppink1"),  # 198
  ((255, 0, 175), "deeppink1"),  # 199
  ((255, 0, 215), "magenta2"),  # 200
  ((255, 0, 255), "magenta1"),  # 201
  ((255, 95, 0), "orangered1"),  # 202
  ((255, 95, 95), "indianred1"),  # 203
  ((255, 95, 135), "indianred1"),  # 204
  ((255, 95, 175), "hotpink"),  # 205
  ((255, 95, 215), "hotpink"),  # 206
  ((255, 95, 255), "mediumorchid1"),  # 207
  ((255, 135, 0), "darkorange"),  # 208
  ((255, 135, 95), "salmon1"),  # 209
  ((255, 135, 135), "lightcoral"),  # 210
  ((255, 135, 175), "palevioletred1"),  # 211
  ((255, 135, 215), "orchid2"),  # 212
  ((255, 135, 255), "orchid1"),  # 213
  ((255, 175, 0), "orange1"),  # 214
  ((255, 175, 95), "sandybrown"),  # 215
  ((255, 175, 135), "lightsalmon1"),  # 216
  ((255, 175, 175), "lightpink1"),  # 217
  ((255, 175, 215), "pink1"),  # 218
  ((255, 175, 255), "plum1"),  # 219
  ((255, 215, 0), "gold1"),  # 220
  ((255, 215, 95), "lightgoldenrod2"),  # 221
  ((255, 215, 135), "lightgoldenrod2"),  # 222
  ((255, 215, 175), "navajowhite1"),  # 223
  ((255, 215, 215), "mistyrose1"),  # 224
  ((255, 215, 255), "thistle1"),  # 225
  ((255, 255, 0), "yellow1"),  # 226
  ((255, 255, 95), "lightgoldenrod1"),  # 227
  ((255, 255, 135), "khaki1"),  # 228
  ((255, 255, 175), "wheat1"),  # 229
  ((255, 255, 215), "cornsilk1"),  # 230
  ((255, 255, 255), "grey100"),  # 231
  ((8, 8, 8), "grey3"),  # 232
  ((18, 18, 18), "grey7"),  # 233
  ((28, 28, 28), "grey11"),  # 234
  ((38, 38, 38), "grey15"),  # 235
  ((48, 48, 48), "grey19"),  # 236
  ((58, 58, 58), "grey23"),  # 237
  ((68, 68, 68), "grey27"),  # 238
  ((78, 78, 78), "grey30"),  # 239
  ((88, 88, 88), "grey35"),  # 240
  ((98, 98, 98), "grey39"),  # 241
  ((108, 108, 108), "grey42"),  # 242
  ((118, 118, 118), "grey46"),  # 243
  ((128, 128, 128), "grey50"),  # 244
  ((138, 138, 138), "grey54"),  # 245
  ((148, 148, 148), "grey58"),  # 246
  ((158, 158, 158), "grey62"),  # 247
  ((168, 168, 168), "grey66"),  # 248
  ((178, 178, 178), "grey70"),  # 249
  ((188, 188, 188), "grey74"),  # 250
  ((198, 198, 198), "grey78"),  # 251
  ((208, 208, 208), "grey82"),  # 252
  ((218, 218, 218), "grey85"),  # 253
  ((228, 228, 228), "grey89"),  # 254
  ((238, 238, 238), "grey93"),  # 255
]

CLICK_MOUSE = "\x1b[?1000;1006h"  # sends only click events
DRAG_MOUSE = "\x1b[?1002;1006h"  # sends only click & drag events
MOVE_MOUSE = "\x1b[?1003;1006h"  # sends only mouse move events
RESET_MOUSE = "\x1b[?1000;1002;1003;1006l"

KEY_MOUSE_PRESS = "\x1b[<{button};{row};{columns}m"
KEY_MOUSE_RELEASE = "\x1b[<{button};{row};{columns}M"
KEY_PASTE_BEGIN = "\x1b[200~"
KEY_PASTE_END = "\x1b[201~"

# xterm sends an escape sequence followed by a bitmask of modifiers pressed
# \x1b[...;B... where B is a 1 + a bitmask of (LSB shift, meta, ctrl MSB)
# otherwise if there is a lowercase letter, shift will capitalize it and meta will prepend \x1b to it
# maybe implement SET_FULL later: https://sw.kovidgoyal.net/kitty/protocol-extensions.html#keyboard-handling

KEYS = [
  Key("up", "\x1b[A"),
  Key("up", "\x1bOA"),
  Key("up", "\x1b[1;2A", shift=True),
  Key("up", "\x1b[1;3A", meta=True),
  Key("up", "\x1b[1;5A", ctrl=True),
  Key("up", "\x1b[1;4A", shift=True, meta=True),
  Key("up", "\x1b[1;6A", shift=True, ctrl=True),
  Key("up", "\x1b[1;7A", meta=True, ctrl=True),
  Key("up", "\x1b[1;8A", shift=True, meta=True, ctrl=True),

  Key("down", "\x1b[B"),
  Key("down", "\x1bOB"),
  Key("down", "\x1b[1;2B", shift=True),
  Key("down", "\x1b[1;3B", meta=True),
  Key("down", "\x1b[1;5B", ctrl=True),
  Key("down", "\x1b[1;4B", shift=True, meta=True),
  Key("down", "\x1b[1;6B", shift=True, ctrl=True),
  Key("down", "\x1b[1;7B", meta=True, ctrl=True),
  Key("down", "\x1b[1;8B", shift=True, meta=True, ctrl=True),

  Key("right", "\x1b[C"),
  Key("right", "\x1bOC"),
  Key("right", "\x1b[1;2C", shift=True),
  Key("right", "\x1b[1;3C", meta=True),
  Key("right", "\x1b[1;5C", ctrl=True),
  Key("right", "\x1b[1;4C", shift=True, meta=True),
  Key("right", "\x1b[1;6C", shift=True, ctrl=True),
  Key("right", "\x1b[1;7C", meta=True, ctrl=True),
  Key("right", "\x1b[1;8C", shift=True, meta=True, ctrl=True),

  Key("left", "\x1b[D"),
  Key("left", "\x1bOD"),
  Key("left", "\x1b[1;2D", shift=True),
  Key("left", "\x1b[1;3D", meta=True),
  Key("left", "\x1b[1;5D", ctrl=True),
  Key("left", "\x1b[1;4D", shift=True, meta=True),
  Key("left", "\x1b[1;6D", shift=True, ctrl=True),
  Key("left", "\x1b[1;7D", meta=True, ctrl=True),
  Key("left", "\x1b[1;8D", shift=True, meta=True, ctrl=True),

  Key("return", "\r"),
  Key("return", "\x1b\r", meta=True),  # rxvt & kde
  Key("return", "\n", ctrl=True),  # unknown

  Key("backspace", "\x7f"),
  Key("backspace", "\x1b\x7f", meta=True),
  Key("backspace", "\b", ctrl=True),
  Key("backspace", "\x1b\x1b", meta=True, ctrl=True),

  Key("delete", "\x1b[3~"),
  Key("delete", "\x1b[3;2~", shift=True),
  Key("delete", "\x1b[3;3~", meta=True),
  Key("delete", "\x1b[3;5~", ctrl=True),
  Key("delete", "\x1b[3;4~", shift=True, meta=True),
  Key("delete", "\x1b[3;6~", shift=True, ctrl=True),
  Key("delete", "\x1b[3;7~", meta=True, ctrl=True),
  Key("delete", "\x1b[3;8~", shift=True, meta=True, ctrl=True),

  Key("tab", "\t"),
  Key("tab", "\x1b[Z", shift=True),
  Key("tab", "\x1b\t", meta=True),  # cannot properly test, assumed
  Key("tab", "\x1b\x1b[Z", shift=True, meta=True),  # cannot properly test, assumed

  Key("escape", "\x1b"),

  Key("insert", "\x1b[2~"),
  Key("insert", "\x1b[2;5~", ctrl=True),

  Key("home", "\x1b[H"),
  Key("home", "\x1bOH"),
  Key("home", "\x1b[1;5H", ctrl=True),

  Key("end", "\x1b[F"),
  Key("end", "\x1bOF"),
  Key("end", "\x1b[1;5F", ctrl=True),

  Key("pg_last", "\x1b[5~"),
  Key("pg_last", "\x1b[5;5~", ctrl=True),

  Key("pg_next", "\x1b[6~"),
  Key("pg_next", "\x1b[6;5~", ctrl=True),

  Key("f1", "\x1bOP"),

  Key("f2", "\x1bOQ"),

  Key("f3", "\x1bOR"),

  Key("f4", "\x1bOS"),

  Key("f5", "\x1b[15~"),

  Key("f6", "\x1b[17~"),

  Key("f7", "\x1b[18~"),

  Key("f8", "\x1b[19~"),

  Key("f9", "\x1b[20~"),

  Key("f10", "\x1b[21~"),

  Key("f11", "\x1b[23~"),

  Key("f12", "\x1b[24~"),
]