#!/usr/bin/env python3
"""Offline preview renderer for Minecraft item_display rigs (Narukami / rlk datapack).

Nobody can run Minecraft in this container, so this script re-implements just enough of
the game to SEE display-entity rigs: it interprets the datapack's summon / data merge /
data modify / tp / kill / tag / function commands, loads item definitions + block-style
item models from a resource pack, and rasterises them with a numpy z-buffer to a PNG.

CONVENTIONS (verified against tools/build_raiden_rig.mjs, build_raiden_judgment_rig.mjs and
the hazard generator comments; see --help-conventions):

  * World axes are Minecraft's: +X east, +Y up, +Z south.  Entity yaw 0 faces +Z (south),
    yaw 90 faces -X (west), yaw 180 faces -Z (north), yaw -90 faces +X (east).
  * One item_display vertex v (model pixels) is drawn at
        world = Pos + Ryaw/pitch * ( T + L * S * R * ( Ry180 * (v/16 - 0.5) ) )
    where Ry180 is vanilla ItemDisplayRenderer's extra 180 degree turn about Y,
    L/R are left/right_rotation quaternions [x,y,z,w], S the scale and T the translation.
    Entity orientation (billboard "fixed") is rotationYXZ(-yaw, pitch, 0).
    right_rotation [0,1,0,0] (used by the judgment rig, hazards, blink fragments) cancels
    the Ry180, so those meshes appear exactly as authored in model space.
  * Rig consequence: the boss rig authors "forward" as -Z, then mirrors z and the
    quaternion before writing; the head's skin FRONT face is the model's north (-Z) face,
    which Ry180 turns to local +Z.  So with boss yaw 0 the face looks toward +Z (south).
    A viewer standing in FRONT of a yaw-0 boss stands at +Z looking north (camera yaw 180):
    screen-right = +X (east) = the boss's LEFT hand side; screen-left = -X (west) = the
    boss's RIGHT hand side (the giant-sword arm).
  * The judgment (final calamity) rig is summoned at the arena origin (0,201,0) with
    Rotation [0,0].  The locked player camera is at (0,204,13) looking north (yaw 180,
    pitch -10), so from the player: screen-right = +X (east), screen-left = -X (west).

MODES
  --rig PHASE CLIP TICK    rig/spawn + rig/select/CLIP + rig/poses/<phase>/CLIP/TICK
                           PHASE = 0..3 or normal|forming|armored|exhausted
  --judgment TICK          judgment_rig/start + judgment_rig/frame/(TICK-frame_offset)
                           (frame/N carries the generator's pose(N+1), so by default
                           --judgment 120 shows pose(120) = the contact pose)
  --spawn F.. --apply F..  generic: run the spawn files, then the apply files in order.
                           Files are rlk:function ids, paths relative to
                           <dp>/data/rlk/function, or file paths.  '{t}' in a name is
                           replaced by the tick (for --strip).
  --item MODEL_ID          render raw item model(s) at the origin with identity transform.
  --strip a..b[:step]      render one panel per tick (filmstrip).  Combine with --track.

EXAMPLES (run from anywhere; default --dp is the live datapack, default --rp the scratch rp)
  P=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/preview
  python3 $P/raiden_preview.py --rig armored idle 0 -o out.png          # front,right,top,iso
  python3 $P/raiden_preview.py --rig 2 arm_sweep 0 --strip 0..9 --views front \
          --track rlk_rd_giant_weapon:9,31.2,8                            # swing filmstrip + tip path
  python3 $P/raiden_preview.py --judgment 120 --camera-preset judgment    # camera,front,top,right
  python3 $P/raiden_preview.py --judgment 0 --camera-preset judgment --strip 104..126:2 \
          --track rlk_rd_j_sword:8.86,30.4,8 --track-range 96..140        # ultimate from the player
  python3 $P/raiden_preview.py --spawn rlk:boss/raiden/movement/depart_armored \
          --apply rlk:boss/raiden/movement/fx_tick --as rlk_rd_move_fx \
          --score rdMvPhase=2 --score rdMvKind=1 --score rdMvAge=2       # generic files
  python3 $P/raiden_preview.py --item rlk:raiden/giant_katana --item-cancel-flip --no-grid
  $P/make_rp.sh /home/user/rlk/roguelike $MYRP     # rebuild an RP (+ datapack copy $MYRP_dp)
  --track prints, per tick, the point's position, its on-screen direction of travel
  (scr-dir: +x = screen right, +y = screen up, in the FIRST view) and lead=model<axis>, the item
  model axis that best faces the direction of travel (e.g. judgment katana: model -X = white
  cutting edge, +X = blue spine, +-Z = flat faces), so "edge leads" means lead=model-X.

HELD PROPS (10-29, checked against the 26.3 client jar)
  A hand prop (katana, yari, drum stick, dagger, staff) is just another item_display: the client applies the
  transformation, then ItemDisplayRenderer.submitInner's Ry180, then the item model's display transform for the
  entity's item_display context -- "none" for every rig here, and ItemTransforms.getTransform(NONE) is the identity
  (only thirdperson/firstperson/head/gui/ground/fixed/on_shelf read the model's "display" block). Nothing flips a
  prop in game that this renderer does not flip. A prop pointing straight back is foreshortened in a FRONT view,
  so judge grips from the RIGHT (side) view, or run --held <tag> (arrow + fwd/up/right table, REVERSED? flag).
  The ch2 swarm (ns katana, sp yari, dr sticks) shipped reversed because ch2mob/rig.humanoid read the authored
  weapon angle on the prop's raw +Y while the arm hangs along -Y; fixed in rig.humanoid (HAND_GRIP).

TEXTURES / BLENDING (vanilla 26.x item-display emulation, v2)
  --tex-mode uv            nearest-neighbour texel sampling with face uv + rotation (default);
                           avg = one alpha-weighted average colour per texture (old look).
  --alpha-cutout 0.1       fragments below alpha 0.1 are discarded (vanilla item shaders).
  --blend mc               sprites with partial alpha are translucent as a whole; their quads are
                           sorted back-to-front by CENTROID distance and drawn with depth test AND
                           depth write (a translucent card drawn first hides cards behind it).
                           --blend exact = order-independent per-pixel compositing.
  --light view|mc|flat     view = soft view-relative lambert (default); mc = vanilla entity diffuse
                           light (up 1.0, N/S 0.74, E/W 0.5); flat = none.
  --floor [R,G,B]          opaque floor at y=0 (default light_gray_concrete 125,125,115).
  Quads crossing the near plane are clipped (big floor decals render from inside them).
  Only sprites with a .png.mcmeta 'animation' section are treated as animated strips.

Run with -h for every option.  Output: one PNG grid, panels labelled.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

HERE = Path(__file__).resolve().parent
DEFAULT_DP = Path('/home/user/rlk/roguelike')
DEFAULT_RP = HERE / 'rp'
PHASES = {0: 'normal', 1: 'forming', 2: 'armored', 3: 'exhausted'}

# Average colours of vanilla concrete textures (the resource pack's rlk:player_motion/*
# concrete swatches are copies of these; the real pack is not in this container).
VANILLA_CONCRETE = {
    'white': (207, 213, 214), 'orange': (224, 97, 0), 'magenta': (169, 48, 159),
    'light_blue': (35, 137, 198), 'yellow': (240, 175, 21), 'lime': (94, 168, 24),
    'pink': (213, 101, 142), 'gray': (54, 57, 61), 'light_gray': (125, 125, 115),
    'cyan': (21, 119, 136), 'purple': (100, 31, 156), 'blue': (44, 46, 143),
    'brown': (96, 59, 31), 'green': (73, 91, 36), 'red': (142, 32, 32), 'black': (8, 10, 15),
}
SPECIAL_TEXTURES = {'rlk:cm/fm/metal': (0xD9, 0xB4, 0x4A, 255)}
MISSING_RGBA = (255, 0, 255, 255)


class Log:
    def __init__(self, quiet=False):
        self.quiet = quiet
        self.counts = {}
        self.notes = []

    def count(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1

    def note(self, msg):
        if msg not in self.notes:
            self.notes.append(msg)
            if not self.quiet:
                print('[preview] ' + msg, file=sys.stderr)


LOG = Log()

# ----------------------------------------------------------------------------- SNBT


class SNBTError(ValueError):
    pass


_NUM_RE = re.compile(r'^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?([bslfdBSLFD])?$')


def _ws(s, i):
    n = len(s)
    while i < n and s[i] in ' \t\r\n':
        i += 1
    return i


def _string(s, i):
    q = s[i]
    i += 1
    out = []
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({'n': '\n', 't': '\t'}.get(nxt, nxt))
            i += 2
            continue
        if c == q:
            return ''.join(out), i + 1
        out.append(c)
        i += 1
    raise SNBTError('unterminated string')


def _scalar(tok):
    low = tok.lower()
    if low == 'true':
        return 1
    if low == 'false':
        return 0
    m = _NUM_RE.match(tok)
    if m:
        body = tok[:-1] if m.group(1) else tok
        if m.group(1) and m.group(1).lower() in 'bsl' and re.match(r'^[-+]?\d+$', body):
            return int(body)
        if re.match(r'^[-+]?\d+$', body) and not m.group(1):
            return int(body)
        return float(body)
    return tok


def snbt_value(s, i=0):
    i = _ws(s, i)
    if i >= len(s):
        raise SNBTError('unexpected end')
    c = s[i]
    if c == '{':
        d = {}
        i = _ws(s, i + 1)
        if i < len(s) and s[i] == '}':
            return d, i + 1
        while True:
            i = _ws(s, i)
            if s[i] in '"\'':
                k, i = _string(s, i)
            else:
                j = i
                while j < len(s) and (s[j].isalnum() or s[j] in '_-.+'):
                    j += 1
                k, i = s[i:j], j
            i = _ws(s, i)
            if i >= len(s) or s[i] != ':':
                raise SNBTError(f'expected ":" at {i}: {s[max(0, i - 20):i + 20]!r}')
            v, i = snbt_value(s, i + 1)
            d[k] = v
            i = _ws(s, i)
            if i < len(s) and s[i] == ',':
                i = _ws(s, i + 1)
                if i < len(s) and s[i] == '}':
                    return d, i + 1
                continue
            if i < len(s) and s[i] == '}':
                return d, i + 1
            raise SNBTError(f'expected , or }} at {i}')
    if c == '[':
        i = _ws(s, i + 1)
        if i + 1 < len(s) and s[i] in 'BILbil' and s[i + 1] == ';':
            i = _ws(s, i + 2)
        lst = []
        if i < len(s) and s[i] == ']':
            return lst, i + 1
        while True:
            v, i = snbt_value(s, i)
            lst.append(v)
            i = _ws(s, i)
            if i < len(s) and s[i] == ',':
                i = _ws(s, i + 1)
                if i < len(s) and s[i] == ']':
                    return lst, i + 1
                continue
            if i < len(s) and s[i] == ']':
                return lst, i + 1
            raise SNBTError(f'expected , or ] at {i}')
    if c in '"\'':
        return _string(s, i)
    j = i
    while j < len(s) and s[j] not in ',]} \t\r\n':
        j += 1
    return _scalar(s[i:j]), j


def parse_snbt(s):
    v, i = snbt_value(s, 0)
    return v


def deep_merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = json.loads(json.dumps(v))
    return dst


def split_tokens(s):
    """Split a command on top-level whitespace, keeping [..], {..}, quotes intact."""
    out, cur, depth, q, i = [], [], 0, None, 0
    while i < len(s):
        c = s[i]
        if q:
            cur.append(c)
            if c == '\\' and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
            cur.append(c)
        elif c in '[{(':
            depth += 1
            cur.append(c)
        elif c in ']})':
            depth -= 1
            cur.append(c)
        elif c.isspace() and depth == 0:
            if cur:
                out.append(''.join(cur))
                cur = []
        else:
            cur.append(c)
        i += 1
    if cur:
        out.append(''.join(cur))
    return out


def split_path(path):
    """NBT path 'item.components."minecraft:item_model"' -> ['item','components','minecraft:item_model']."""
    parts, cur, q = [], [], None
    for c in path:
        if q:
            if c == q:
                q = None
            else:
                cur.append(c)
        elif c in '"\'':
            q = c
        elif c == '.':
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
    parts.append(''.join(cur))
    out = []
    for p in parts:
        m = re.match(r'^(.*?)((?:\[-?\d+\])*)$', p)
        if m and m.group(2):
            if m.group(1):
                out.append(m.group(1))
            out += [int(x) for x in re.findall(r'\[(-?\d+)\]', m.group(2))]
        else:
            out.append(p)
    return out

# ----------------------------------------------------------------------------- maths


def quat_to_mat(q):
    x, y, z, w = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def quat_from_nbt(v):
    if isinstance(v, dict):
        ax = np.array(v.get('axis', [0, 1, 0]), float)
        n = np.linalg.norm(ax)
        ax = ax / n if n > 0 else np.array([0, 1, 0.])
        a = float(v.get('angle', 0))
        s = math.sin(a / 2)
        return np.array([ax[0] * s, ax[1] * s, ax[2] * s, math.cos(a / 2)])
    q = np.array([float(x) for x in v], float)
    n = np.linalg.norm(q)
    return q / n if n > 1e-12 else np.array([0, 0, 0, 1.])


def rot_y(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


RY180 = np.diag([-1.0, 1.0, -1.0])


def transformation_matrix(tr):
    """4x4 matrix of a display 'transformation' NBT (decomposed or 16-float row-major)."""
    M = np.eye(4)
    if tr is None:
        return M
    if isinstance(tr, list):
        if len(tr) == 16:
            return np.array([float(x) for x in tr]).reshape(4, 4)
        LOG.note('transformation list without 16 floats; using identity')
        return M
    t = np.array([float(x) for x in tr.get('translation', [0, 0, 0])])
    L = quat_to_mat(quat_from_nbt(tr.get('left_rotation', [0, 0, 0, 1])))
    S = np.diag([float(x) for x in tr.get('scale', [1, 1, 1])])
    R = quat_to_mat(quat_from_nbt(tr.get('right_rotation', [0, 0, 0, 1])))
    M[:3, :3] = L @ S @ R
    M[:3, 3] = t
    return M


def entity_orientation(yaw, pitch):
    # DisplayRenderer FIXED billboard: rotationYXZ(-yaw, pitch, 0)
    return rot_y(-yaw) @ rot_x(pitch)


def mc_forward(yaw, pitch=0.0):
    y, p = math.radians(yaw), math.radians(pitch)
    return np.array([-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p)])


def norm(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v

# ----------------------------------------------------------------------------- assets


def procedural_skin():
    """64x64 stand-in for the unavailable rlk:raiden/skin (standard player-skin layout).

    Head front = peach face with violet eyes so facing is obvious; hair = dark purple;
    torso/arms = purple kimono with a gold sash and pale collar on the FRONT; hands peach;
    legs dark.  Overlay (hat/jacket/sleeve/pants) regions are transparent."""
    a = np.zeros((64, 64, 4), float)

    def fill(x0, y0, x1, y1, rgb, alpha=1.0):
        a[y0:y1, x0:x1] = (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, alpha)
    HAIR, SKIN, KIM, KIM_L, DARK, SASH = (60, 34, 96), (241, 204, 178), (108, 64, 168), (196, 170, 232), (32, 26, 44), (222, 176, 82)
    fill(0, 0, 32, 16, HAIR)            # head: all hair by default
    fill(16, 0, 24, 8, SKIN)            # head bottom (chin)
    fill(8, 8, 16, 16, SKIN)            # head FRONT face
    fill(8, 8, 16, 10, HAIR)            # fringe
    fill(9, 12, 11, 13, (110, 40, 190)); fill(13, 12, 15, 13, (110, 40, 190))   # eyes
    fill(9, 11, 11, 12, (250, 250, 255)); fill(13, 11, 15, 12, (250, 250, 255))
    fill(11, 14, 13, 15, (205, 110, 120))                                          # mouth
    fill(16, 16, 40, 32, KIM)           # torso all faces
    fill(20, 20, 28, 32, KIM)           # torso front
    for r in range(5):                  # pale V collar on the front only
        fill(20 + r, 20 + r, 21 + r, 21 + r, KIM_L); fill(27 - r, 20 + r, 28 - r, 21 + r, KIM_L)
    fill(16, 26, 40, 28, SASH)          # sash all around
    fill(20, 26, 28, 28, (240, 200, 90))
    fill(40, 16, 56, 32, KIM); fill(44, 20, 48, 29, KIM_L)   # right arm, front stripe
    fill(40, 29, 56, 32, SKIN); fill(48, 16, 52, 20, SKIN)   # right hand
    fill(32, 48, 48, 64, KIM); fill(36, 52, 40, 61, KIM_L)   # left arm
    fill(32, 61, 48, 64, SKIN); fill(40, 48, 44, 52, SKIN)   # left hand
    fill(0, 16, 16, 32, DARK); fill(0, 20, 16, 23, KIM)      # right leg
    fill(16, 48, 32, 64, DARK); fill(16, 52, 32, 55, KIM)    # left leg
    return a


ELEMENT_FACES = ('north', 'south', 'east', 'west', 'up', 'down')


def face_corners(face, lo, hi):
    """TL, TR, BR, BL as seen from outside the face (vanilla UV orientation)."""
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    return {
        'north': [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        'south': [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        'east': [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
        'west': [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        'up': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        'down': [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
    }[face]


def default_uv(face, lo, hi):
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    return {
        'north': [16 - x1, 16 - y1, 16 - x0, 16 - y0], 'south': [x0, 16 - y1, x1, 16 - y0],
        'east': [16 - z1, 16 - y1, 16 - z0, 16 - y0], 'west': [z0, 16 - y1, z1, 16 - y0],
        'up': [x0, z0, x1, z1], 'down': [x0, 16 - z1, x1, 16 - z0],
    }[face]


def element_rotation_fn(rot):
    if not rot:
        return None
    origin = np.array(rot.get('origin', [8, 8, 8]), float)
    if 'axis' in rot:
        ang = float(rot.get('angle', 0))
        ax = rot['axis']
        R = {'x': rot_x, 'y': rot_y, 'z': rot_z}[ax](ang)
        scale = np.ones(3)
        if rot.get('rescale') and abs(ang) > 1e-6:
            f = 1 / math.cos(math.radians(abs(ang)))
            scale = np.array([f, f, f])
            scale[{'x': 0, 'y': 1, 'z': 2}[ax]] = 1
    else:
        R = rot_x(float(rot.get('x', 0)))
        R = rot_y(float(rot.get('y', 0))) @ R
        R = rot_z(float(rot.get('z', 0))) @ R
        scale = np.ones(3)
    return lambda pts: (np.asarray(pts) - origin) @ R.T * scale + origin


class Assets:
    def __init__(self, rps, skin=None):
        self.rps = [Path(p) for p in rps]
        self.skin = skin
        self.tex_ids = {}
        self.tex_uniform = []      # rgba float or None
        self.tex_arrays = []       # (H,W,4) float or None
        self.tex_names = []
        self.tex_kind = []         # 'solid' | 'cutout' | 'translucent' (vanilla sprite material routing)
        self.tex_avg = []          # alpha-weighted average rgba (for --tex-mode avg)
        self.models = {}
        self.items = {}
        self.missing_items = set()
        self.missing_textures = set()

    def find(self, ns, rel):
        for rp in self.rps:
            p = rp / 'assets' / ns / rel
            if p.exists():
                return p
        return None

    @staticmethod
    def split_id(ident, default_ns='minecraft'):
        if ':' in ident:
            ns, path = ident.split(':', 1)
        else:
            ns, path = default_ns, ident
        return ns, path

    def texture(self, tid):
        if tid in self.tex_ids:
            return self.tex_ids[tid]
        ns, path = self.split_id(tid)
        uniform, arr = None, None
        p = self.find(ns, f'textures/{path}.png')
        if tid == 'rlk:raiden/skin' and self.skin:
            p = Path(self.skin)
        if p is not None:
            img = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.0
            meta = Path(str(p) + '.mcmeta')
            if meta.exists():                          # animated sprite: first frame only
                try:
                    anim = json.loads(meta.read_text(encoding='utf-8')).get('animation')
                except ValueError:
                    anim = None
                if anim is not None:
                    fw = int(anim.get('width', img.shape[1]))
                    fh = int(anim.get('height', img.shape[1] if 'width' not in anim else img.shape[0]))
                    img = img[:fh, :fw]
            flat = img.reshape(-1, 4)
            if np.all(np.abs(flat - flat[0]) < 1e-6):
                uniform = flat[0].copy()
            else:
                arr = img
        elif tid == 'rlk:raiden/skin':
            arr = procedural_skin()
            LOG.note('rlk:raiden/skin not in resource pack: using procedural stand-in skin (front face = peach face)')
        elif tid in SPECIAL_TEXTURES:
            uniform = np.array(SPECIAL_TEXTURES[tid], float) / 255
        else:
            m = re.search(r'(?:^|/)([a-z_]+)_concrete$', path)
            if m and m.group(1) in VANILLA_CONCRETE:
                uniform = np.array((*VANILLA_CONCRETE[m.group(1)], 255), float) / 255
            else:
                uniform = np.array(MISSING_RGBA, float) / 255
                self.missing_textures.add(tid)
                LOG.note(f'missing texture {tid} -> magenta')
        idx = len(self.tex_names)
        self.tex_ids[tid] = idx
        self.tex_names.append(tid)
        self.tex_uniform.append(uniform)
        self.tex_arrays.append(arr)
        a = (uniform[None, :] if uniform is not None else arr.reshape(-1, 4))
        alpha = a[:, 3]
        if np.all(alpha > 0.999):
            kind = 'solid'
        elif np.all((alpha < 0.001) | (alpha > 0.999)):
            kind = 'cutout'
        else:
            kind = 'translucent'
        self.tex_kind.append(kind)
        wsum = alpha.sum()
        rgb = (a[:, :3] * alpha[:, None]).sum(0) / wsum if wsum > 1e-9 else np.zeros(3)
        self.tex_avg.append(np.array([*rgb, alpha.mean()]))
        return idx

    def load_model_json(self, model_id, depth=0):
        ns, path = self.split_id(model_id)
        p = self.find(ns, f'models/{path}.json')
        if p is None:
            return None
        m = json.loads(p.read_text(encoding='utf-8'))
        if 'parent' in m and depth < 8:
            parent = self.load_model_json(m['parent'], depth + 1) or {}
            merged = {'textures': {**parent.get('textures', {}), **m.get('textures', {})}}
            merged['elements'] = m.get('elements', parent.get('elements'))
            return merged
        return m

    def model(self, model_id):
        if model_id in self.models:
            return self.models[model_id]
        m = self.load_model_json(model_id)
        baked = None
        if m is None:
            LOG.note(f'missing model {model_id}')
        elif not m.get('elements'):
            LOG.note(f'model {model_id} has no elements (flat/generated items are not rendered)')
        else:
            baked = self.bake(m)
        self.models[model_id] = baked
        return baked

    def resolve_tex(self, textures, ref):
        seen = 0
        while ref.startswith('#') and seen < 10:
            ref = textures.get(ref[1:], '')
            seen += 1
        return ref if ref and not ref.startswith('#') else 'rlk:__missing__'

    def bake(self, m):
        textures = m.get('textures', {})
        corners, uvs, tex, tint = [], [], [], []
        for el in m['elements']:
            f, t = np.array(el['from'], float), np.array(el['to'], float)
            lo, hi = np.minimum(f, t), np.maximum(f, t)
            rotfn = element_rotation_fn(el.get('rotation'))
            for face, spec in el.get('faces', {}).items():
                if face not in ELEMENT_FACES:
                    continue
                c = np.array(face_corners(face, lo, hi), float)
                if rotfn:
                    c = rotfn(c)
                u1, v1, u2, v2 = spec.get('uv') or default_uv(face, lo, hi)
                uvc = [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]
                k = (int(spec.get('rotation', 0)) // 90) % 4
                uvc = [uvc[(i - k) % 4] for i in range(4)]
                corners.append(c / 16.0 - 0.5)
                uvs.append(np.array(uvc, float) / 16.0)
                tex.append(self.texture(self.resolve_tex(textures, spec.get('texture', '#missing'))))
                tint.append(int(spec.get('tintindex', -1)))
        if not corners:
            return None
        return {'corners': np.array(corners), 'uv': np.array(uvs), 'tex': np.array(tex, int), 'tint': np.array(tint, int)}

    def item(self, item_model):
        """item_model id -> list of (baked, tints)."""
        if item_model in self.items:
            return self.items[item_model]
        ns, path = self.split_id(item_model)
        p = self.find(ns, f'items/{path}.json')
        out = []
        if p is None:
            self.missing_items.add(item_model)
            LOG.note(f'missing item definition {item_model}')
        else:
            d = json.loads(p.read_text(encoding='utf-8'))
            self._collect(d.get('model', {}), out)
        self.items[item_model] = out
        return out

    def _collect(self, node, out):
        typ = node.get('type', 'minecraft:model').replace('minecraft:', '')
        if typ == 'model':
            baked = self.model(node['model'])
            if baked is not None:
                tints = []
                for tdef in node.get('tints', []):
                    if tdef.get('type', '').replace('minecraft:', '') == 'constant':
                        v = tdef.get('value', -1)
                        if isinstance(v, list):
                            tints.append(np.array(v[:3], float))
                        else:
                            v = int(v) & 0xFFFFFF
                            tints.append(np.array([(v >> 16) & 255, (v >> 8) & 255, v & 255], float) / 255)
                    else:
                        LOG.note(f'tint type {tdef.get("type")} not supported -> white')
                        tints.append(np.ones(3))
                out.append((baked, tints))
        elif typ == 'composite':
            for sub in node.get('models', []):
                self._collect(sub, out)
        elif typ in ('select', 'condition', 'range_dispatch'):
            LOG.note(f'item model type {typ}: rendering fallback/first branch only')
            cand = node.get('fallback') or node.get('on_false')
            if cand is None:
                cases = node.get('cases') or node.get('entries') or []
                if cases:
                    cand = cases[0].get('model')
            if cand:
                self._collect(cand, out)
        elif typ != 'empty':
            LOG.note(f'item model type {typ} not supported')

# ----------------------------------------------------------------------------- scene


def _uuid_int(s):
    """Minecraft's UUID.fromString: five dash-separated hex groups, each may be shortened."""
    a, b, c, d, e = (int(x, 16) for x in s.split('-'))
    return (a << 96) | (b << 80) | (c << 64) | (d << 48) | e


