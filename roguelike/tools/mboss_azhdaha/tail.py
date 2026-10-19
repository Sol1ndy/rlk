"""S2-T: 41 서리 습격, 42 벼락 습격 (B3 specials), 43 쏟아지는 천화 (bg slot T), 44 번개의 가루, 45 / 46 천동만상 ice /
electro, the Cryo / Electro addon bodies AZ:xt/** (plan.md 4.6, 5; s2.md 2.1, 7, 8, 10). STUB by S1-MOD: ids,
Pattern records and empty, timing-correct files (43: the sphere at tail_cast fire 18 hands over to bg slot T for 200 t);
no addon bodies. S2-T replaces all of it and adds h_pt.py."""
from . import api as A
from .geo_a import P4_W

ICICLE_FIRE = A.ev('tail_cast', 'fire')
PATTERNS = [
    A.Pattern(41, 'frost', '서리 습격', 'special', None, phases=(3,), elem=('tail', 4), max_len=A.B3_LEN, length=A.B3_LEN - 4,
              hooks=('b3tick', 'stop', 'reload', 'pause', 'resume')),
    A.Pattern(42, 'bolt', '벼락 습격', 'special', None, phases=(3,), elem=('tail', 3), max_len=A.B3_LEN, length=A.B3_LEN - 4,
              hooks=('b3tick', 'stop', 'reload', 'pause', 'resume')),
    A.Pattern(43, 'icicle', '쏟아지는 천화', 'bg', 'tail_cast', phases=(3,), elem=('tail', 4), cooldown=400, recover=18,
              max_len=50, length=34, gates=('no_bg',),
              weight={'head_mid': 3, 'head_far': 3, 'flank_far': 3, 'tail_lane': 3, 'tail_off': 3},
              hooks=('bgtick', 'cancel_bg', 'reload')),
    A.Pattern(44, 'shell', '번개의 가루', 'normal', 'tail_cast', phases=(3,), elem=('tail', 3), cooldown=400, recover=20,
              max_len=170, length=145,
              weight={'head_near': 1, 'head_mid': 2, 'head_far': 2, 'flank_far': 2, 'tail_lane': 2, 'tail_off': 2}),
    A.Pattern(45, 'icespike', '천동만상 – 얼음 가시', 'normal', 'spikes', phases=(3,), elem=('tail', 4), recover=20, max_len=110,
              length=100, replaces=4, gates=('field_area',)),
    A.Pattern(46, 'elspike', '천동만상 – 번개 가시', 'normal', 'spikes', phases=(3,), elem=('tail', 3), recover=20, max_len=150,
              length=140, replaces=4),
]
P4_WEIGHTS = P4_W


def emit(g):
    for p in PATTERNS:
        if p.kind == 'special':
            A.stub_emit(g, p, b3=True)
        elif p.id == 43:
            A.stub_emit(g, p, bg=(ICICLE_FIRE, 'T', 200))
        else:
            A.stub_emit(g, p)
