"""S2-A helpers (geo_a.py: P1 chin slam, P2 jump slam, P3 charge, P4 back spikes). Pure Python; imported by geo_a.py
directly (s2.md 1: a helper used by two stages moves into api.py by request).

    Sub(g, key, sub)            a per-tick bucket of lines that run positioned / rotated at a marker: at(t, *lines) as a
                                TL; flush(tl, sel) writes p/<key>/<sub>/<t> and adds one positioned call per tick to tl
    marker(tags, pos='~ 201 ~') a summon line of a pattern marker (rlk_room rlk_mb_aux rlk_mb_az_pat + tags)
    at_m(tag)                   'execute at <marker> rotated as <marker>' prefix of a marker tag
    sel_m(tag)                  the marker selector of a tag
    sel_e(tag)                  any entity with a tag
"""
from . import api as A

__all__ = ['Sub', 'marker', 'at_m', 'sel_m', 'sel_e', 'PAT_TAGS']

PAT_TAGS = ('rlk_room', 'rlk_mb_aux', 'rlk_mb_az_pat')


def sel_m(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def sel_e(tag):
    return f'@e[tag={tag}]'


def at_m(tag):
    return f'execute at {sel_m(tag)} rotated as {sel_m(tag)}'


def marker(tags, pos=None):
    pos = pos or f'~ {A.L.num(float(A.CY))} ~'
    t = ','.join(f'"{x}"' for x in PAT_TAGS + tuple(tags))
    return f'summon minecraft:marker {pos} {{Tags:[{t}]}}'


class Sub:
    """Lines per pattern tick that must run at a marker (the hazards / fronts / fx of a point that is not the body):
    the TL-like `at(t, *lines)` collects them (api.Gen.wave accepts it as its `tl`), `flush` writes one function per
    tick and puts the positioned call into the real TL."""

    def __init__(self, g, key, sub):
        self.g, self.key, self.sub, self.ev = g, key, sub, {}

    def at(self, t, *lines):
        for line in lines:
            for one in A._flat([line]):
                self.ev.setdefault(int(t), []).append(one)

    def span(self, t0, t1, *lines):
        for t in range(t0, t1 + 1):
            self.at(t, *lines)

    def flush(self, tl, tag, cond=None):
        """Write p/<key>/<sub>/<t> and call each at the marker `tag` on its tick (cond: an extra execute guard)."""
        for t, lines in sorted(self.ev.items()):
            name = f'{self.sub}/{t}' if t >= 0 else f'{self.sub}/m{-t}'
            self.g.pw(self.key, name, [f'# {self.key} {self.sub} at tick {t} (positioned / rotated at {tag})'] + lines)
            pre = at_m(tag) + (f' {cond}' if cond else '')
            tl.at(t, f'{pre} run function {A.NS}p/{self.key}/{name}')