class Entity:
    @property
    def uuid(self):
        u = self.nbt.get('UUID')
        if not isinstance(u, list) or len(u) != 4:
            return None
        v = 0
        for x in u:
            v = (v << 32) | (int(x) & 0xFFFFFFFF)
        return v

    def __init__(self, etype, pos, yaw, pitch, nbt, idx):
        self.etype = etype
        self.pos = np.array(pos, float)
        self.yaw = yaw
        self.pitch = pitch
        self.nbt = nbt
        self.idx = idx
        self.alive = True

    @property
    def tags(self):
        return set(self.nbt.get('Tags', []))

    def item_model(self):
        item = self.nbt.get('item') or {}
        comps = item.get('components') or {}
        return comps.get('minecraft:item_model') or comps.get('item_model')


class Ctx:
    def __init__(self, pos, yaw, pitch, executor=None):
        self.pos = np.array(pos, float)
        self.yaw = yaw
        self.pitch = pitch
        self.executor = executor

    def copy(self):
        return Ctx(self.pos.copy(), self.yaw, self.pitch, self.executor)


class StopFunction(Exception):
    pass


class Scene:
    """Tiny interpreter for the display-entity subset of mcfunction."""

    def __init__(self, dp, origin=(0, 0, 0), scores=None, macros=None, max_depth=4, follow=True):
        self.dp = Path(dp)
        self.origin = np.array(origin, float)
        self.entities = []
        self.scores = scores or {}
        self.macros = macros or {}
        self.max_depth = max_depth
        self.follow = follow

    # ---- files
    def resolve(self, ident):
        ident = ident.strip()
        p = Path(ident)
        if p.suffix == '.mcfunction' and p.exists():
            return p
        if ':' in ident:
            ns, path = ident.split(':', 1)
            cand = self.dp / 'data' / ns / 'function' / (path + '.mcfunction')
        else:
            cand = self.dp / 'data/rlk/function' / (ident if ident.endswith('.mcfunction') else ident + '.mcfunction')
        if cand.exists():
            return cand
        raise FileNotFoundError(f'function file not found: {ident} ({cand})')

    def run_file(self, ident, ctx, macros=None, depth=0):
        path = self.resolve(ident)
        macros = dict(self.macros, **(macros or {}))
        try:
            for raw in path.read_text(encoding='utf-8').splitlines():
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('$'):
                    keys = re.findall(r'\$\(([A-Za-z0-9_]+)\)', line)
                    if any(k not in macros for k in keys):
                        LOG.count('macro line skipped (missing keys)')
                        continue
                    line = re.sub(r'\$\(([A-Za-z0-9_]+)\)', lambda m: str(macros[m.group(1)]), line[1:])
                self.command(line, ctx.copy(), depth)
        except StopFunction:
            pass

    # ---- selectors
    def select(self, sel, ctx):
        if re.match(r'^[0-9a-fA-F]+-[0-9a-fA-F]+-[0-9a-fA-F]+-[0-9a-fA-F]+-[0-9a-fA-F]+$', sel):
            want = int(sel.replace('-', ''), 16) if len(sel) == 36 else _uuid_int(sel)
            return [e for e in self.entities if e.alive and e.uuid == want]
        if sel == '@s':
            return [ctx.executor] if ctx.executor is not None and ctx.executor.alive else None
        m = re.match(r'^@([enarps])(?:\[(.*)\])?$', sel)
        if not m:
            return None
        if m.group(1) in 'aprs':
            return None              # players / unknown executor: not part of the scene
        args = split_args(m.group(2) or '')
        res = [e for e in self.entities if e.alive]
        limit = None
        for k, v in args:
            if k == 'tag':
                if v.startswith('!'):
                    res = [e for e in res if v[1:] not in e.tags] if v[1:] else [e for e in res if e.tags]
                else:
                    res = [e for e in res if v in e.tags] if v else [e for e in res if not e.tags]
            elif k == 'type':
                neg = v.startswith('!')
                t = v.lstrip('!').replace('minecraft:', '')
                res = [e for e in res if (e.etype == t) != neg]
            elif k == 'limit':
                limit = int(v)
            elif k in ('scores', 'distance', 'sort', 'x', 'y', 'z', 'dx', 'dy', 'dz', 'nbt', 'predicate'):
                LOG.count(f'selector arg {k} ignored')
        if m.group(1) == 'n':
            limit = 1
        if limit is not None:
            res = res[:limit]
        return res

    # ---- coordinates
    def coords(self, toks, ctx):
        if len(toks) < 3:
            raise ValueError('need 3 coords')
        if any(t.startswith('^') for t in toks):
            f = mc_forward(ctx.yaw, ctx.pitch)
            left = np.array([math.cos(math.radians(ctx.yaw)), 0, math.sin(math.radians(ctx.yaw))])
            up = np.cross(f, left)
            vals = [float(t[1:] or 0) for t in toks]
            return ctx.pos + left * vals[0] + up * vals[1] + f * vals[2]
        out = []
        for i, t in enumerate(toks):
            if t.startswith('~'):
                out.append(ctx.pos[i] + float(t[1:] or 0))
            else:
                out.append(float(t) - self.origin[i])
        return np.array(out)

    @staticmethod
    def rot(tok, base):
        return base + float(tok[1:] or 0) if tok.startswith('~') else float(tok)

    # ---- commands
    def command(self, line, ctx, depth):
        toks = split_tokens(line)
        if not toks:
            return
        head = toks[0]
        try:
            if head == 'execute':
                self.execute(toks, 1, ctx, depth)
            elif head == 'summon':
                self.summon(toks, ctx)
            elif head == 'data':
                self.data(toks, ctx)
            elif head == 'kill':
                for e in self.select(toks[1], ctx) or []:
                    e.alive = False
                self.entities = [e for e in self.entities if e.alive]
            elif head in ('tp', 'teleport'):
                self.teleport(toks, ctx)
            elif head == 'tag' and len(toks) >= 4:
                for e in self.select(toks[1], ctx) or []:
                    tags = list(e.nbt.get('Tags', []))
                    if toks[2] == 'add' and toks[3] not in tags:
                        tags.append(toks[3])
                    elif toks[2] == 'remove' and toks[3] in tags:
                        tags.remove(toks[3])
                    e.nbt['Tags'] = tags
            elif head == 'function':
                if not self.follow or depth >= self.max_depth:
                    LOG.count('function call not followed (depth)')
                    return
                macros = None
                if len(toks) > 2 and toks[2].startswith('{'):
                    macros = parse_snbt(toks[2])
                elif len(toks) > 2:
                    LOG.count('function ... with <source>: macros unavailable')
                try:
                    self.run_file(toks[1], ctx, macros, depth + 1)
                except FileNotFoundError as ex:
                    LOG.note(str(ex))
            elif head == 'return':
                if len(toks) > 1 and toks[1] == 'run':
                    self.command(' '.join(toks[2:]), ctx, depth)
                raise StopFunction()
            else:
                LOG.count(f'ignored command: {head}')
        except StopFunction:
            raise
        except (ValueError, IndexError, KeyError, SNBTError) as ex:
            LOG.note(f'could not interpret: {line[:140]} ({ex})')

    def execute(self, toks, i, ctx, depth):
        while i < len(toks):
            sub = toks[i]
            if sub == 'run':
                self.command(' '.join(toks[i + 1:]), ctx, depth)
                return
            if sub in ('as', 'at'):
                ents = self.select(toks[i + 1], ctx)
                if ents is None:                      # @s / players: keep current context
                    i += 2
                    continue
                for e in ents:
                    c = ctx.copy()
                    if sub == 'as':
                        c.executor = e
                    else:
                        c.pos, c.yaw, c.pitch = e.pos.copy(), e.yaw, e.pitch
                    self.execute(toks, i + 2, c, depth)
                return
            if sub == 'positioned':
                if toks[i + 1] == 'as':
                    ents = self.select(toks[i + 2], ctx)
                    if ents:
                        ctx.pos = ents[0].pos.copy()
                    i += 3
                elif toks[i + 1] == 'over':
                    i += 3
                else:
                    ctx.pos = self.coords(toks[i + 1:i + 4], ctx)
                    i += 4
                continue
            if sub == 'rotated':
                if toks[i + 1] == 'as':
                    ents = self.select(toks[i + 2], ctx)
                    if ents:
                        ctx.yaw, ctx.pitch = ents[0].yaw, ents[0].pitch
                    i += 3
                else:
                    ctx.yaw = self.rot(toks[i + 1], ctx.yaw)
                    ctx.pitch = self.rot(toks[i + 2], ctx.pitch)
                    i += 3
                continue
            if sub == 'facing':
                i += 4 if toks[i + 1] == 'entity' else 4
                continue
            if sub in ('anchored', 'align', 'in', 'on', 'summon'):
                i += 2
                continue
            if sub in ('if', 'unless'):
                res, n = self.condition(toks, i + 1, ctx)
                if res is None:
                    LOG.count('execute skipped (unknown condition)')
                    return
                if res != (sub == 'if'):
                    return
                i += 1 + n
                continue
            if sub == 'store':
                kind = toks[i + 2]
                i += {'score': 5, 'storage': 7, 'entity': 7, 'block': 9, 'bossbar': 5}.get(kind, 5)
                continue
            LOG.count(f'execute subcommand {sub} unsupported')
            return

    def condition(self, toks, i, ctx):
        kind = toks[i]
        if kind == 'score':
            obj = toks[i + 2]
            key = f'{toks[i + 1]} {obj}'
            val = self.scores.get(key, self.scores.get(obj))
            if toks[i + 3] == 'matches':
                rng = toks[i + 4]
                if val is None:
                    return None, 5
                lo, _, hi = rng.partition('..')
                if '..' not in rng:
                    ok = val == int(rng)
                else:
                    ok = (lo == '' or val >= int(lo)) and (hi == '' or val <= int(hi))
                return ok, 5
            return None, 6
        if kind == 'entity':
            ents = self.select(toks[i + 1], ctx)
            if ents is None:
                return (True if toks[i + 1] == '@s' else None), 2
            return bool(ents), 2
        n = {'block': 5, 'blocks': 9, 'data': 4, 'predicate': 2, 'loaded': 4, 'dimension': 2,
             'biome': 5, 'function': 2, 'items': 4}.get(kind, 2)
        return None, n

    def summon(self, toks, ctx):
        etype = toks[1].replace('minecraft:', '')
        pos = ctx.pos.copy()
        rest = toks[2:]
        if len(rest) >= 3 and not rest[0].startswith('{'):
            pos = self.coords(rest[:3], ctx)
            rest = rest[3:]
        nbt = parse_snbt(rest[0]) if rest else {}
        rot = nbt.get('Rotation', [0, 0])
        e = Entity(etype, pos, float(rot[0]), float(rot[1]), nbt, len(self.entities))
        self.entities.append(e)

    def data(self, toks, ctx):
        if toks[1] == 'merge' and toks[2] == 'entity':
            v = parse_snbt(toks[4])
            for e in self.select(toks[3], ctx) or []:
                deep_merge(e.nbt, v)
                if 'Rotation' in v:
                    e.yaw, e.pitch = float(v['Rotation'][0]), float(v['Rotation'][1])
        elif toks[1] == 'modify' and toks[2] == 'entity':
            path = split_path(toks[4])
            op = toks[5]
            if op not in ('set', 'merge') or toks[6] != 'value':
                LOG.count(f'data modify {op} {toks[6]} ignored')
                return
            v = parse_snbt(' '.join(toks[7:]))
            for e in self.select(toks[3], ctx) or []:
                if path[0] in ('Rotation', 'Pos'):
                    e.nbt.setdefault('Rotation', [e.yaw, e.pitch])
                node = e.nbt
                for j, k in enumerate(path[:-1]):
                    nxt = path[j + 1]
                    if isinstance(k, int):
                        node = node[k]
                    else:
                        if k not in node or not isinstance(node[k], (dict, list)):
                            node[k] = [0] * (nxt + 1) if isinstance(nxt, int) else {}
                        node = node[k]
                last = path[-1]
                if isinstance(last, int):
                    while len(node) <= last:
                        node.append(0)
                    node[last] = json.loads(json.dumps(v))
                elif op == 'merge' and isinstance(node.get(last), dict) and isinstance(v, dict):
                    deep_merge(node[last], v)
                else:
                    node[last] = json.loads(json.dumps(v))
                if path[0] == 'Rotation':
                    e.yaw, e.pitch = float(e.nbt['Rotation'][0]), float(e.nbt['Rotation'][1])
        else:
            LOG.count('data command ignored')

    def teleport(self, toks, ctx):
        args = toks[1:]
        if not args:
            return
        if args[0].startswith('@'):
            targets = self.select(args[0], ctx)
            args = args[1:]
        else:
            targets = [ctx.executor] if ctx.executor is not None else []
        if not targets:
            return
        if len(args) == 1 and args[0].startswith('@'):
            dst = self.select(args[0], ctx)
            if dst:
                for e in targets:
                    e.pos = dst[0].pos.copy()
            return
        if len(args) < 3:
            return
        pos = self.coords(args[:3], ctx)
        for e in targets:
            e.pos = pos.copy()
            if len(args) >= 5 and args[3] != 'facing':
                e.yaw = self.rot(args[3], ctx.yaw)
                e.pitch = self.rot(args[4], ctx.pitch)


