# 아이템 조정 묶음 5 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# hurricane_core: 반복 간격(틱, 공용 #st10 대신 이 아이템만)
scoreboard players set #vortexGap tmp 10
# hound_whistle: 반복 간격(틱, 공용 #st20 대신 이 아이템만)
scoreboard players set #houndGap tmp 20
# 달궈진 솥: 불길 한 번당 피해 계수 (공격력의 %, items/proc/pot_fire 의 고정값 대신)
scoreboard players set #potCoef tmp 45
# 사냥개 호루라기: 물기 피해 계수 · 물 때마다 회복 ‰ (10‰ = 최대 체력의 1%, 값은 load 에서 ‰ 로 설정. items/proc/hound_heal 이 ‰ 로 계산)
scoreboard players set #houndCoef tmp 35
# 사냥꾼의 표식: 타격당 피해 증가 0.1% 단위 (30 = 3%, 값은 load 에서 ‰ 로 설정. items/proc/hunt 가 ÷10)
# 바람의 정다면체: 회오리 피해 계수
scoreboard players set #vortexCoef tmp 20
# 메이드의 건틀릿: 회복량 = 방어력의 ‰ (60‰ = 6%, items/proc/maid 의 고정값 6% 대신)
scoreboard players set #maidHeal tmp 60
# 잠결의 별: 보호막 ‰ (80‰ = 최대 체력의 8%, 값은 load 에서 ‰ 로 설정) · 별 간격(틱, 공용 #st30 대신) · 발사 피해 계수
scoreboard players set #nightGap tmp 30
scoreboard players set #nightCoef tmp 80
# 밤혼의 구슬: 낙뢰 피해 계수
scoreboard players set #orbCoef tmp 50
# 달궈진 솥: 불길 횟수(효과 길이라 d) · 불길 간격(틱, #potGap > 10 이어야 함) · 피해 계수. 첫 불길 0.5초 · 판정 범위는 고정
data modify storage rlk:tune t.hot_pot set value [{n:"#potN",m:"d"},{n:"#potGap",m:"c"},{n:"#potCoef",m:"a"}]
data modify storage rlk:tune ids append value "hot_pot"
# 사냥개 호루라기: 지속 시간 · 피해 계수 · 회복 ‰. 물기 간격 1초(#st20, items/proc/hound_tick)는 공용이라 고정
data modify storage rlk:tune t.hound_whistle set value [{n:"#houndDur",m:"d"},{n:"#houndCoef",m:"a"},{n:"#houndHeal",m:"a"},{n:"#houndGap",m:"c"}]
data modify storage rlk:tune ids append value "hound_whistle"
# 사냥꾼의 표식: 타격당 피해 증가 (최대 10회 #huntMax 는 고정, 최대치는 따라서 바뀜)
data modify storage rlk:tune t.hunter_mark set value [{n:"#huntPer",m:"a"}]
data modify storage rlk:tune ids append value "hunter_mark"
# 바람의 정다면체: 회오리 지속 시간 · 피해 계수. 타격 간격 0.5초(#st10, items/proc/vortex_tick)는 공용이라 고정 · 반경 5칸 고정
data modify storage rlk:tune t.hurricane_core set value [{n:"#vortexDur",m:"d"},{n:"#vortexCoef",m:"a"},{n:"#vortexGap",m:"c"}]
data modify storage rlk:tune ids append value "hurricane_core"
# 열혈 저울: 공격력 증가 % · 지속 시간
data modify storage rlk:tune t.kinetic_scale set value [{n:"#kinAtk",m:"a"},{n:"#kinDur",m:"d"}]
data modify storage rlk:tune ids append value "kinetic_scale"
# 메이드의 건틀릿: 회복 ‰ · 재사용 대기(틱)
data modify storage rlk:tune t.maid_gauntlet set value [{n:"#maidHeal",m:"a"},{n:"#maidCdT",m:"c"}]
data modify storage rlk:tune ids append value "maid_gauntlet"
# 특순대 휘장: 공격력 증가 % · 지속 시간 (과부하 반응 조건은 고정)
data modify storage rlk:tune t.musketeer_badge set value [{n:"#muskAtk",m:"a"},{n:"#muskDur",m:"d"}]
data modify storage rlk:tune ids append value "musketeer_badge"
# 잠결의 별: 보호막 ‰ · 지속 시간 · 별 간격 · 피해 계수. 발사에 필요한 별 4개(night_tick 의 ..3 / 4..)와 보호막 유지 15초는 고정
data modify storage rlk:tune t.night_stars set value [{n:"#nightShield",m:"a"},{n:"#nightDur",m:"d"},{n:"#nightGap",m:"c"},{n:"#nightCoef",m:"a"}]
data modify storage rlk:tune ids append value "night_stars"
# 밤혼의 구슬: 피해 계수 · 재사용 대기(틱). 반경 3칸 고정
data modify storage rlk:tune t.nightsoul_orb set value [{n:"#orbCoef",m:"a"},{n:"#orbCdT",m:"c"}]
data modify storage rlk:tune ids append value "nightsoul_orb"
# 낡은 석판: 옆 아이템 스탯 증가 % (옆 아이템 자신의 강화 배율은 items/slate/add 에서 따로 곱함)
data modify storage rlk:tune t.old_slate set value [{n:"#slatePct",m:"a"}]
data modify storage rlk:tune ids append value "old_slate"
