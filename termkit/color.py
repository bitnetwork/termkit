import collections
import colorsys
from typing import List, Tuple, Union
import typing

# predefine the internal collections so they are visible to Colors, as they contain instances of Color
ID_MAP = []
NAME_MAP = {}

class Color():
  """
  Abstraction of a RGB color.

  >>> Color(red=255, green=0, blue=0)
  <Color 'red'>
   
  >>> Color(red=255)
  <Color 'red'>

  >>> Color(rgb=(255, 0, 0))
  <Color 'red'>
  """
  __slots__ = ("rgb", )
  rgb: Tuple[int]

  GAMMA = 2.2

  def __init__(self, rgb: Tuple[int] = None, *_, red: int = 0, green: int = 0, blue: int = 0):
    if rgb is None:
      rgb = (red, green, blue)
    super().__setattr__("rgb", rgb)

  def __setattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field assignment")

  def __delattr__(self, *_):
    raise TypeError(f"{repr(self.__class__.__name__)} does not support field deletion")

  def __hash__(self):
    return hash(self.rgb)

  def __eq__(self, other):
    if not isinstance(other, Color):
      return NotImplemented
    return self.rgb == other.rgb

  # def __add__(self, other):
    # defined later

  # def __int__(self):
    # defined later

  def __str__(self):
    # return color name, id or hex number is fail
    raise NotImplementedError()

  @property
  def __hex__(self) -> str:
    return f"0x{self.red:02x}{self.green:02x}{self.blue:02x}"

  def __repr__(self):
    if len(self.names) > 0:
      return f"<{self.__class__.__name__} {repr(self.names[0])}>"
    try:
      return f"<{self.__class__.__name__} {repr(self.id)}>"
    except IndexError:
      return f"<{self.__class__.__name__} rgb={repr(self.rgb)}>"
  
  def __iter__(self):
    return iter(self.rgb)

  @staticmethod
  def gamma_expansion(channel: Union[float, int], gamma=GAMMA):
    """Converts a non-linear color channel to a linear one"""
    return round((channel / 255) ** gamma * 255)

  @staticmethod
  def gamma_compression(channel: int, gamma=GAMMA):
    """Converts a linear color channel to a non-linear one"""
    return Color.gamma_expansion(channel, 1 / gamma)

  @classmethod
  def from_lrgb(cls, lrgb: Tuple[float] = None, *_, red: float = 0, green: float = 0, blue: float = 0, gamma=GAMMA):
    """Contructs a Color instance based off of linear color channels"""
    if lrgb is None:
      lrgb = (red, green, blue)

    rgb = tuple(cls.gamma_compression(channel, gamma=gamma) for channel in lrgb)
    return cls(rgb)

  @property
  def red(self) -> int:
    """The red component of the Color"""
    return self.rgb[0]

  @property
  def green(self) -> int:
    """The green component of the Color"""
    return self.rgb[1]

  @property
  def blue(self) -> int:
    """The blue component of the Color"""
    return self.rgb[2]

  @property
  def hex(self) -> str:
    """Gets the web color hex string"""
    return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

  @property
  def id(self) -> int:
    """Gets the id number associated with the color, if available, else raise IndexError"""
    try:
      return ID_MAP.index(self)
    except ValueError:  # wow that's not descriptive at all, let's re-raise that
      raise IndexError()

  __int__ = id

  @property
  def names(self) -> List[str]:
    """Returns a list of all English color names mapping the color"""
    names = [key for key, value in NAME_MAP.items() if value == self]
    return names

  def lrgb(self, gamma=GAMMA) -> Tuple[float]:
    """Computes the linear rgb of the color using a gamma value"""
    return tuple(self.gamma_expansion(channel, gamma=gamma) for channel in self.rgb)

  def distance(self, other: "Color", gamma=GAMMA) -> float:
    """Computes the euclidean distance between two colors"""
    channels = zip(self.lrgb(gamma=gamma), other.lrgb(gamma=gamma))
    difference = sum(abs(s_channel - o_channel) for s_channel, o_channel in channels)
    return difference

  def closest_color(self, colors: typing.Iterable["Color"] = ID_MAP, gamma=GAMMA) -> "Color":
    """
    Finds the closest color in the color mapping.

    >>> Color(rgb=(0, 0, 239)).closest_color()
    <Color 'blue'>

    Downscale a color to the 16 color space
    >>> colors[60].closest_color(ID_MAP[:16])
    <Color 'gray'>
    """
    if self in colors:
      return self

    sums = [(color, self.distance(color, gamma=gamma)) for color in colors]
    return min(sums, key=lambda c: c[1])[0]

  def mix(self, other: "Color", gamma=GAMMA) -> "Color":
    """
    Mixes two colors, constructing a new color

    >>> colors["red"].mix(colors["blue"])
    <Color rgb=(186, 0, 186)>

    >>> colors["white"].mix(colors["black"])
    <Color rgb=(186, 186, 186)>
    """
    channels = zip(self.lrgb(gamma=gamma), other.lrgb(gamma=gamma))
    mixed_color = tuple(round((s_channel + o_channel) / 2) for s_channel, o_channel in channels)
    return self.from_lrgb(mixed_color)

  __add__ = mix

