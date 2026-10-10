# @s = 플레이어, at @s. 마검 키리온: 평타 참격 — 주변(3.5)에 공격력의 60% 불 원소 피해
function rlk:items/proc/kirion_dmg_calc
scoreboard players set #sub itv 1
# 붉은 선분 참격 (공격마다 무작위 방향)
execute positioned ~ ~1.62 ~ rotated ~ 0 run function rlk:items/proc/kirion_line_rand
execute unless score #k120 snd matches 1 run function rlk:snd/f128
execute unless score #k121 snd matches 1 run function rlk:snd/f129
execute as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/apply
scoreboard players set #sub itv 0