def split_args(s):
    out, cur, depth, q = [], [], 0, None
    for c in s:
        if q:
            cur.append(c)
            if c == q:
                q = None
            continue
        if c in '"\'':
            q = c
        elif c in '[{':
            depth += 1
        elif c in ']}':
            depth -= 1
        if c == ',' and depth == 0:
            out.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
    if cur:
        out.append(''.join(cur))
    res = []
    for a in out:
        if '=' in a:
            k, v = a.split('=', 1)
            res.append((k.strip(), v.strip()))
    return res

# ----------------------------------------------------------------------------- geometry


class Geometry:
    """World-space quads of one scene (per view only billboard:center differs)."""

    def __init__(self, scene, assets, hide=(), only=(), translucent=True):
        self.items = []   # (entity, baked, tints, M4 base)
        self.hidden = []
        self.assets = assets
        self.translucent = translucent
        for e in scene.entities:
            if e.etype != 'item_display':
                continue
            tags = e.tags
            name = next((t for t in sorted(tags) if t.startswith('rlk_rd_')), None) or ','.join(sorted(tags)) or f'#{e.idx}'
            if hide and any(any(h in t for t in tags) for h in hide):
                continue
            if only and not any(any(o in t for t in tags) for o in only):
                continue
            mid = e.item_model()
            if not mid:
                LOG.count('item_display without item_model (not rendered)')
                continue
            M = transformation_matrix(e.nbt.get('transformation'))
            det = np.linalg.det(M[:3, :3])
            if abs(det) < 1e-9:
                self.hidden.append(name)
                continue
            for baked, tints in assets.item(mid):
                self.items.append((e, baked, tints, M, name))

    def entity_matrix(self, e, M, view):
        bb = e.nbt.get('billboard', 'fixed')
        if bb == 'fixed' or view is None:
            O = entity_orientation(e.yaw, e.pitch)
        elif bb == 'center':
            O = rot_y(180 - view.yaw) @ rot_x(-view.pitch)
        elif bb == 'vertical':
            O = rot_y(180 - view.yaw)
        else:   # horizontal
            O = rot_y(-e.yaw) @ rot_x(-view.pitch)
        W = np.eye(4)
        W[:3, :3] = O @ M[:3, :3] @ RY180
        W[:3, 3] = O @ M[:3, 3] + e.pos
        return W

    def point(self, tag, model_px, view=None):
        """World position of a model-pixel point on the first entity carrying tag."""
        for e, baked, tints, M, name in self.items:
            if tag in e.tags:
                W = self.entity_matrix(e, M, view)
                p = np.asarray(model_px, float) / 16 - 0.5
                return W[:3, :3] @ p + W[:3, 3], W[:3, :3]
        return None, None

    def quads(self, view):
        V, UV, TEX, TINT, SGN, QN = [], [], [], [], [], []
        for e, baked, tints, M, name in self.items:
            W = self.entity_matrix(e, M, view)
            c = baked['corners'] @ W[:3, :3].T + W[:3, 3]
            V.append(c)
            UV.append(baked['uv'])
            TEX.append(baked['tex'])
            tint = np.ones((len(baked['tex']), 3))
            for k, tv in enumerate(tints):
                tint[baked['tint'] == k] = tv
            TINT.append(tint)
            SGN.append(np.full(len(baked['tex']), 1.0 if np.linalg.det(W[:3, :3]) > 0 else -1.0))
            # (mcq) the normal vanilla lights a baked quad with: its model-space normal snapped to the nearest axis
            # (BakedQuad.direction), carried through the entity transform
            cm = baked['corners']
            if len(cm):
                nm = np.cross(cm[:, 3] - cm[:, 0], cm[:, 1] - cm[:, 0])
                ax = np.abs(nm).argmax(1); ii = np.arange(len(nm))
                ns = np.zeros_like(nm); ns[ii, ax] = np.sign(nm[ii, ax])
                QN.append(ns @ np.linalg.inv(W[:3, :3]))
            else:
                QN.append(np.zeros((0, 3)))
        self._qn = np.concatenate(QN) if QN else np.zeros((0, 3))
        if not V:
            z = np.zeros((0, 4, 3))
            return z, np.zeros((0, 4, 2)), np.zeros(0, int), np.zeros((0, 3)), np.zeros(0)
        return np.concatenate(V), np.concatenate(UV), np.concatenate(TEX), np.concatenate(TINT), np.concatenate(SGN)

