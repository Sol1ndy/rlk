"""Display-entity helpers of the P3/P4 module (p34.py): quaternions, transformations, summons.

Owned by the P3/P4 author (imported only by p34.py). Pure Python, no side effects.

Frames. Every display this module summons is first placed at a group origin and then turned to
the group's yaw with one `tp ... ~ ~ ~ ~ 0`, so its local frame is the boss frame of that moment:
+x = her LEFT, +y = up, +z = her FORWARD (Minecraft yaw 0 faces +z, and a display's local +x is
then +x = east = the left hand of someone facing south). All per-piece placement lives in the
transformation (translation, left_rotation, scale), computed here at generation time, so the only
runtime input is the group origin and yaw.

Navia card models (rlk:navia_fx/<kind>, tools/build_navia_fx_cards.py) are reused as plain
item models: "face" kinds lie in the local XY plane facing +z (ring, glow, star, burst: x,y in
+-0.5 at scale 1; shard: x in +-0.125, y in 0..1, pivot at the root), the "flat" crescent lies in
the local XZ plane, arc bulging toward +z, outer radius 0.485 x scale, head (thick, bright end) at
local +x (80 degrees to the left of +z), so a counter-clockwise (left-turning) sweep leads with the
head; mirror x for a clockwise one.

A text_display whose text is one space " " draws only its background: x in [-0.05, 0.075] b and
y in [0, 0.25] b (one line) at scale 1 (vanilla TextDisplayRenderer: 0.025 b per pixel, the space
advance 4 px plus a 1 px pad either side). Edges that must be exact use the y = 0 edge.
"""
import math

from .api import L

# ---------------------------------------------------------------------------------------------
# quaternions [x, y, z, w]


def qaxis(axis, deg):
    a = math.radians(deg) / 2
    n = math.sqrt(sum(c * c for c in axis))
    s = math.sin(a) / n
    return (axis[0] * s, axis[1] * s, axis[2] * s, math.cos(a))


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def qrot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # v' = q v q*
    tx = 2 * (y * vz - z * vy)
    ty = 2 * (z * vx - x * vz)
    tz = 2 * (x * vy - y * vx)
    return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))


QI = (0.0, 0.0, 0.0, 1.0)
FLAT_UP = qaxis((1, 0, 0), -90)          # a face card lying on the floor, facing up


def yaw_q(deg):
    """Turn about +y: +deg turns forward (+z) toward the LEFT (+x)."""
    return qaxis((0, 1, 0), deg)


def fwd(deg, r=1.0):
    """Horizontal point at angle deg (0 = forward, +90 = left) and distance r, boss frame."""
    a = math.radians(deg)
    return (r * math.sin(a), 0.0, r * math.cos(a))


# ---------------------------------------------------------------------------------------------
# NBT snippets


def f(v):
    return L.num(float(v), 4) + 'f'


def vec(v):
    return '[' + ','.join(f(c) for c in v) + ']'


def tf(t=(0, 0, 0), q=QI, s=(1, 1, 1), r=QI):
    if isinstance(s, (int, float)):
        s = (s, s, s)
    return f'transformation:{{translation:{vec(t)},left_rotation:{vec(q)},scale:{vec(s)},right_rotation:{vec(r)}}}'


def tags(*names):
    return 'Tags:[' + ','.join(f'"{n}"' for n in names) + ']'


def argb(hexrgb, alpha):
    """'#RRGGBB', alpha 0..1 -> signed 32-bit ARGB int (text_display background)."""
    v = (int(round(alpha * 255)) << 24) | int(hexrgb[1:], 16)
    return v - (1 << 32) if v & 0x80000000 else v


def rgb_int(hexrgb):
    return int(hexrgb[1:], 16)


BRIGHT = 'brightness:{sky:15,block:15}'