class ColorPalette():
  """
  Anonymous getter class to simplify contructing colors from ids, names, or hex strings.

  >>> colors["red"]
  <Color 'red'>

  >>> colors["#ffaa00"]
  <Color rgb=(255, 170, 0)>

  >>> colors[15]
  <Color 'white'>
  """
  def __getitem__(self, key: Union[str, int]):
    if type(key) is int:
      # raises indexError naturally
      return ID_MAP[key]

    if type(key) is str:
      if key.startswith("#"):
        rgb = int(key.lstrip("#"), base=16)

        # maybe later
        # if len(key) == 4:  # "#rgb"
          # pass

        if len(key) == 7:  # "#rrggbb"
          return Color(
            red=rgb >> 16 & 0xff,  # last two hex digits
            green=rgb >> 8 & 0xff,  # center two hex digits
            blue=rgb & 0xff,  # first two hex digits
          )

      else:
        # raises KeyError naturally
        return NAME_MAP[key]
    raise KeyError()

  def __iter__(self):
    return iter(ID_MAP)

  def items(self):
    return NAME_MAP.items()

# Global instance of ColorPallatte for ease of access
colors = ColorPalette()

# 256 xterm color list
ID_MAP += [
  Color(rgb=(0, 0, 0)),  # 0 black
  Color(rgb=(128, 0, 0)),  # 1 maroon
  Color(rgb=(0, 128, 0)),  # 2 green
  Color(rgb=(128, 128, 0)),  # 3 olive
  Color(rgb=(0, 0, 128)),  # 4 navy
  Color(rgb=(128, 0, 128)),  # 5 purple
  Color(rgb=(0, 128, 128)),  # 6 teal
  Color(rgb=(192, 192, 192)),  # 7 silver
  Color(rgb=(128, 128, 128)),  # 8 grey
  Color(rgb=(255, 0, 0)),  # 9 red
  Color(rgb=(0, 255, 0)),  # 10 lime
  Color(rgb=(255, 255, 0)),  # 11 yellow
  Color(rgb=(0, 0, 255)),  # 12 blue
  Color(rgb=(255, 0, 255)),  # 13 fuchsia
  Color(rgb=(0, 255, 255)),  # 14 aqua
  Color(rgb=(255, 255, 255)),  # 15 white
  Color(rgb=(0, 0, 0)),  # 16 grey0
  Color(rgb=(0, 0, 95)),  # 17 navyblue
  Color(rgb=(0, 0, 135)),  # 18 darkblue
  Color(rgb=(0, 0, 175)),  # 19 blue3
  Color(rgb=(0, 0, 215)),  # 20 blue3
  Color(rgb=(0, 0, 255)),  # 21 blue1
  Color(rgb=(0, 95, 0)),  # 22 darkgreen
  Color(rgb=(0, 95, 95)),  # 23 deepskyblue4
  Color(rgb=(0, 95, 135)),  # 24 deepskyblue4
  Color(rgb=(0, 95, 175)),  # 25 deepskyblue4
  Color(rgb=(0, 95, 215)),  # 26 dodgerblue3
  Color(rgb=(0, 95, 255)),  # 27 dodgerblue2
  Color(rgb=(0, 135, 0)),  # 28 green4
  Color(rgb=(0, 135, 95)),  # 29 springgreen4
  Color(rgb=(0, 135, 135)),  # 30 turquoise4
  Color(rgb=(0, 135, 175)),  # 31 deepskyblue3
  Color(rgb=(0, 135, 215)),  # 32 deepskyblue3
  Color(rgb=(0, 135, 255)),  # 33 dodgerblue1
  Color(rgb=(0, 175, 0)),  # 34 green3
  Color(rgb=(0, 175, 95)),  # 35 springgreen3
  Color(rgb=(0, 175, 135)),  # 36 darkcyan
  Color(rgb=(0, 175, 175)),  # 37 lightseagreen
  Color(rgb=(0, 175, 215)),  # 38 deepskyblue2
  Color(rgb=(0, 175, 255)),  # 39 deepskyblue1
  Color(rgb=(0, 215, 0)),  # 40 green3
  Color(rgb=(0, 215, 95)),  # 41 springgreen3
  Color(rgb=(0, 215, 135)),  # 42 springgreen2
  Color(rgb=(0, 215, 175)),  # 43 cyan3
  Color(rgb=(0, 215, 215)),  # 44 darkturquoise
  Color(rgb=(0, 215, 255)),  # 45 turquoise2
  Color(rgb=(0, 255, 0)),  # 46 green1
  Color(rgb=(0, 255, 95)),  # 47 springgreen2
  Color(rgb=(0, 255, 135)),  # 48 springgreen1
  Color(rgb=(0, 255, 175)),  # 49 mediumspringgreen
  Color(rgb=(0, 255, 215)),  # 50 cyan2
  Color(rgb=(0, 255, 255)),  # 51 cyan1
  Color(rgb=(95, 0, 0)),  # 52 darkred
  Color(rgb=(95, 0, 95)),  # 53 deeppink4
  Color(rgb=(95, 0, 135)),  # 54 purple4
  Color(rgb=(95, 0, 175)),  # 55 purple4
  Color(rgb=(95, 0, 215)),  # 56 purple3
  Color(rgb=(95, 0, 255)),  # 57 blueviolet
  Color(rgb=(95, 95, 0)),  # 58 orange4
  Color(rgb=(95, 95, 95)),  # 59 grey37
  Color(rgb=(95, 95, 135)),  # 60 mediumpurple4
  Color(rgb=(95, 95, 175)),  # 61 slateblue3
  Color(rgb=(95, 95, 215)),  # 62 slateblue3
  Color(rgb=(95, 95, 255)),  # 63 royalblue1
  Color(rgb=(95, 135, 0)),  # 64 chartreuse4
  Color(rgb=(95, 135, 95)),  # 65 darkseagreen4
  Color(rgb=(95, 135, 135)),  # 66 paleturquoise4
  Color(rgb=(95, 135, 175)),  # 67 steelblue
  Color(rgb=(95, 135, 215)),  # 68 steelblue3
  Color(rgb=(95, 135, 255)),  # 69 cornflowerblue
  Color(rgb=(95, 175, 0)),  # 70 chartreuse3
  Color(rgb=(95, 175, 95)),  # 71 darkseagreen4
  Color(rgb=(95, 175, 135)),  # 72 cadetblue
  Color(rgb=(95, 175, 175)),  # 73 cadetblue
  Color(rgb=(95, 175, 215)),  # 74 skyblue3
  Color(rgb=(95, 175, 255)),  # 75 steelblue1
  Color(rgb=(95, 215, 0)),  # 76 chartreuse3
  Color(rgb=(95, 215, 95)),  # 77 palegreen3
  Color(rgb=(95, 215, 135)),  # 78 seagreen3
  Color(rgb=(95, 215, 175)),  # 79 aquamarine3
  Color(rgb=(95, 215, 215)),  # 80 mediumturquoise
  Color(rgb=(95, 215, 255)),  # 81 steelblue1
  Color(rgb=(95, 255, 0)),  # 82 chartreuse2
  Color(rgb=(95, 255, 95)),  # 83 seagreen2
  Color(rgb=(95, 255, 135)),  # 84 seagreen1
  Color(rgb=(95, 255, 175)),  # 85 seagreen1
  Color(rgb=(95, 255, 215)),  # 86 aquamarine1
  Color(rgb=(95, 255, 255)),  # 87 darkslategray2
  Color(rgb=(135, 0, 0)),  # 88 darkred
  Color(rgb=(135, 0, 95)),  # 89 deeppink4
  Color(rgb=(135, 0, 135)),  # 90 darkmagenta
  Color(rgb=(135, 0, 175)),  # 91 darkmagenta
  Color(rgb=(135, 0, 215)),  # 92 darkviolet
  Color(rgb=(135, 0, 255)),  # 93 purple
  Color(rgb=(135, 95, 0)),  # 94 orange4
  Color(rgb=(135, 95, 95)),  # 95 lightpink4
  Color(rgb=(135, 95, 135)),  # 96 plum4
  Color(rgb=(135, 95, 175)),  # 97 mediumpurple3
  Color(rgb=(135, 95, 215)),  # 98 mediumpurple3
  Color(rgb=(135, 95, 255)),  # 99 slateblue1
  Color(rgb=(135, 135, 0)),  # 100 yellow4
  Color(rgb=(135, 135, 95)),  # 101 wheat4
  Color(rgb=(135, 135, 135)),  # 102 grey53
  Color(rgb=(135, 135, 175)),  # 103 lightslategrey
  Color(rgb=(135, 135, 215)),  # 104 mediumpurple
  Color(rgb=(135, 135, 255)),  # 105 lightslateblue
  Color(rgb=(135, 175, 0)),  # 106 yellow4
  Color(rgb=(135, 175, 95)),  # 107 darkolivegreen3
  Color(rgb=(135, 175, 135)),  # 108 darkseagreen
  Color(rgb=(135, 175, 175)),  # 109 lightskyblue3
  Color(rgb=(135, 175, 215)),  # 110 lightskyblue3
  Color(rgb=(135, 175, 255)),  # 111 skyblue2
  Color(rgb=(135, 215, 0)),  # 112 chartreuse2
  Color(rgb=(135, 215, 95)),  # 113 darkolivegreen3
  Color(rgb=(135, 215, 135)),  # 114 palegreen3
  Color(rgb=(135, 215, 175)),  # 115 darkseagreen3
  Color(rgb=(135, 215, 215)),  # 116 darkslategray3
  Color(rgb=(135, 215, 255)),  # 117 skyblue1
  Color(rgb=(135, 255, 0)),  # 118 chartreuse1
  Color(rgb=(135, 255, 95)),  # 119 lightgreen
  Color(rgb=(135, 255, 135)),  # 120 lightgreen
  Color(rgb=(135, 255, 175)),  # 121 palegreen1
  Color(rgb=(135, 255, 215)),  # 122 aquamarine1
  Color(rgb=(135, 255, 255)),  # 123 darkslategray1
  Color(rgb=(175, 0, 0)),  # 124 red3
  Color(rgb=(175, 0, 95)),  # 125 deeppink4
  Color(rgb=(175, 0, 135)),  # 126 mediumvioletred
  Color(rgb=(175, 0, 175)),  # 127 magenta3
  Color(rgb=(175, 0, 215)),  # 128 darkviolet
  Color(rgb=(175, 0, 255)),  # 129 purple
  Color(rgb=(175, 95, 0)),  # 130 darkorange3
  Color(rgb=(175, 95, 95)),  # 131 indianred
  Color(rgb=(175, 95, 135)),  # 132 hotpink3
  Color(rgb=(175, 95, 175)),  # 133 mediumorchid3
  Color(rgb=(175, 95, 215)),  # 134 mediumorchid
  Color(rgb=(175, 95, 255)),  # 135 mediumpurple2
  Color(rgb=(175, 135, 0)),  # 136 darkgoldenrod
  Color(rgb=(175, 135, 95)),  # 137 lightsalmon3
  Color(rgb=(175, 135, 135)),  # 138 rosybrown
  Color(rgb=(175, 135, 175)),  # 139 grey63
  Color(rgb=(175, 135, 215)),  # 140 mediumpurple2
  Color(rgb=(175, 135, 255)),  # 141 mediumpurple1
  Color(rgb=(175, 175, 0)),  # 142 gold3
  Color(rgb=(175, 175, 95)),  # 143 darkkhaki
  Color(rgb=(175, 175, 135)),  # 144 navajowhite3
  Color(rgb=(175, 175, 175)),  # 145 grey69
  Color(rgb=(175, 175, 215)),  # 146 lightsteelblue3
  Color(rgb=(175, 175, 255)),  # 147 lightsteelblue
  Color(rgb=(175, 215, 0)),  # 148 yellow3
  Color(rgb=(175, 215, 95)),  # 149 darkolivegreen3
  Color(rgb=(175, 215, 135)),  # 150 darkseagreen3
  Color(rgb=(175, 215, 175)),  # 151 darkseagreen2
  Color(rgb=(175, 215, 215)),  # 152 lightcyan3
  Color(rgb=(175, 215, 255)),  # 153 lightskyblue1
  Color(rgb=(175, 255, 0)),  # 154 greenyellow
  Color(rgb=(175, 255, 95)),  # 155 darkolivegreen2
  Color(rgb=(175, 255, 135)),  # 156 palegreen1
  Color(rgb=(175, 255, 175)),  # 157 darkseagreen2
  Color(rgb=(175, 255, 215)),  # 158 darkseagreen1
  Color(rgb=(175, 255, 255)),  # 159 paleturquoise1
  Color(rgb=(215, 0, 0)),  # 160 red3
  Color(rgb=(215, 0, 95)),  # 161 deeppink3
  Color(rgb=(215, 0, 135)),  # 162 deeppink3
  Color(rgb=(215, 0, 175)),  # 163 magenta3
  Color(rgb=(215, 0, 215)),  # 164 magenta3
  Color(rgb=(215, 0, 255)),  # 165 magenta2
  Color(rgb=(215, 95, 0)),  # 166 darkorange3
  Color(rgb=(215, 95, 95)),  # 167 indianred
  Color(rgb=(215, 95, 135)),  # 168 hotpink3
  Color(rgb=(215, 95, 175)),  # 169 hotpink2
  Color(rgb=(215, 95, 215)),  # 170 orchid
  Color(rgb=(215, 95, 255)),  # 171 mediumorchid1
  Color(rgb=(215, 135, 0)),  # 172 orange3
  Color(rgb=(215, 135, 95)),  # 173 lightsalmon3
  Color(rgb=(215, 135, 135)),  # 174 lightpink3
  Color(rgb=(215, 135, 175)),  # 175 pink3
  Color(rgb=(215, 135, 215)),  # 176 plum3
  Color(rgb=(215, 135, 255)),  # 177 violet
  Color(rgb=(215, 175, 0)),  # 178 gold3
  Color(rgb=(215, 175, 95)),  # 179 lightgoldenrod3
  Color(rgb=(215, 175, 135)),  # 180 tan
  Color(rgb=(215, 175, 175)),  # 181 mistyrose3
  Color(rgb=(215, 175, 215)),  # 182 thistle3
  Color(rgb=(215, 175, 255)),  # 183 plum2
  Color(rgb=(215, 215, 0)),  # 184 yellow3
  Color(rgb=(215, 215, 95)),  # 185 khaki3
  Color(rgb=(215, 215, 135)),  # 186 lightgoldenrod2
  Color(rgb=(215, 215, 175)),  # 187 lightyellow3
  Color(rgb=(215, 215, 215)),  # 188 grey84
  Color(rgb=(215, 215, 255)),  # 189 lightsteelblue1
  Color(rgb=(215, 255, 0)),  # 190 yellow2
  Color(rgb=(215, 255, 95)),  # 191 darkolivegreen1
  Color(rgb=(215, 255, 135)),  # 192 darkolivegreen1
  Color(rgb=(215, 255, 175)),  # 193 darkseagreen1
  Color(rgb=(215, 255, 215)),  # 194 honeydew2
  Color(rgb=(215, 255, 255)),  # 195 lightcyan1
  Color(rgb=(255, 0, 0)),  # 196 red1
  Color(rgb=(255, 0, 95)),  # 197 deeppink2
  Color(rgb=(255, 0, 135)),  # 198 deeppink1
  Color(rgb=(255, 0, 175)),  # 199 deeppink1
  Color(rgb=(255, 0, 215)),  # 200 magenta2
  Color(rgb=(255, 0, 255)),  # 201 magenta1
  Color(rgb=(255, 95, 0)),  # 202 orangered1
  Color(rgb=(255, 95, 95)),  # 203 indianred1
  Color(rgb=(255, 95, 135)),  # 204 indianred1
  Color(rgb=(255, 95, 175)),  # 205 hotpink
  Color(rgb=(255, 95, 215)),  # 206 hotpink
  Color(rgb=(255, 95, 255)),  # 207 mediumorchid1
  Color(rgb=(255, 135, 0)),  # 208 darkorange
  Color(rgb=(255, 135, 95)),  # 209 salmon1
  Color(rgb=(255, 135, 135)),  # 210 lightcoral
  Color(rgb=(255, 135, 175)),  # 211 palevioletred1
  Color(rgb=(255, 135, 215)),  # 212 orchid2
  Color(rgb=(255, 135, 255)),  # 213 orchid1
  Color(rgb=(255, 175, 0)),  # 214 orange1
  Color(rgb=(255, 175, 95)),  # 215 sandybrown
  Color(rgb=(255, 175, 135)),  # 216 lightsalmon1
  Color(rgb=(255, 175, 175)),  # 217 lightpink1
  Color(rgb=(255, 175, 215)),  # 218 pink1
  Color(rgb=(255, 175, 255)),  # 219 plum1
  Color(rgb=(255, 215, 0)),  # 220 gold1
  Color(rgb=(255, 215, 95)),  # 221 lightgoldenrod2
  Color(rgb=(255, 215, 135)),  # 222 lightgoldenrod2
  Color(rgb=(255, 215, 175)),  # 223 navajowhite1
  Color(rgb=(255, 215, 215)),  # 224 mistyrose1
  Color(rgb=(255, 215, 255)),  # 225 thistle1
  Color(rgb=(255, 255, 0)),  # 226 yellow1
  Color(rgb=(255, 255, 95)),  # 227 lightgoldenrod1
  Color(rgb=(255, 255, 135)),  # 228 khaki1
  Color(rgb=(255, 255, 175)),  # 229 wheat1
  Color(rgb=(255, 255, 215)),  # 230 cornsilk1
  Color(rgb=(255, 255, 255)),  # 231 grey100
  Color(rgb=(8, 8, 8)),  # 232 grey3
  Color(rgb=(18, 18, 18)),  # 233 grey7
  Color(rgb=(28, 28, 28)),  # 234 grey11
  Color(rgb=(38, 38, 38)),  # 235 grey15
  Color(rgb=(48, 48, 48)),  # 236 grey19
  Color(rgb=(58, 58, 58)),  # 237 grey23
  Color(rgb=(68, 68, 68)),  # 238 grey27
  Color(rgb=(78, 78, 78)),  # 239 grey30
  Color(rgb=(88, 88, 88)),  # 240 grey35
  Color(rgb=(98, 98, 98)),  # 241 grey39
  Color(rgb=(108, 108, 108)),  # 242 grey42
  Color(rgb=(118, 118, 118)),  # 243 grey46
  Color(rgb=(128, 128, 128)),  # 244 grey50
  Color(rgb=(138, 138, 138)),  # 245 grey54
  Color(rgb=(148, 148, 148)),  # 246 grey58
  Color(rgb=(158, 158, 158)),  # 247 grey62
  Color(rgb=(168, 168, 168)),  # 248 grey66
  Color(rgb=(178, 178, 178)),  # 249 grey70
  Color(rgb=(188, 188, 188)),  # 250 grey74
  Color(rgb=(198, 198, 198)),  # 251 grey78
  Color(rgb=(208, 208, 208)),  # 252 grey82
  Color(rgb=(218, 218, 218)),  # 253 grey85
  Color(rgb=(228, 228, 228)),  # 254 grey89
  Color(rgb=(238, 238, 238)),  # 255 grey93
]

NAME_MAP.update({
  # 8-bit standard color names
  "black": colors[0],
  "maroon": colors[1],
  "green": colors[2],
  "olive": colors[3],
  "navy": colors[4],
  "purple": colors[5],
  "teal": colors[6],
  "silver": colors[7],
  # 16-bit standard color names
  "gray": colors[8], "grey": colors[8],
  "red": colors[9],
  "lime": colors[10],
  "yellow": colors[11],
  "blue": colors[12],
  "fuchsia": colors[13], "magenta": colors[13],
  "aqua": colors[14],
  "white": colors[15],
})

if __name__ == "__main__":
    import doctest
    doctest.testmod()
