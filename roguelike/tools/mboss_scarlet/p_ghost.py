"""Ghost patterns of 홍련 (Scarlet): R1 자영 돌격, R2 월륜 일섬, R3 자영 활강 and the gauntlets A8 자영 연참 (60 %) /
A13 필살 · 자영 연참 (5 %), with the shared ghost helpers g/** (the cut builder g/cut/**, reappear points, discs)
(PLAN §4.4-4.5, §5). OWNER: S4.

D0 stub: S4 replaces this file. Contract (api.Pattern): PATTERNS = [api.Pattern(key, tid, clips, build) for key in
api.P2]; build(W) writes only p/<key>/** and g/** (W = api.Writer('S4', api.OWN['S4'])); timings from api.SCRIPTS /
api.ev, hits from api.HITS (DMG tiers), cuts only through api.cut(), discs only through api.disc(), the shield only
through api.shield().
"""
from . import api  # noqa: F401

PATTERNS = []