def item_display(model, tag_list, transform, bb='fixed', tp_dur=0, extra=''):
    """summon line (at ~ ~ ~) of an item_display showing item model `model` (full id)."""
    return (f'summon minecraft:item_display ~ ~ ~ {{{tags(*tag_list)},billboard:"{bb}",{BRIGHT},view_range:2f,'
            f'shadow_radius:0f,teleport_duration:{int(tp_dur)},interpolation_duration:0,{transform},'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{model}"}}}}{extra}}}')


def card_model(kind):
    return f'rlk:navia_fx/{kind}'


def block_display(block, tag_list, transform, glow=None, tp_dur=0, extra=''):
    g = f',Glowing:1b,glow_color_override:{rgb_int(glow)}' if glow else ''
    return (f'summon minecraft:block_display ~ ~ ~ {{{tags(*tag_list)},{BRIGHT},view_range:2f,shadow_radius:0f,'
            f'teleport_duration:{int(tp_dur)},interpolation_duration:0,block_state:{{id:"minecraft:{block}"}},'
            f'{transform}{g}{extra}}}')


def text_quad(colour_argb, tag_list, transform, bb='center', tp_dur=1):
    return (f'summon minecraft:text_display ~ ~ ~ {{{tags(*tag_list)},billboard:"{bb}",{BRIGHT},view_range:2f,'
            f'teleport_duration:{int(tp_dur)},interpolation_duration:0,background:{colour_argb},text:{{text:" "}},'
            f'{transform}}}')


def merge(sel, transform, dur):
    """Interpolate every entity of `sel` to `transform` over `dur` ticks (start now)."""
    return f'execute as {sel} run data merge entity @s {{start_interpolation:0,interpolation_duration:{int(dur)},{transform}}}'


# ---------------------------------------------------------------------------------------------
# shapes


def cube_tf(centre, size, q=QI):
    """block_display transformation of a cube of edge `size` centred at `centre` turned by q."""
    h = size / 2
    off = qrot(q, (h, h, h))
    return tf((centre[0] - off[0], centre[1] - off[1], centre[2] - off[2]), q, size)


def shard_tf(root, yaw, lean, length, roll=0.0, width=1.0):
    """Navia shard card (pivot at its root) planted at `root`, leaning `lean` degrees from vertical
    toward the boss-frame direction `yaw`, `length` blocks long; width x the card's own width."""
    q = qmul(yaw_q(yaw), qmul(qaxis((1, 0, 0), lean), qaxis((0, 0, 1), roll)))
    return tf(root, q, (length * width, length, length))


def crescent_q(head, mirror=False, tilt=None):
    """Rotation of a flat crescent whose head sits at boss-frame angle `head` (0 forward, + left).
    Unmirrored the head is 80 degrees left of the card's +z, mirrored 80 degrees right.
    tilt = (direction deg, angle deg): the swing plane is lowest toward `direction`."""
    centre = head + 80 if mirror else head - 80
    q = yaw_q(centre)
    if tilt:
        d, a = tilt
        axis = fwd(d + 90)                 # horizontal axis perpendicular to the low direction
        q = qmul(qaxis(axis, a), q)
    return q


def crescent_tf(head, radius, height, mirror=False, tilt=None, k=1.0):
    s = 2 * radius / 0.97 * k
    q = crescent_q(head, mirror, tilt)
    return tf((0, height, 0), q, (-s if mirror else s, s, s))


def band_tf(angle, a, B):
    """One of four pinwheel bands of a screen vignette whose aperture is a square of half-size a
    turned by 45 degrees (a diamond). The band's inner edge is the background's exact y = 0 edge."""
    sx = (2 * a + B) / 0.125
    sy = B / 0.25
    q = qaxis((0, 0, 1), angle)
    t = qrot(q, (-a + 0.05 * sx, a, 0.0))
    return tf(t, q, (sx, sy, 1))


def quad_tf(cx, cy, w, h, angle=0.0):
    """A background rectangle w x h centred at screen offset (cx, cy), turned by `angle`."""
    sx, sy = w / 0.125, h / 0.25
    q = qaxis((0, 0, 1), angle)
    c = qrot(q, (0.0125 * sx, h / 2, 0.0))
    return tf((cx - c[0], cy - c[1], 0.0), q, (sx, sy, 1))
