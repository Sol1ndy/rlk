"""S2-L: 31 격류 범람 (Hydro orbs), 32 운석 낙하 (Pyro meteors), 33 화염 잠식 (the Pyro fire rule), the Hydro / Pyro
addon bodies AZ:xl/** (plan.md 4.6, 4.7, 5; s2.md 2.1, 6, 9, 10). STUB by S1-MOD: ids, Pattern records and empty,
timing-correct cast / ctick / bgtick files (31: the orbs would spawn at roar_rear drop - 2 and orbit 600 t + fade 10 t
in bg slot L; 32: the cast ends after the last small meteor R+74); no addon bodies (so the dispatchers stay empty);
p/firefield/on_brand only counts its calls (#aq33N). S2-L replaces all of it and adds h_pl.py."""
from . import api as A

EVERY2 = {z: 2 for z in A.ZONES}
EVERY1 = {z: 1 for z in A.ZONES}
ORB_SPAWN = A.ev('roar_rear', 'drop') - 2               # 60
ORB_LIFE = 600 + 10
METEOR_END = A.ev('roar_rear', 'roar') + 74             # R + 74
PATTERNS = [
    A.Pattern(31, 'orbs', '격류 범람', 'cast', None, phases=(2, 3), elem=('leg', 2), phase_weight={2: EVERY2, 3: EVERY1},
              cooldown=600, recover=30, max_len=90, length=82, gates=('no_live', 'no_bg'),
              hooks=('cast', 'ctick', 'refresh', 'bgtick', 'cancel_bg', 'reload', 'pause', 'resume')),
    A.Pattern(32, 'meteor', '운석 낙하', 'cast', None, phases=(2, 3), elem=('leg', 1), phase_weight={2: EVERY2, 3: EVERY1},
              cooldown=600, recover=30, max_len=110, length=94, gates=('no_live', 'field_area'), hooks=('cast', 'ctick')),
]


def emit(g):
    A.stub_emit(g, PATTERNS[0], cast=(ORB_SPAWN, 'L', ORB_LIFE))
    A.stub_emit(g, PATTERNS[1], cast=(METEOR_END, None, None))
    g.pw('firefield', 'on_brand', ['# STUB (S1-MOD): 33 화염 잠식 (S2-L): a fire field r 4.5 / 160 t under the player, or extend one within 4 b.',
                                   '# @s = body, at the player\'s floor point; #azBrNew 1 new brand / 0 refresh. Counts calls only.',
                                   'scoreboard players add #aq33N mb 1'])