# ----------------------------------------------------------------------------- views


class View:
    def __init__(self, name, yaw, pitch, persp=False, pos=None, fov=70.0, label=None):
        self.name = name
        self.yaw = yaw
        self.pitch = pitch
        self.persp = persp
        self.pos = None if pos is None else np.array(pos, float)
        self.fov = fov
        self.label = label or name
        self.f = mc_forward(yaw, pitch)
        self.r = np.array([-math.cos(math.radians(yaw)), 0.0, -math.sin(math.radians(yaw))])
        self.u = np.cross(self.r, self.f)
        # framing (ortho)
        self.center = np.zeros(2)
        self.scale = 1.0

    def cam(self, P):
        """(…,3) world -> (…,3) camera coords X right, Y up, Z depth."""
        Q = P - self.pos if self.persp else P
        return np.stack([Q @ self.r, Q @ self.u, Q @ self.f], axis=-1)

    def screen(self, C, W, H):
        if self.persp:
            focal = (H / 2) / math.tan(math.radians(self.fov) / 2)
            Z = np.maximum(C[..., 2], 1e-6)
            sx = W / 2 + C[..., 0] / Z * focal
            sy = H / 2 - C[..., 1] / Z * focal
        else:
            sx = W / 2 + (C[..., 0] - self.center[0]) * self.scale
            sy = H / 2 - (C[..., 1] - self.center[1]) * self.scale
        return np.stack([sx, sy], axis=-1)

    def axis_words(self):
        def word(v):
            names = [('+X(E)', [1, 0, 0]), ('-X(W)', [-1, 0, 0]), ('+Y(up)', [0, 1, 0]), ('-Y', [0, -1, 0]),
                     ('+Z(S)', [0, 0, 1]), ('-Z(N)', [0, 0, -1])]
            best = max(names, key=lambda n: float(np.dot(v, n[1])))
            return best[0]
        return f'scr-right={word(self.r)} scr-up={word(self.u)}'


def make_views(names, subject_yaw, camera=None, fov=70.0, az=None, el=None):
    F = subject_yaw
    table = {
        'front': (F + 180, 0, 'front (viewer in front, looking at its face)'),
        'back': (F, 0, 'back (viewer behind it)'),
        'left': (F + 90, 0, "left (viewer at subject's LEFT side)"),
        'right': (F - 90, 0, "right (viewer at subject's RIGHT side)"),
        'top': (F + 180, 90, 'top (from above, its front at bottom)'),
        'iso': (F + 180 + 40, 25, 'iso (front-right, 25deg down)'),
        'iso_left': (F + 180 - 40, 25, 'iso_left (front-left, 25deg down)'),
        'below': (F + 180, -60, 'below (front, 60deg up)'),
    }
    views = []
    for n in names:
        n = n.strip()
        if not n:
            continue
        if n in ('camera', 'player'):
            if camera is None:
                LOG.note('view "camera" needs --camera or --camera-preset; skipped')
                continue
            x, y, z, yw, pt = camera
            views.append(View('camera', yw, pt, True, (x, y, z), fov, f'camera @({x + 0:.3g},{y + 0:.3g},{z + 0:.3g}) yaw {yw % 360:g} pitch {pt:g} (rel. origin)'))
        elif n.startswith('cam:'):
            yw, pt = (float(v) for v in n[4:].split(','))
            views.append(View(n, yw, pt, label=f'ortho cam yaw {yw:g} pitch {pt:g}'))
        elif n.startswith('az:'):
            a, e = (float(v) for v in n[3:].split(','))
            views.append(View(n, F + 180 + a, e, label=f'az {a:g} (from front, + toward its right) el {e:g}'))
        elif n in table:
            yw, pt, lab = table[n]
            views.append(View(n, yw, pt, label=lab))
        else:
            raise SystemExit(f'unknown view {n!r}; use front,back,left,right,top,iso,iso_left,below,camera,cam:YAW,PITCH,az:A,E')
    if az is not None:
        views.append(View('custom', F + 180 + az, el or 0, label=f'az {az:g} el {el or 0:g}'))
    return views

