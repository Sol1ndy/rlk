# 플레이어가 원소 공격(#elem)을 맞음 (@s = 플레이어, at @s anchored eyes). #dmgIn 을 반응에 따라 보정
function rlk:element/src_mob
scoreboard players set #elU tmp 1000
function rlk:element/react
scoreboard players set @s elAct 1
execute unless score #rx tmp matches 1.. run return 0
execute positioned ^ ^-2 ^1.6 run function rlk:element/rx_text
# 증폭(증발·융해) / 추가 피해(촉진·발산)
scoreboard players operation #dmgIn tmp *= #mulPct tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
scoreboard players operation #dmgIn tmp += #addDmg tmp
# 격변 반응(과부하·초전도·쇄빙·확산·개화)은 즉시 추가 피해로. 결정은 효과 없음
execute if score @s rxQ matches 3..8 run scoreboard players operation #dmgIn tmp += @s rxDmg
execute if score @s rxQ matches 11 run scoreboard players operation #dmgIn tmp += @s rxDmg
execute if score @s rxQ matches 4 run scoreboard players set @s scT 240
scoreboard players set @s rxQ 0
