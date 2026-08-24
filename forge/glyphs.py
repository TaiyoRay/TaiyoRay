from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.misc.transform import Transform


def load(path, wght):
    f = TTFont(path)
    f = instancer.instantiateVariableFont(f, {"wght": wght})
    return f


def glyph_path(font, char, scale=1.0, dx=0.0, dy=0.0, flip=True):
    """Return (svg_path_d, advance, bounds) in a y-down coordinate system."""
    cmap = font.getBestCmap()
    gname = cmap[ord(char)]
    gs = font.getGlyphSet()
    g = gs[gname]

    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
    t = Transform(scale, 0, 0, -scale if flip else scale, dx, dy)
    tpen = TransformPen(pen, t)
    g.draw(tpen)

    bp = ControlBoundsPen(gs)
    g.draw(bp)
    xmin, ymin, xmax, ymax = bp.bounds
    b = (xmin * scale + dx,
         (-ymax * scale + dy) if flip else ymin * scale + dy,
         xmax * scale + dx,
         (-ymin * scale + dy) if flip else ymax * scale + dy)
    return pen.getCommands(), g.width * scale, b


def upem(font):
    return font["head"].unitsPerEm