# ----------------------------------------------------------------------------- raster

BUCKETS = (1, 2, 4, 8, 16, 32, 64, 128)


def rasterize(S, Z, persp, W, H, eps=1e-7, budget=3_000_000):
    """S (T,3,2) screen coords, Z (T,3) depth.  Returns tri, pix, depth, b0, b1, b2."""
    T = len(S)
    if T == 0:
        e = np.zeros(0)
        return np.zeros(0, int), np.zeros(0, int), e, e, e, e
    x0, y0, x1, y1, x2, y2 = S[:, 0, 0], S[:, 0, 1], S[:, 1, 0], S[:, 1, 1], S[:, 2, 0], S[:, 2, 1]
    area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    minx, maxx = S[:, :, 0].min(1), S[:, :, 0].max(1)
    miny, maxy = S[:, :, 1].min(1), S[:, :, 1].max(1)
    ix0 = np.maximum(np.ceil(minx - 0.5), 0).astype(np.int64)
    ix1 = np.minimum(np.floor(maxx - 0.5), W - 1).astype(np.int64)
    iy0 = np.maximum(np.ceil(miny - 0.5), 0).astype(np.int64)
    iy1 = np.minimum(np.floor(maxy - 0.5), H - 1).astype(np.int64)
    nx, ny = ix1 - ix0 + 1, iy1 - iy0 + 1
    ok = (np.abs(area) > 1e-10) & (nx > 0) & (ny > 0)
    K = np.maximum(nx, ny)
    outs = []
    prev = 0
    groups = [(b, np.nonzero(ok & (K > prev_b) & (K <= b))[0]) for prev_b, b in zip((0,) + BUCKETS[:-1], BUCKETS)]
    big = np.nonzero(ok & (K > BUCKETS[-1]))[0]
    groups += [(int(K[t]), np.array([t])) for t in big]
    for kb, idx in groups:
        if len(idx) == 0:
            continue
        g = np.arange(kb)
        per = kb * kb
        step = max(1, budget // per)
        for s in range(0, len(idx), step):
            ti = idx[s:s + step]
            PX = ix0[ti][:, None, None] + g[None, None, :]
            PY = iy0[ti][:, None, None] + g[None, :, None]
            valid = (PX <= ix1[ti][:, None, None]) & (PY <= iy1[ti][:, None, None])
            cx, cy = PX + 0.5, PY + 0.5
            a = area[ti][:, None, None]
            X0, Y0 = x0[ti][:, None, None], y0[ti][:, None, None]
            X1, Y1 = x1[ti][:, None, None], y1[ti][:, None, None]
            X2, Y2 = x2[ti][:, None, None], y2[ti][:, None, None]
            w0 = ((X1 - cx) * (Y2 - cy) - (X2 - cx) * (Y1 - cy)) / a
            w1 = ((X2 - cx) * (Y0 - cy) - (X0 - cx) * (Y2 - cy)) / a
            w2 = 1 - w0 - w1
            inside = valid & (w0 >= -eps) & (w1 >= -eps) & (w2 >= -eps)
            a_i, b_i, c_i = np.nonzero(inside)
            if len(a_i) == 0:
                continue
            tri = ti[a_i]
            px = PX[a_i, 0, c_i]
            py = PY[a_i, b_i, 0]
            W0, W1, W2 = w0[a_i, b_i, c_i], w1[a_i, b_i, c_i], w2[a_i, b_i, c_i]
            z0, z1, z2 = Z[tri, 0], Z[tri, 1], Z[tri, 2]
            if persp:
                iz = W0 / z0 + W1 / z1 + W2 / z2
                depth = 1 / iz
                B0, B1, B2 = W0 / z0 * depth, W1 / z1 * depth, W2 / z2 * depth
            else:
                depth = W0 * z0 + W1 * z1 + W2 * z2
                B0, B1, B2 = W0, W1, W2
            outs.append((tri, py * W + px, depth, B0, B1, B2))
    if not outs:
        e = np.zeros(0)
        return np.zeros(0, int), np.zeros(0, int), e, e, e, e
    return tuple(np.concatenate([o[k] for o in outs]) for k in range(6))


MC_LIGHT0 = norm(np.array([0.2, 1.0, -0.7]))
MC_LIGHT1 = norm(np.array([-0.2, 1.0, 0.7]))


def floor_quad(assets, opts, view=None):
    """Opaque ground plane at y=0 (relative to the origin), e.g. the arena's light_gray_concrete."""
    rgb = tuple(int(v) for v in opts.floor.split(','))
    SPECIAL_TEXTURES['rlk:__floor__'] = (*rgb, 255)
    t = assets.texture('rlk:__floor__')
    h = opts.floor_half
    g = np.arange(-h, h, 2.0)          # 2-block tiles so perspective near-plane culling only drops tiles behind the eye
    X, Z = np.meshgrid(g, g)
    X, Z = X.ravel(), Z.ravel()
    S = np.full(len(X), 2.0)
    if view is not None and view.persp:
        # 0.25-block tiles in a 6x6 patch under the eye (no near-plane hole at the bottom of the frame)
        fx, fz = 2 * np.floor(view.pos[0] / 2) - 2, 2 * np.floor(view.pos[2] / 2) - 2
        far = ~((X >= fx) & (X < fx + 6) & (Z >= fz) & (Z < fz + 6))
        X, Z, S = X[far], Z[far], S[far]
        f = np.arange(0, 6, 0.25)
        FX, FZ = np.meshgrid(fx + f, fz + f)
        X, Z = np.r_[X, FX.ravel()], np.r_[Z, FZ.ravel()]
        S = np.r_[S, np.full(FX.size, 0.25)]
    O = np.zeros_like(X)
    V = np.stack([np.stack([X, O, Z], 1), np.stack([X + S, O, Z], 1),
                  np.stack([X + S, O, Z + S], 1), np.stack([X, O, Z + S], 1)], 1)
    k = len(V)
    return V, np.zeros((k, 4, 2)), np.full(k, t), np.ones((k, 3)), np.ones(k)


NEAR = 0.05


def clip_near(TC, TUV, tq):
    """Clip camera-space triangles against z = NEAR (Sutherland-Hodgman), carrying UVs."""
    z = TC[:, :, 2]
    inside = z > NEAR
    n_in = inside.sum(1)
    keep = n_in == 3
    outC, outU, outQ = [TC[keep]], [TUV[keep]], [tq[keep]]
    for t in np.nonzero((n_in > 0) & (n_in < 3))[0]:
        poly_c, poly_u = [], []
        for k in range(3):
            a, b = k, (k + 1) % 3
            za, zb = z[t, a], z[t, b]
            if za > NEAR:
                poly_c.append(TC[t, a]); poly_u.append(TUV[t, a])
            if (za > NEAR) != (zb > NEAR):
                f = (NEAR - za) / (zb - za)
                poly_c.append(TC[t, a] + (TC[t, b] - TC[t, a]) * f)
                poly_u.append(TUV[t, a] + (TUV[t, b] - TUV[t, a]) * f)
        for k in range(1, len(poly_c) - 1):
            outC.append(np.array([[poly_c[0], poly_c[k], poly_c[k + 1]]]))
            outU.append(np.array([[poly_u[0], poly_u[k], poly_u[k + 1]]]))
            outQ.append(np.array([tq[t]]))
    return np.concatenate(outC), np.concatenate(outU), np.concatenate(outQ)


def render_view(geo, view, W, H, opts, assets, lines3d=()):
    V, UV, TEX, TINT, SGN = geo.quads(view)
    if getattr(opts, 'floor', None):
        fV, fUV, fT, fTi, fS = floor_quad(assets, opts, view)
        V, UV, TEX, TINT, SGN = (np.concatenate([a, b]) for a, b in ((V, fV), (UV, fUV), (TEX, fT), (TINT, fTi), (SGN, fS)))
    C = view.cam(V.reshape(-1, 3)).reshape(V.shape)
    S = view.screen(C, W, H)
    color = np.empty((H * W, 3))
    yy = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    bg0, bg1 = np.array(opts.bg_top) / 255, np.array(opts.bg_bottom) / 255
    color[:] = (bg0[None, :] * (1 - yy.reshape(-1, 1)) + bg1[None, :] * yy.reshape(-1, 1))
    zbuf = np.full(H * W, np.inf)
    if len(V):
        n = np.cross(V[:, 3] - V[:, 0], V[:, 1] - V[:, 0]) * SGN[:, None]
        nl = np.linalg.norm(n, axis=1)
        keep = nl > 1e-12
        n = n / np.maximum(nl, 1e-12)[:, None]
        if view.persp:
            keep &= C[:, :, 2].max(1) > NEAR      # partly-behind quads are clipped below
            to_face = V.mean(1) - view.pos
            keep &= np.einsum('ij,ij->i', n, to_face) < 0
        else:
            keep &= (n @ view.f) < 0
        if getattr(opts, 'tex_mode', 'uv') == 'avg':
            uni = np.array(assets.tex_avg) if assets.tex_avg else np.zeros((0, 4))
        else:
            uni = np.array([u if u is not None else [np.nan] * 4 for u in assets.tex_uniform]) if assets.tex_uniform else np.zeros((0, 4))
        qcol = uni[TEX] if len(uni) else np.zeros((len(TEX), 4))
        kinds = np.array([k == 'translucent' for k in assets.tex_kind], bool)
        qtrans = kinds[TEX] if len(kinds) else np.zeros(len(TEX), bool)
        if not opts.translucent:
            keep &= ~qtrans
        light_mode = 'flat' if opts.flat else getattr(opts, 'light', 'view')
        if light_mode == 'flat':
            shade = np.ones(len(V))
        elif light_mode == 'mcq':
            # as mc, but each quad lit by its axis-snapped baked normal (vanilla): a face turned 22.5 deg in its model
            # keeps the light of its axis
            qn = getattr(geo, '_qn', None)
            m = np.array(n)
            if qn is not None and len(qn):
                k = min(len(qn), len(n)); q = qn[:k] / np.maximum(np.linalg.norm(qn[:k], axis=1), 1e-12)[:, None]
                q *= np.where(np.einsum('ij,ij->i', q, n[:k]) < 0, -1.0, 1.0)[:, None]
                m[:k] = q
            shade = np.minimum(1.0, 0.6 * (np.clip(m @ MC_LIGHT0, 0, None) + np.clip(m @ MC_LIGHT1, 0, None)) + 0.4)
        elif light_mode == 'mc':
            # vanilla entity/item diffuse lighting (overworld): world-fixed lights, ambient 0.4
            shade = np.minimum(1.0, 0.6 * (np.clip(n @ MC_LIGHT0, 0, None) + np.clip(n @ MC_LIGHT1, 0, None)) + 0.4)
        else:
            light = norm(-0.35 * view.r + 0.75 * view.u - 0.55 * view.f)
            shade = 0.42 + 0.58 * np.clip(n @ light, 0, 1)
        sel = np.nonzero(keep)[0]
        tri_q = np.concatenate([sel, sel])
        tri_v = np.concatenate([np.tile([0, 1, 2], (len(sel), 1)), np.tile([0, 2, 3], (len(sel), 1))])
        TC = C[tri_q[:, None], tri_v]                 # (T,3,3) camera-space vertices
        TUV = UV[tri_q[:, None], tri_v]               # (T,3,2)
        if view.persp:
            TC, TUV, tri_q = clip_near(TC, TUV, tri_q)
        St = view.screen(TC, W, H)
        Zt = TC[:, :, 2]
        tri, pix, depth, b0, b1, b2 = rasterize(St, Zt, view.persp, W, H)
        q = tri_q[tri]
        rgba = qcol[q].copy()
        texd = np.isnan(rgba[:, 0])
        if texd.any():
            tt = tri[texd]
            qq = q[texd]
            uv = (TUV[tt, 0] * b0[texd, None] + TUV[tt, 1] * b1[texd, None] + TUV[tt, 2] * b2[texd, None])
            sub = np.zeros((len(qq), 4))
            for t_id in np.unique(TEX[qq]):
                arr = assets.tex_arrays[t_id]
                m = TEX[qq] == t_id
                h, w = arr.shape[:2]
                ux = np.clip((uv[m, 0] * w).astype(int), 0, w - 1)
                vy = np.clip((uv[m, 1] * h).astype(int), 0, h - 1)
                sub[m] = arr[vy, ux]
            rgba[texd] = sub
        rgba[:, :3] *= TINT[q] * shade[q][:, None]
        alpha = rgba[:, 3]
        cut = getattr(opts, 'alpha_cutout', 0.1)
        live = alpha >= cut if cut > 0 else alpha > 0.02
        blend = getattr(opts, 'blend', 'mc')
        if blend == 'mc':
            # sprites with partial alpha go to the translucent item sheet as a whole
            opaque = live & ~qtrans[q]
        else:
            opaque = live & (alpha >= 0.999)
        # opaque resolve
        oi = np.nonzero(opaque)[0]
        if len(oi):
            order = np.lexsort((depth[oi], pix[oi]))
            oi = oi[order]
            _, first = np.unique(pix[oi], return_index=True)
            win = oi[first]
            zbuf[pix[win]] = depth[win]
            color[pix[win]] = rgba[win, :3]
        # translucent composite (front-to-back over operator, depth-tested vs opaque)
        ti = np.nonzero(live & ~opaque)[0]
        if len(ti):
            ti = ti[depth[ti] < zbuf[pix[ti]] - 1e-6]
        if len(ti) and blend == 'mc':
            # Vanilla: translucent quads sorted back-to-front by centroid distance, drawn with
            # depth test LEQUAL AND depth write, so a nearer quad drawn earlier hides later ones.
            cen = V.mean(1)
            if view.persp:
                qd = np.linalg.norm(cen - view.pos, axis=1)
            else:
                qd = cen @ view.f
            rank = np.empty(len(V), np.int64)
            rank[np.lexsort((np.arange(len(V)), -qd))] = np.arange(len(V))
            r_t = rank[q[ti]]
            order = np.lexsort((r_t, pix[ti]))
            ti = ti[order]
            p = pix[ti]
            d = depth[ti]
            starts = np.r_[0, np.nonzero(np.diff(p))[0] + 1]
            grp = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(p)]))
            span = float(d.max() - d.min()) + 10.0
            run = np.minimum.accumulate(d - grp * span) + grp * span       # inclusive running min
            prev = np.r_[np.inf, run[:-1]]
            prev[starts] = np.inf
            drawn = d <= prev + 1e-9
            ti, p, grp = ti[drawn], p[drawn], grp[drawn]
            if len(ti):
                starts = np.r_[0, np.nonzero(np.diff(p))[0] + 1]
                grp = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(p)]))
                a = np.clip(alpha[ti] * opts.alpha_scale, 0, 1.0)
                la = np.log(np.maximum(1 - a, 1e-12))
                # transmittance of everything drawn AFTER (in front of) each fragment
                rc = np.cumsum(la[::-1])[::-1]                      # suffix sums incl. self
                ends = np.r_[starts[1:], len(p)] - 1
                tail = np.zeros(len(starts))                         # suffix sum beyond each group
                tail[:-1] = rc[ends[:-1] + 1]
                after = rc - la - tail[grp]
                contrib = rgba[ti, :3] * (a * np.exp(after))[:, None]
                up = p[starts]
                total = np.zeros(len(starts))
                np.add.at(total, grp, la)
                acc = np.zeros((len(starts), 3))
                np.add.at(acc, grp, contrib)
                color[up] = color[up] * np.exp(total)[:, None] + acc
            ti = ti[:0]
        if len(ti):
            order = np.lexsort((depth[ti], pix[ti]))
            ti = ti[order]
            p = pix[ti]
            a = np.clip(alpha[ti] * opts.alpha_scale, 0, 0.995)
            la = np.log1p(-a)
            cum = np.cumsum(la)
            starts = np.r_[0, np.nonzero(np.diff(p))[0] + 1]
            grp = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(p)]))
            before = cum - la - (cum[starts] - la[starts])[grp]
            contrib = rgba[ti, :3] * (a * np.exp(before))[:, None]
            up = p[starts]
            total = np.zeros(len(starts))
            np.add.at(total, grp, la)
            acc = np.zeros((len(starts), 3))
            np.add.at(acc, grp, contrib)
            color[up] = color[up] * np.exp(total)[:, None] + acc
    img = color.reshape(H, W, 3)
    zimg = zbuf.reshape(H, W)
    for pts, rgb, width, occluded_rgb in lines3d:
        draw_polyline3d(img, zimg, view, pts, rgb, width, occluded_rgb, W, H)
    return np.clip(img, 0, 1), zimg


