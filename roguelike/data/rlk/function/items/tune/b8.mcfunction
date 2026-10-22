# 아이템 조정 묶음 8 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# seamless_shield: 보호막 간격(틱, 공용 #st50 대신 이 아이템만)
scoreboard players set #seamGap tmp 50
# tailor_doll: 반복 간격(틱, 공용 #st60 대신 이 아이템만)
scoreboard players set #dollGap tmp 60
# lumidouce_case: 반복 간격(틱, 공용 #st40 대신 이 아이템만)
scoreboard players set #caseGap tmp 40
# 은방울 향수함 · 별빛 바람뭉치 · 양화: 피해 = 공격력의 % (case_hit1 · case_hit2 · wisp_boom · blossom_hit 의 coef 대신)
scoreboard players set #caseCoef tmp 40
scoreboard players set #caseFireCoef tmp 80
scoreboard players set #wispCoef tmp 110
scoreboard players set #blossomCoef tmp 60
# 재단 인형: 피해 = 방어력의 ‰ (doll_hit 의 pm 대신)
scoreboard players set #dollPm tmp 1000
# 간호사의 주사기: 해소 때 회복 = 최대 체력의 ‰ (80‰ = 8%, nurse_pay 의 숫자 8 대신. ‰ 로 계산)
scoreboard players set #nurseHeal tmp 80
# 무결점 보호막 · 치유의 부적: 보호막 · 회복을 최대 체력의 ‰ 로 (60‰ = 6%, 20‰ = 2%, 값은 load 에서 ‰ 로 설정. seam_pulse · talisman_heal 이 ‰ 로 계산)
# 은방울 향수함: 수명(틱) · 피해 계수 · 불 붙은 적 피해 계수. 2초 간격(#st40, items/proc/case_tick)은 공용이라 고정 · 반경 10칸 고정
data modify storage rlk:tune t.lumidouce_case set value [{n:"#caseDur",m:"d"},{n:"#caseCoef",m:"a"},{n:"#caseFireCoef",m:"a"},{n:"#caseGap",m:"c"}]
data modify storage rlk:tune ids append value "lumidouce_case"
# 단풍잎 한 장: 지속 시간(틱) · 원소 피해 보너스 % (단계별 13/17/21/25) · 재사용 대기(틱)
data modify storage rlk:tune t.maple_leaf set value [{n:"#mapleDur",m:"d"},{n:"#mapleDmg",m:"a"},{n:"#mapleCdT",m:"c"}]
data modify storage rlk:tune ids append value "maple_leaf"
# 간호사의 주사기: 원소 에너지(×100) · 회복 ‰. 생명의 계약 #nurseBol 20% 는 대가라 고정
data modify storage rlk:tune t.nurse_syringe set value [{n:"#nurseEnergy",m:"a"},{n:"#nurseHeal",m:"a"}]
data modify storage rlk:tune ids append value "nurse_syringe"
# 흑요석 거울: 보호막 % (단계별 6/8/10/12) · 받는 피해 증가 % · 표식 지속 시간(틱). 반경 6칸 고정
data modify storage rlk:tune t.obsidian_mirror set value [{n:"#mirShield",m:"a"},{n:"#mirDmg",m:"a"},{n:"#mirDur",m:"d"}]
data modify storage rlk:tune ids append value "obsidian_mirror"
# 봉인된 검: 필요 처치 수 #kirionNeed 150 은 변신 조건이라 고정, 능력치만 자동 배율 (표 없음)
# 무결점 보호막: 지속 시간(틱) · 간격(틱, #seamGap) · 보호막 ‰ · 회복 ‰
data modify storage rlk:tune t.seamless_shield set value [{n:"#seamDur",m:"d"},{n:"#seamGap",m:"c"},{n:"#seamShield",m:"a"},{n:"#seamHeal",m:"a"}]
data modify storage rlk:tune ids append value "seamless_shield"
# 별빛 바람뭉치: 피해 계수 · 재사용 대기(틱). 폭발까지 #wispFuse 1.5초 · 반경 3.5칸은 고정
data modify storage rlk:tune t.star_wisp set value [{n:"#wispCoef",m:"a"},{n:"#wispCdT",m:"c"}]
data modify storage rlk:tune ids append value "star_wisp"
# 양화: 꽃 수명(틱) · 피해 계수 · 재사용 대기(틱). 꽃 반경 6칸 · 피해 반경 3칸은 고정
data modify storage rlk:tune t.sun_blossom set value [{n:"#blossomDur",m:"d"},{n:"#blossomCoef",m:"a"},{n:"#blossomCdT",m:"c"}]
data modify storage rlk:tune ids append value "sun_blossom"
# 재단 인형: 수명(틱) · 피해 ‰. 3초 간격(#st60, items/proc/doll_tick)은 공용이라 고정 · 반경 10칸 고정
data modify storage rlk:tune t.tailor_doll set value [{n:"#dollDur",m:"d"},{n:"#dollPm",m:"a"},{n:"#dollGap",m:"c"}]
data modify storage rlk:tune ids append value "tailor_doll"
# 치유의 부적: 부적 지속 시간(틱) · 회복 ‰ · 회복 재사용 대기(틱)
data modify storage rlk:tune t.talisman set value [{n:"#talDur",m:"d"},{n:"#talHeal",m:"a"},{n:"#talCdT",m:"c"}]
data modify storage rlk:tune ids append value "talisman"
