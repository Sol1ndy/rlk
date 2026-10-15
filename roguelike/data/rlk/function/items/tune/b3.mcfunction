# 아이템 조정 묶음 3 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# 새 상수 없음: 세 상수 모두 load 에서 매번 설정 (#beadsHeal 15 · #herbPct 50 · #thimbleDmg 8)
# 기도 묵주: 개당 받는 치유량 증가 % (+100 기준은 고정)
data modify storage rlk:tune t.prayer_beads set value [{n:"#beadsHeal",m:"a"}]
data modify storage rlk:tune ids append value "prayer_beads"
# 붉은 약초: 회복 구슬 회복량 증가 % (개수와 무관, +100 기준은 고정)
data modify storage rlk:tune t.red_herb set value [{n:"#herbPct",m:"a"}]
data modify storage rlk:tune ids append value "red_herb"
# 마녀의 골무: 개당 스킬 · 폭발 피해 증가 % (#eb eng 가 % 단위라 그대로. 단계별 4/5/7/8)
data modify storage rlk:tune t.witch_thimble set value [{n:"#thimbleDmg",m:"a"}]
data modify storage rlk:tune ids append value "witch_thimble"
# 점술사의 수정 조각 · 새싹 · 견습 기사의 휘장 · 정전기 털뭉치 · 여행자의 장화 · 낡은 숫돌: 능력치만 있어 자동 배율 (표 없음)