def draw_polyline3d(img, zimg, view, pts, rgb, width, occluded_rgb, W, H):
    pts = np.asarray(pts, float)
    if len(pts) < 2:
        return
    C = view.cam(pts)
    S = view.screen(C, W, H)
    samples_s, samples_z = [], []
    for k in range(len(pts) - 1):
        if view.persp and (C[k, 2] < 0.05 or C[k + 1, 2] < 0.05):
            continue
        seg = np.linalg.norm(S[k + 1] - S[k])
        n = int(min(max(2, seg * 1.5), 20000))
        t = np.linspace(0, 1, n)[:, None]
        if view.persp:
            iz = (1 - t) / C[k, 2] + t / C[k + 1, 2]
            z = 1 / iz[:, 0]
            tt = (t[:, 0] / C[k + 1, 2]) * z
            P3 = C[k] * (1 - tt[:, None]) + C[k + 1] * tt[:, None]
            samples_s.append(view.screen(P3, W, H))
            samples_z.append(P3[:, 2])
        else:
            samples_s.append(S[k] * (1 - t) + S[k + 1] * t)
            samples_z.append(C[k, 2] * (1 - t[:, 0]) + C[k + 1, 2] * t[:, 0])
    if not samples_s:
        return
    Ss = np.concatenate(samples_s)
    Zs = np.concatenate(samples_z)
    r = max(0, int(width) // 2)
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            px = np.floor(Ss[:, 0]).astype(int) + dx
            py = np.floor(Ss[:, 1]).astype(int) + dy
            m = (px >= 0) & (px < W) & (py >= 0) & (py < H)
            px, py, z = px[m], py[m], Zs[m]
            vis = z <= zimg[py, px] + 0.02
            img[py[vis], px[vis]] = np.array(rgb) / 255
            if occluded_rgb is not None:
                img[py[~vis], px[~vis]] = np.array(occluded_rgb) / 255

# ----------------------------------------------------------------------------- runner


def parse_strip(s):
    m = re.match(r'^(-?\d+)\.\.(-?\d+)(?::(\d+))?$', s)
    if not m:
        raise SystemExit('--strip expects a..b or a..b:step')
    a, b, st = int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
    return list(range(a, b + 1, st))


def phase_name(p):
    if str(p).isdigit():
        return PHASES[int(p)]
    if p in PHASES.values():
        return p
    raise SystemExit(f'phase must be 0-3 or one of {list(PHASES.values())}')


class Job:
    """Builds the scene for a tick."""

    def __init__(self, args):
        self.args = args
        self.dp = Path(args.dp)
        self.mode = 'generic'
        self.subject_yaw = args.yaw
        if args.rig:
            self.mode = 'rig'
            self.phase = phase_name(args.rig[0])
            self.clip = args.rig[1]
            self.tick0 = int(args.rig[2]) if args.rig[2].lstrip('-').isdigit() else 0
            self.origin = args.origin or (0, 0, 0)
        elif args.judgment is not None:
            self.mode = 'judgment'
            self.tick0 = args.judgment
            self.origin = args.origin or (0, 201, 0)
            self.subject_yaw = args.yaw
        elif args.item:
            self.mode = 'item'
            self.tick0 = 0
            self.origin = args.origin or (0, 0, 0)
        else:
            self.mode = 'generic'
            self.tick0 = 0
            self.origin = args.origin or (0, 0, 0)
            if not args.spawn and not args.apply:
                raise SystemExit('nothing to render: use --rig, --judgment, --spawn/--apply or --item')

    def scene(self, tick):
        a = self.args
        scores = dict(a.score_map)
        sc = Scene(self.dp, self.origin, scores=scores, macros=a.macro_map, max_depth=a.depth, follow=not a.no_follow)
        ctx = Ctx((0, 0, 0), a.yaw, 0.0)
        if self.mode == 'rig':
            base = 'rlk:boss/raiden/rig/'
            sc.run_file(base + 'spawn', ctx)
            sc.run_file(base + f'select/{self.clip}', ctx)
            pose = f'{base}poses/{self.phase}/{self.clip}/{tick}'
            clipf = self.dp / f'data/rlk/function/boss/raiden/rig/clip/{self.clip}.mcfunction'
            if clipf.exists():
                played = [int(x) for x in re.findall(rf'rdPhase matches {"0123"[list(PHASES.values()).index(self.phase)]} if score @s rdRigT matches (\d+) ', clipf.read_text())]
                if played and tick > max(played):
                    LOG.note(f'tick {tick} > last dispatched tick {max(played)} of clip {self.clip}: stale pose file, never played in game')
            try:
                sc.run_file(pose, ctx)
            except FileNotFoundError:
                d = self.dp / 'data/rlk/function/boss/raiden/rig/poses' / self.phase / self.clip
                have = sorted(int(p.stem) for p in d.glob('*.mcfunction')) if d.exists() else []
                raise SystemExit(f'no pose file {pose}; available ticks: {have[:1]}..{have[-1:]}' if have else
                                 f'no clip {self.clip!r} for phase {self.phase}; clips: ' +
                                 ', '.join(sorted(p.name for p in (d.parent).iterdir())) if d.parent.exists() else 'none')
        elif self.mode == 'judgment':
            base = 'rlk:boss/raiden/judgment_rig/'
            sc.run_file(base + 'start', ctx)
            ft = tick - a.frame_offset
            if ft >= 0:
                try:
                    sc.run_file(f'{base}frame/{ft}', ctx)
                except FileNotFoundError:
                    raise SystemExit(f'no judgment frame/{ft}')
        elif self.mode == 'item':
            for k, mid in enumerate(a.item):
                sc.entities.append(Entity('item_display', (k * a.item_spacing, 0, 0), a.yaw, 0.0,
                                          {'Tags': [f'item_{k}'], 'item': {'components': {'minecraft:item_model': mid}},
                                           'transformation': {'translation': [0, 0, 0], 'left_rotation': [0, 0, 0, 1],
                                                              'scale': [a.item_scale] * 3, 'right_rotation': [0, 0, 0, 1] if not a.item_cancel_flip else [0, 1, 0, 0]}},
                                          k))
        for f in a.spawn or []:
            sc.run_file(f.replace('{t}', str(tick)), ctx)
        for f in a.apply or []:
            f = f.replace('{t}', str(tick))
            if a.as_tag:
                for e in [e for e in sc.entities if a.as_tag in e.tags and e.alive]:
                    sc.run_file(f, Ctx(e.pos, e.yaw, e.pitch, executor=e))
            else:
                sc.run_file(f, ctx)
        return sc

    def overlays(self):
        """3D guide lines: (points, rgb, width, occluded_rgb)."""
        a = self.args
        out = []
        if a.no_grid:
            return out
        half, step = a.grid if a.grid else ((24, 2) if self.mode == 'judgment' else (4, 1))
        g = np.arange(-half, half + 1e-9, step)
        for v in g:
            col = (92, 96, 110) if abs(v) > 1e-9 else (130, 136, 150)
            out.append(([[v, 0, -half], [v, 0, half]], col, 1, None))
            out.append(([[-half, 0, v], [half, 0, v]], col, 1, None))
        # world axes on the ground
        out.append(([[0, 0.01, 0], [1.0, 0.01, 0]], (230, 70, 70), 2, (120, 50, 50)))
        out.append(([[0, 0.01, 0], [0, 0.01, 1.0]], (70, 120, 240), 2, (40, 60, 120)))
        # subject facing arrow
        f = mc_forward(self.subject_yaw)
        side = np.array([f[2], 0, -f[0]])
        L = 1.6 if self.mode != 'judgment' else 4
        tip = f * L + [0, 0.02, 0]
        out.append(([[0, 0.02, 0], tip], (255, 170, 40), 3, (140, 95, 30)))
        out.append(([tip, tip - f * 0.3 * L / 1.6 + side * 0.18 * L / 1.6], (255, 170, 40), 3, (140, 95, 30)))
        out.append(([tip, tip - f * 0.3 * L / 1.6 - side * 0.18 * L / 1.6], (255, 170, 40), 3, (140, 95, 30)))
        if self.mode == 'judgment':
            out.append((circle((0, 0, 3), 4.0), (80, 220, 255), 2, (40, 110, 130)))      # flower dome
            out.append((circle((0, 0, 0), 23.0), (170, 150, 120), 2, (90, 80, 60)))     # arena edge
            out.append(([[0, 0, 3], [0, 1.2, 3]], (255, 120, 220), 4, (130, 60, 110)))   # flower
            out.append(([[0, 0, -8], [0, 2.4, -8]], (200, 200, 200), 3, (100, 100, 100)))  # hidden boss
        for spec in a.circle or []:
            x, y, z, r = (float(v) for v in spec.split(','))
            out.append((circle((x, y, z), r), (120, 255, 160), 2, (60, 120, 80)))
        for spec in a.marker or []:
            parts = spec.split(',')
            x, y, z = (float(v) for v in parts[:3])
            out.append(([[x, y, z], [x, y + 0.6, z]], (120, 255, 160), 4, (60, 120, 80)))
        return out

    def labels3d(self):
        out = []
        if self.mode == 'judgment':
            out += [((0, 1.4, 3), 'flower+dome r4'), ((0, 2.6, -8), 'boss (hidden)'), ((0, 3, 13), 'player cam')]
        for spec in self.args.marker or []:
            parts = spec.split(',')
            if len(parts) > 3:
                out.append(((float(parts[0]), float(parts[1]) + 0.7, float(parts[2])), parts[3]))
        return out


def circle(c, r, n=96):
    t = np.linspace(0, 2 * math.pi, n + 1)
    return np.stack([c[0] + r * np.cos(t), np.full_like(t, c[1] + 0.01), c[2] + r * np.sin(t)], 1)


def load_font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/freefont/FreeSans.ttf'):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit_views(views, geos, W, H, args):
    for v in views:
        if v.persp:
            continue
        if args.extent:
            v.scale = min(W, H) / (2 * args.extent)
            c = np.array(args.center or (0, 0, 0), float)
            v.center = v.cam(c)[:2]
            continue
        pts = []
        for g in geos:
            Vq = g.quads(v)[0]
            if len(Vq):
                pts.append(v.cam(Vq.reshape(-1, 3))[:, :2])
        if args.center:
            pts.append(v.cam(np.array([args.center], float))[:, :2])
        if not pts:
            v.scale, v.center = min(W, H) / 8, np.zeros(2)
            continue
        P = np.concatenate(pts)
        lo, hi = P.min(0), P.max(0)
        size = np.maximum(hi - lo, 0.5)
        bar = 30 * max(1, args.ss)          # label bar height in render pixels
        v.scale = min(W * 0.9 / size[0], (H - bar) * 0.9 / size[1]) * args.zoom
        v.center = (lo + hi) / 2 + np.array([0, bar / 2 / v.scale])


def draw_gizmo(d, view, x, y, font):
    L = 22
    for vec, col, name in (([1, 0, 0], (235, 80, 80), 'X'), ([0, 1, 0], (90, 220, 90), 'Y'), ([0, 0, 1], (90, 140, 255), 'Z')):
        v = np.array(vec, float)
        sx, sy = float(v @ view.r), float(v @ view.u)
        ex, ey = x + sx * L, y - sy * L
        d.line([(x, y), (ex, ey)], fill=col, width=2)
        if abs(sx) + abs(sy) > 0.15:
            d.text((ex + 2 * np.sign(sx) - 3, ey - 7 - 3 * np.sign(sy)), name, fill=col, font=font)
        else:
            d.text((x + 3, y + 2), name + ('.' if float(v @ view.f) > 0 else 'o'), fill=col, font=font)


def track_points(job, args, ticks_all, view_list):
    """Returns {spec: [(tick, world, axes3x3 or None)]}"""
    res = {}
    for spec in args.track or []:
        tag, rest = spec.split(':', 1)
        coords = [float(v) for v in rest.split(':')[0].split(',')]
        rows = []
        for t in ticks_all:
            g = Geometry(job.scene(t), ASSETS, translucent=True)
            p, A = g.point(tag, coords)
            rows.append((t, p, A))
        res[spec] = rows
    return res


def print_tracks(tracks, views, W, H):
    for spec, rows in tracks.items():
        print(f'\n== track {spec}  (world coords relative to origin; screen +x right, +y up)')
        names = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
        for i, (t, p, A) in enumerate(rows):
            if p is None:
                print(f't={t:4d}  (entity missing or hidden)')
                continue
            prev = rows[i - 1][1] if i > 0 else None
            nxt = rows[i + 1][1] if i + 1 < len(rows) else None
            vel = None
            if prev is not None and nxt is not None:
                vel = (nxt - prev) / 2
            elif nxt is not None:
                vel = nxt - p
            elif prev is not None:
                vel = p - prev
            s = f't={t:4d}  pos=({p[0]:7.2f},{p[1]:7.2f},{p[2]:7.2f})'
            for v in views:
                C = v.cam(p[None])[0]
                if v.persp:
                    sx, sy = v.screen(C[None], W, H)[0]
                    s += f'  [{v.name}] scr=({sx / W * 2 - 1:+.2f},{1 - sy / H * 2:+.2f})'
                else:
                    s += f'  [{v.name}] ({C[0]:+6.2f},{C[1]:+6.2f})'
            if vel is not None and np.linalg.norm(vel) > 1e-6:
                vu = vel / np.linalg.norm(vel)
                s += f'  |v|={np.linalg.norm(vel):5.2f}/tick'
                if A is not None:
                    dirs = [A[:, 0], -A[:, 0], A[:, 1], -A[:, 1], A[:, 2], -A[:, 2]]
                    dots = [float(norm(dv) @ vu) for dv in dirs]
                    k = int(np.argmax(dots))
                    s += f'  lead=model{names[k]}({dots[k]:+.2f})'
                for v in views[:1]:
                    if v.persp:
                        C1 = v.cam((p + vel * 0.05)[None])[0]
                        a0 = v.screen(v.cam(p[None]), W, H)[0]
                        a1 = v.screen(C1[None], W, H)[0]
                        dv = a1 - a0
                        s += f'  scr-dir=({dv[0]:+.2f},{-dv[1]:+.2f})'
                    else:
                        s += f'  scr-dir=({vu @ v.r:+.2f},{vu @ v.u:+.2f})'
            print(s)
            if A is not None and getattr(ARGS, 'track_axes', False):
                for k, nm in enumerate(['+X', '+Y', '+Z']):
                    dv = norm(A[:, k])
                    print(f'          model{nm} -> world ({dv[0]:+.2f},{dv[1]:+.2f},{dv[2]:+.2f})')


ASSETS = None
ARGS = None


def main(argv=None):
    global ASSETS, ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dp', default=str(DEFAULT_DP), help='datapack root containing data/ (default: live roguelike)')
    ap.add_argument('--rp', action='append', help='resource pack root(s) with assets/; repeat to layer (first wins). default: scratch rp')
    ap.add_argument('--skin', help='real 64x64 player-skin PNG for rlk:raiden/skin (else procedural stand-in)')
    ap.add_argument('--rig', nargs=3, metavar=('PHASE', 'CLIP', 'TICK'))
    ap.add_argument('--judgment', type=int, metavar='TICK', help='final-calamity rig at rdTime TICK')
    ap.add_argument('--frame-offset', type=int, default=1, help='judgment: apply frame/(TICK-offset); frame/N carries pose(N+1) (default 1)')
    ap.add_argument('--spawn', nargs='+', help='function files run first (summons)')
    ap.add_argument('--apply', nargs='+', help='function files run after spawn (data merge/modify)')
    ap.add_argument('--as', dest='as_tag', help='run --apply files as (and at) every entity carrying this exact tag (@s = that entity)')
    ap.add_argument('--item', action='append', help='render an item model id raw at the origin (repeatable)')
    ap.add_argument('--item-scale', type=float, default=1.0)
    ap.add_argument('--item-spacing', type=float, default=1.5)
    ap.add_argument('--item-cancel-flip', action='store_true', help='--item: use right_rotation [0,1,0,0] (show model axes as authored)')
    ap.add_argument('--origin', nargs=3, type=float, help='world coords of the execution point ~ ~ ~ (judgment default 0 201 0)')
    ap.add_argument('--yaw', type=float, default=0.0, help='executor/boss yaw (rig parts are tp-ed with it). 0 = faces +Z south')
    ap.add_argument('--score', action='append', default=[], help='OBJ=VAL or "TARGET OBJ=VAL" used by execute if score')
    ap.add_argument('--macro', action='append', default=[], help='KEY=VALUE for $(KEY) macro lines')
    ap.add_argument('--depth', type=int, default=4, help='max nested function depth to follow')
    ap.add_argument('--no-follow', action='store_true', help='do not follow function calls')
    ap.add_argument('--views', default=None, help='comma list: front,back,left,right,top,iso,iso_left,below,camera,cam:YAW,PITCH,az:A,E')
    ap.add_argument('--az', type=float, help='extra view: azimuth from front (+ toward subject right)')
    ap.add_argument('--el', type=float, help='extra view elevation (deg down)')
    ap.add_argument('--camera', nargs=5, type=float, metavar=('X', 'Y', 'Z', 'YAW', 'PITCH'), help='perspective camera, WORLD coords (MC yaw/pitch)')
    ap.add_argument('--camera-preset', choices=['judgment', 'player-front'],
                    help='judgment = locked final-calamity player camera, eye (0,204,13) world = arena centre +(0,3,13), yaw 180 pitch -10; '
                         'player-front = eye 1.62 high, --camera-dist blocks in front of the subject, looking back at it')
    ap.add_argument('--camera-dist', type=float, default=7.0)
    ap.add_argument('--fov', type=float, default=70.0, help='vertical FOV for camera view (MC default 70)')
    ap.add_argument('--strip', help='a..b[:step] ticks, one panel per tick (per view)')
    ap.add_argument('--track', action='append', help='TAG:x,y,z  model-pixel point on entity with TAG; prints path + leading model axis, draws path')
    ap.add_argument('--track-axes', action='store_true', help='also print model axes in world for tracked entities')
    ap.add_argument('--track-range', help='a..b ticks used for the printed track table (default = strip range, every tick)')
    ap.add_argument('--held', action='append', default=[],
                    help='hand-prop check: entities whose tags contain this substring get a magenta arrow along their model +Y '
                         '(the business end: blade / spear tip / stick head) and a printed fwd/up/right table in the subject frame; '
                         'a business end pointing behind the grip is flagged REVERSED? (see HELD PROPS in the module doc)')
    ap.add_argument('--hide', action='append', default=[], help='hide entities whose tags contain this substring')
    ap.add_argument('--only', action='append', default=[], help='render only entities whose tags contain this substring')
    ap.add_argument('--no-translucent', dest='translucent', action='store_false', help='hide faces whose texture alpha < 255')
    ap.add_argument('--alpha-scale', type=float, default=1.0, help='multiply translucent alpha (e.g. 2 to exaggerate)')
    ap.add_argument('--flat', action='store_true', help='no shading at all (same as --light flat)')
    ap.add_argument('--light', choices=['view', 'mc', 'mcq', 'flat'], default='view',
                    help='view = soft view-relative lambert (default); mc = vanilla item/entity diffuse lighting '
                         '(world lights (0.2,1,-0.7),(-0.2,1,0.7), ambient 0.4: up 1.0, N/S 0.74, E/W 0.5, down 0.4); flat = none')
    ap.add_argument('--tex-mode', choices=['uv', 'avg'], default='uv',
                    help='uv = nearest-neighbour texel sampling with face uv/rotation (default); avg = one average colour per texture')
    ap.add_argument('--blend', choices=['mc', 'exact'], default='mc',
                    help='mc = vanilla translucent item sheet: per-quad back-to-front centroid sort with depth write (default); '
                         'exact = per-pixel sorted order-independent compositing')
    ap.add_argument('--alpha-cutout', type=float, default=0.1,
                    help='discard fragments with alpha below this (vanilla item_entity shaders: 0.1). 0 = keep all > 0.02')
    ap.add_argument('--floor', nargs='?', const='125,125,115', default=None,
                    help='draw an opaque floor at y=0 (default colour 125,125,115 = light_gray_concrete, the arena floor)')
    ap.add_argument('--floor-half', type=float, default=40.0)
    ap.add_argument('--grid', nargs=2, type=float, metavar=('HALF', 'STEP'))
    ap.add_argument('--no-grid', action='store_true')
    ap.add_argument('--marker', action='append', help='x,y,z[,label] (coords relative to origin)')
    ap.add_argument('--circle', action='append', help='x,y,z,r ground circle (relative to origin)')
    ap.add_argument('--extent', type=float, help='ortho half-size in blocks (fixed framing instead of auto-fit)')
    ap.add_argument('--center', nargs=3, type=float, help='ortho framing centre (relative coords)')
    ap.add_argument('--zoom', type=float, default=1.0)
    ap.add_argument('--width', type=int, default=None, help='output width px (default 900, wider for long strips)')
    ap.add_argument('--cols', type=int)
    ap.add_argument('--aspect', type=float, help='panel height/width (default 1, 0.62 for camera-only)')
    ap.add_argument('--ss', type=int, default=2, help='supersampling factor (default 2)')
    ap.add_argument('--bg-top', type=int, nargs=3, default=(36, 38, 48))
    ap.add_argument('--bg-bottom', type=int, nargs=3, default=(58, 60, 72))
    ap.add_argument('--title', help='extra title text')
    ap.add_argument('-o', '--out', default=str(HERE / 'out' / 'preview.png'))
    ap.add_argument('-q', '--quiet', action='store_true')
    args = ap.parse_args(argv)
    ARGS = args
    LOG.quiet = args.quiet
    args.score_map = {}
    for s in args.score:
        k, v = s.rsplit('=', 1)
        args.score_map[k.strip()] = int(v)
    args.macro_map = dict(s.split('=', 1) for s in args.macro)
    rps = args.rp or [str(DEFAULT_RP)]
    ASSETS = Assets(rps, args.skin)
    job = Job(args)
    cam_rel = None
    if args.camera_preset == 'judgment' and not args.camera:
        cam_rel = (0.0, 3.0, 13.0, 180.0, -10.0)      # relative to the arena centre (0,201,0)
    elif args.camera_preset == 'player-front' and not args.camera:
        f = mc_forward(job.subject_yaw) * args.camera_dist
        cam_rel = (f[0], 1.62, f[2], job.subject_yaw + 180, -12.0)
    if args.camera:
        x, y, z, yw, pt = args.camera
        o = job.origin
        cam_rel = (x - o[0], y - o[1], z - o[2], yw, pt)
    if args.views:
        vnames = args.views.split(',') if not re.search(r'(cam|az):', args.views) else re.findall(r'(?:cam|az):[^,]+,[^,]+|[^,]+', args.views)
    elif args.strip:
        vnames = ['camera'] if cam_rel else ['front']
    else:
        vnames = (['camera', 'front', 'top', 'right'] if cam_rel else ['front', 'right', 'top', 'iso'])
    views = make_views(vnames, job.subject_yaw, cam_rel, args.fov, args.az, args.el)
    if not views:
        raise SystemExit('no views')
    ticks = parse_strip(args.strip) if args.strip else [job.tick0]
    scenes = {t: job.scene(t) for t in ticks}
    geos = {t: Geometry(scenes[t], ASSETS, hide=args.hide, only=args.only, translucent=args.translucent) for t in ticks}
    panels = [(t, v) for t in ticks for v in views]
    n = len(panels)
    strip = len(ticks) > 1
    all_cam = all(v.persp for v in views)
    if args.cols:
        cols = args.cols
    elif strip and len(views) > 1:
        cols = len(views)
    elif strip:
        cols = min(n, 4 if all_cam else 5)
    else:
        cols = 1 if n == 1 else (2 if n <= 4 else 3)
    if args.width:
        width = args.width
    elif strip:
        width = max(900, cols * (320 if all_cam else 260))
    else:
        width = 900 if n > 1 else 700
    pw = width // cols
    aspect = args.aspect or (0.5625 if all_cam else 1.0)
    ph = int(pw * aspect)
    ss = max(1, args.ss)
    W, H = pw * ss, ph * ss
    fit_views(views, list(geos.values()), W, H, args)
    # tracks
    tracks = {}
    if args.track:
        if args.track_range:
            tr = parse_strip(args.track_range)
        elif len(ticks) > 1:
            tr = list(range(min(ticks), max(ticks) + 1))
        else:
            tr = ticks
        tracks = track_points(job, args, tr, views)
    overlays = job.overlays()
    labels3d = job.labels3d()
    title_h = 22
    rows = math.ceil(n / cols)
    sheet = Image.new('RGB', (pw * cols, ph * rows + title_h), (20, 20, 26))
    font = load_font(12)
    font_s = load_font(10)
    d0 = ImageDraw.Draw(sheet)
    mode_desc = {'rig': lambda: f'rig phase={job.phase} clip={job.clip}', 'judgment': lambda: f'judgment rig (origin {tuple(job.origin)})',
                 'item': lambda: 'items ' + ' '.join(args.item), 'generic': lambda: 'spawn ' + ' '.join(args.spawn or []) + ' apply ' + ' '.join(args.apply or [])}[job.mode]()
    d0.text((6, 4), (args.title + ' | ' if args.title else '') + mode_desc + f' | subject yaw {job.subject_yaw:g} (orange arrow = facing)', fill=(230, 230, 235), font=font)
    held = {t: held_props(geos[t], args.held, job.subject_yaw) for t in ticks} if args.held else {}
    for k, (t, v) in enumerate(panels):
        geo = geos[t]
        lines = list(overlays)
        for row in held.get(t, []):
            c, tip = row['centre'], row['centre'] + row['dir'] * 0.8
            side = np.cross(row['dir'], [0, 1, 0])
            side = side / np.linalg.norm(side) * 0.12 if np.linalg.norm(side) > 1e-6 else np.array([0.12, 0, 0])
            for seg in ([c, tip], [tip, tip - row['dir'] * 0.2 + side], [tip, tip - row['dir'] * 0.2 - side]):
                lines.append((seg, (255, 60, 230), 3, (150, 40, 140)))
        img, zimg = render_view(geo, v, W, H, args, ASSETS, lines)
        pim = Image.fromarray((img * 255).astype(np.uint8))
        if ss > 1:
            pim = pim.resize((pw, ph), Image.LANCZOS)
        d = ImageDraw.Draw(pim)
        # tracked paths
        for spec, rowsl in tracks.items():
            pts = [(tt, p) for tt, p, _ in rowsl if p is not None]
            if len(pts) >= 1:
                P = np.array([p for _, p in pts])
                Sxy = v.screen(v.cam(P), W, H) / ss
                okp = np.ones(len(P), bool) if not v.persp else v.cam(P)[:, 2] > 0.05
                seq = [tuple(s) for s, o in zip(Sxy, okp) if o]
                if len(seq) > 1:
                    d.line(seq, fill=(255, 235, 60), width=2)
                for (tt, p), s, o in zip(pts, Sxy, okp):
                    if not o:
                        continue
                    rr = 4 if tt == t else 2
                    d.ellipse([s[0] - rr, s[1] - rr, s[0] + rr, s[1] + rr], fill=(255, 60, 60) if tt == t else (255, 235, 60))
                ends = [(pts[0], 'start'), (pts[-1], 'end')]
                for (tt, p), word in ends:
                    s = v.screen(v.cam(p[None]), W, H)[0] / ss
                    d.text((s[0] + 4, s[1] - 12), f'{word} t{tt}', fill=(255, 235, 60), font=font_s)
        for pos, text in labels3d:
            C = v.cam(np.array([pos], float))
            if v.persp and C[0, 2] < 0.05:
                continue
            s = v.screen(C, W, H)[0] / ss
            if 0 <= s[0] < pw and 0 <= s[1] < ph:
                d.text((s[0] + 3, s[1] - 6), text, fill=(200, 230, 255), font=font_s)
        tick_txt = f't={t}  ' if job.mode in ('rig', 'judgment') or args.strip else ''
        d.rectangle([0, 0, pw, 28], fill=(0, 0, 0))
        d.text((4, 1), f'{tick_txt}{v.name if strip else v.label}', fill=(255, 255, 255), font=font)
        d.text((4, 15), v.axis_words() + (f'  1 block={v.scale / ss:.0f}px' if not v.persp else f'  fov {v.fov:g}'), fill=(190, 190, 200), font=font_s)
        draw_gizmo(d, v, pw - 34, ph - 30, font_s)
        if geo.hidden and not args.quiet and k == 0:
            pass
        sheet.paste(pim, ((k % cols) * pw, title_h + (k // cols) * ph))
        d0.rectangle([(k % cols) * pw, title_h + (k // cols) * ph, (k % cols) * pw + pw - 1, title_h + (k // cols) * ph + ph - 1], outline=(10, 10, 14))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    g0 = geos[ticks[0]]
    nq = sum(len(b['tex']) for _, b, _, _, _ in g0.items)
    print(f'wrote {out}  ({sheet.size[0]}x{sheet.size[1]}, {n} panels, {len(g0.items)} visible displays, {nq} quads at t={ticks[0]})')
    if g0.hidden:
        print(f'hidden (zero-determinant scale) at t={ticks[0]}: {", ".join(sorted(set(g0.hidden)))}')
    if ASSETS.missing_items:
        print('MISSING item definitions: ' + ', '.join(sorted(ASSETS.missing_items)))
    if ASSETS.missing_textures:
        print('MISSING textures (magenta): ' + ', '.join(sorted(ASSETS.missing_textures)))
    if LOG.counts and not args.quiet:
        print('interpreter notes: ' + '; '.join(f'{k} x{v}' for k, v in sorted(LOG.counts.items())))
    if tracks:
        print_tracks(tracks, views, W, H)
    for t in ticks:
        for row in held.get(t, []):
            print(f"held t={t} {row['name']}: business end (model +Y) fwd {row['fwd']:+.2f} up {row['up']:+.2f} right {row['right']:+.2f}"
                  + ('   REVERSED? (points behind the grip)' if row['fwd'] < -0.2 else ''))


def held_props(geo, subs, subject_yaw):
    """Business-end direction of hand props (model +Y through the full item_display chain, Ry180 included) in the
    subject frame. The 26.x client adds nothing else for item_display:"none" (ItemTransforms.getTransform(NONE) is
    the identity, DisplayRenderer FIXED orientation = rotationYXZ(-yaw, pitch, 0)), so this is what the game shows."""
    f = mc_forward(subject_yaw)
    up = np.array([0.0, 1.0, 0.0])
    right = np.cross(f, up)
    out, seen = [], set()
    for e, baked, tints, M, name in geo.items:
        if e.idx in seen or not any(any(sub in tg for tg in e.tags) for sub in subs):
            continue
        seen.add(e.idx)
        W = geo.entity_matrix(e, M, None)
        d = W[:3, :3] @ np.array([0.0, 1.0, 0.0])
        n = np.linalg.norm(d)
        if n < 1e-9:
            continue
        d = d / n
        tag = next((tg for tg in sorted(e.tags) if any(sub in tg for sub in subs)), name)
        out.append({'name': tag, 'centre': W[:3, 3], 'dir': d, 'fwd': float(d @ f), 'up': float(d @ up), 'right': float(d @ right)})
    return out


if __name__ == '__main__':
    main()
