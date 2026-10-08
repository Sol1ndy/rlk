# 몹이 맞을 때 원소 처리 (@s = 몹, at @s). combat/apply 에서 호출
# 입력: #elem(0~7), #elU(부착량 1000=1U, 0=부착 안 함), #icd(1=기본공격처럼 부착 쿨 적용), #tfm(1=반응 피해라 증폭 안 받음)
# 결과: #dmg 보정(증발·융해 배율, 촉진·발산 추가 피해, 초전도 물리 증폭), 격변 반응은 몹에 예약(rxQ)되어 다음 틱에 발동
scoreboard players set #rx tmp 0
# 초전도: 물리 피해 +40%
execute if score #elem tmp matches 0 if score @s scT matches 1.. run function rlk:element/sc_amp
execute unless score #elem tmp matches 1.. run return 0
# 공허: 맞을 때마다 잠식
execute if score #elem tmp matches 8 run function rlk:element/void/erode
execute unless score #elU tmp matches 1.. run return 0
# 부착 쿨(ICD): 기본공격은 2.5초마다 또는 3타마다 1번만 원소가 묻음
scoreboard players set #apply tmp 1
execute if score #icd tmp matches 1 run function rlk:element/icd
execute if score #apply tmp matches 0 run return 0
execute as @a[tag=player,limit=1] run function rlk:element/src_player
function rlk:element/react
# 각인: 반응이 일어났을 때(증폭 · 원소)
execute if score #rx tmp matches 1.. run function rlk:engravings/on_rx
scoreboard players set @s elAct 1
# 개화 씨앗에 불/번개가 닿으면 발화/만개
execute if score #elem tmp matches 1 run scoreboard players set @e[tag=rlk_core,distance=..3.5] rxQ 13
execute if score #elem tmp matches 3 run scoreboard players set @e[tag=rlk_core,distance=..3.5] rxQ 12
execute unless score #rx tmp matches 1.. run return 0
function rlk:element/rx_text
execute if score #tfm tmp matches 1 run return 0
scoreboard players operation #dmg tmp *= #mulPct tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players operation #dmg tmp += #addDmg tmp
