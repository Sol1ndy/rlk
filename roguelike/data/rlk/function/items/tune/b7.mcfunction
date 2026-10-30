# 아이템 조정 묶음 7 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# jellyfish: 반복 간격(틱, 공용 #st40 대신 이 아이템만)
scoreboard players set #jellyGap tmp 40
# 선학의 깃: 바람 범위 피해 = 공격력의 % (items/proc/crane_boom 의 고정값 대신)
scoreboard players set #craneCoef tmp 150
# 민들레 씨앗: 회복량 = 공격력의 % (items/proc/dandelion 의 고정값 대신)
scoreboard players set #dandHeal tmp 150
# 얼음 깃촉: 깃 하나당 추가 피해 = 공격력의 % (items/proc/quill_hit 의 고정값 대신)
scoreboard players set #quillCoef tmp 45
# 해파리 등불: 파동 피해 = 최대 체력의 ‰ (items/proc/jelly_pulse 의 고정값 대신) · 회복을 ‰ 로 (20‰ = 2%, 값은 load 에서 ‰ 로 설정. jelly_heal 이 ‰ 로 계산)
scoreboard players set #jellyPm tmp 50
# 생명줄: 대쉬 끝 물 피해 = 최대 체력의 ‰ (items/proc/lifeline_fire 의 고정값 대신)
scoreboard players set #lifelinePm tmp 80
# 별의 징조: 징조 지속 시간(틱) · 받는 피해 증가 % (#eb eng 가 % 단위라 그대로. 단계별 10/13/17/20)
data modify storage rlk:tune t.astral_omen set value [{n:"#omenDur",m:"d"},{n:"#omenDmg",m:"a"}]
data modify storage rlk:tune ids append value "astral_omen"
# 주방장의 특선: 능력치만 있어 자동 배율 (표 없음)
# 선학의 깃: 피해 계수 · 대쉬 뒤 유효 시간(틱). 반경 4.5칸은 고정
data modify storage rlk:tune t.crane_feather set value [{n:"#craneCoef",m:"a"},{n:"#craneDur",m:"d"}]
data modify storage rlk:tune ids append value "crane_feather"
# 민들레 씨앗: 회복 계수 · 이동 속도 증가 % · 지속 시간(틱)
data modify storage rlk:tune t.dandelion_seed set value [{n:"#dandHeal",m:"a"},{n:"#dandSpd",m:"a"},{n:"#dandDur",m:"d"}]
data modify storage rlk:tune ids append value "dandelion_seed"
# 용의 불씨: 지속 시간(틱) · 증발·융해 피해 증가 % · 불 원소 피해 보너스 % (drag_rx 의 +100 기준은 고정)
data modify storage rlk:tune t.dragon_flame set value [{n:"#dragDur",m:"d"},{n:"#dragRx",m:"a"},{n:"#dragFire",m:"a"}]
data modify storage rlk:tune ids append value "dragon_flame"
# 꿈결 베개: 원소 마스터리 · 이동 속도 증가 % · 지속 시간(틱). 확산 반응 조건은 고정
data modify storage rlk:tune t.dream_pillow set value [{n:"#pillowEm",m:"a"},{n:"#pillowSpd",m:"a"},{n:"#pillowDur",m:"d"}]
data modify storage rlk:tune ids append value "dream_pillow"
# 금단의 도서: 표 없음 (능력치만 자동 배율). 필요 페이지 #forbNeed 250 은 변신 조건, 적중당 1장 · 적마다 최대 3장은 정수 · 한도라 고정
# 공상의 악보: 스택당 피해 증가 % (#eb eng 가 % 단위라 그대로. 단계별 5/7/8/10) · 지속 시간(틱). 최대 3스택은 고정
data modify storage rlk:tune t.harmonic_score set value [{n:"#harmDmg",m:"a"},{n:"#harmDur",m:"d"}]
data modify storage rlk:tune ids append value "harmonic_score"
# 얼음 깃촉: 얻는 깃 개수(단계별 3/4/5/6) · 유지 시간(틱) · 추가 피해 계수. 적중당 1개 소모 · 2.5칸은 고정
data modify storage rlk:tune t.ice_quill set value [{n:"#quillN",m:"a"},{n:"#quillDur",m:"d"},{n:"#quillCoef",m:"a"}]
data modify storage rlk:tune ids append value "ice_quill"
# 해파리 등불: 수명(틱) · 피해 ‰ · 회복 ‰. 2초 간격(#st40, items/proc/jelly_tick)은 공용이라 고정 · 반경 4칸 고정
data modify storage rlk:tune t.jellyfish set value [{n:"#jellyDur",m:"d"},{n:"#jellyPm",m:"a"},{n:"#jellyHeal",m:"a"},{n:"#jellyGap",m:"c"}]
data modify storage rlk:tune ids append value "jellyfish"
# 생명줄: 피해 ‰. 실 감기 반경 2.5칸은 고정
data modify storage rlk:tune t.lifeline set value [{n:"#lifelinePm",m:"a"}]
data modify storage rlk:tune ids append value "lifeline"
