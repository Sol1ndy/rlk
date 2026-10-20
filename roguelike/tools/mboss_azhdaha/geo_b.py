"""S2-B: P5 stomp, P5b triple stomp, P6 feint, P7 tail whip, P8 tail slam, P9 burrow charge (plan.md 5; s2.md 2.1).
STUB by S1-MOD: ids, Pattern records and empty, timing-correct files; S2-B replaces the emit bodies
(AZ:p/{stomp,stomp3,feint,whip,tailslam,burrow}/**) and adds h_pb.py."""
from . import api as A

PATTERNS = [
    A.Pattern(5, 'stomp', '산명곡응', 'normal', {'by': 'paw', 'map': {1: 'stomp_fl', 2: 'stomp_fr', 3: 'stomp_hl', 4: 'stomp_hr'}},
              recover=18, max_len=80, length=63, weight={'head_near': 1, 'flank_near': 2, 'tail_off': 1, 'paw': 5},
              gates=('field_area',)),
    A.Pattern(10, 'stomp3', '산명곡응 – 연속 발구르기', 'normal', {'by': 'paw', 'map': {1: 'stomp3_fl', 2: 'stomp3_fr'}},
              phases=(3,), recover=20, max_len=100, length=85, replaces=5, gates=('field_area',)),
    A.Pattern(6, 'feint', '성동격서', 'normal', 'feint', recover=14, max_len=60, length=50),
    A.Pattern(7, 'whip', '교활한 통수', 'normal', {'by': 'side', 'map': {1: 'tail_whip_l', -1: 'tail_whip_r'}},
              recover=18, max_len=80, length=64, weight={'flank_far': 1, 'tail_off': 2}, gates=('anchor8', 'exit')),
    A.Pattern(8, 'tailslam', '꼬리찍기', 'normal', 'tail_slam', recover=18, max_len=85, length=70,
              weight={'tail_lane': 4, 'tail_off': 1}, gates=('anchor8', 'field_area')),
    A.Pattern(9, 'burrow', '잠복 돌진', 'normal', 'burrow_dive', phases=(1,), cooldown=600, recover=24, max_len=300,
              length=273, weight={'head_near': 1, 'head_mid': 2, 'head_far': 2, 'flank_far': 1, 'tail_lane': 1, 'tail_off': 1}),
]


def emit(g):
    for p in PATTERNS:
        A.stub_emit(g, p)
