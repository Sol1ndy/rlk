# @s = 참격 마커, at @s (위치+회전). 지나온 자리 참격 1회: 무작위 방향 라인 + 공격력의 30% 불 원소 피해
execute as @a[tag=player,limit=1] run function rlk:items/proc/kirion_dmg_calc
scoreboard players set #sub itv 1
# 대쉬 참격은 개당 30% (평타 참격 60%의 절반). 대쉬 한 번에 여러 개가 생김
scoreboard players operation #dmg tmp /= #st2 tmp
function rlk:items/proc/kirion_line_rand
particle minecraft:crimson_spore ~ ~ ~ 0.6 0.5 0.6 0.04 12
execute unless score #k175 snd matches 1 run function rlk:snd/f187
execute unless score #k176 snd matches 1 run function rlk:snd/f188
execute as @e[tag=rlk_mob,distance=..3] at @s run function rlk:combat/apply
kill @s
scoreboard players set #sub itv 0
