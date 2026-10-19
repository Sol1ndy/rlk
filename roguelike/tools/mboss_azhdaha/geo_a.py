"""S2-A: P1 chin slam, P2 jump slam, P3 charge, P4 back spikes (plan.md 5; s2.md 2.1). STUB by S1-MOD: the ids,
the Pattern records (weights pre-filled from plan.md 4.12) and empty, timing-correct start / tick / cancel; S2-A
replaces the emit bodies (AZ:p/{chin,jump,charge,spikes}/**) and adds h_pa.py."""
from . import api as A

P4_W = {'head_near': 2, 'head_mid': 3, 'head_far': 3, 'flank_near': 2, 'flank_far': 2, 'tail_lane': 2, 'tail_off': 2, 'paw': 1}
PATTERNS = [
    A.Pattern(1, 'chin', '갈라지는 봉인의 땅', 'normal', 'chin_slam', lead=8, recover=18, max_len=80, length=65,
              weight={'head_near': 4, 'head_mid': 2, 'paw': 2}, gates=('field_area',)),
    A.Pattern(2, 'jump', '바위 분쇄 충돌', 'normal', 'jump_slam', recover=16, max_len=70, length=53,
              weight={'head_near': 1, 'head_mid': 3, 'head_far': 3, 'flank_near': 1, 'flank_far': 2, 'tail_lane': 1,
                      'tail_off': 2, 'paw': 1}, gates=('field_area',)),
    A.Pattern(3, 'charge', '바위 용왕의 돌진', 'normal', 'charge_coil', lead=10, recover=30, max_len=90, length=71,
              weight={'head_mid': 1, 'head_far': 5}, gates=('front35',)),
    A.Pattern(4, 'spikes', '천동만상', 'normal', 'spikes', phases=(1, 2), recover=20, max_len=100, length=90, weight=P4_W),
]


def emit(g):
    for p in PATTERNS:
        A.stub_emit(g, p)
