# 실제 대쉬 (@s = 플레이어, at @s): 무적 + 효과 + 방향/이동
scoreboard players set @s dashInvT 9
playsound minecraft:entity.wind_charge.wind_burst master @a ~ ~ ~ 0.9 1.4
playsound minecraft:entity.breeze.slide master @a ~ ~ ~ 0.7 1.5
particle minecraft:cloud ~ ~0.5 ~ 0.3 0.3 0.3 0.03 8
execute at @e[tag=rlk_body,limit=1] anchored eyes rotated ~ 0 run particle minecraft:cloud ^ ^-0.2 ^1 0.25 0.25 0.25 0.03 6
# 현재 이동 입력 방향(없으면 시선 방향)으로 이동 시작
function rlk:player/dash_dir
# 아이템 대쉬 트리거
function rlk:items/hook/on_dash
