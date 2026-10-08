# @s = 플레이어, at @s. 마검 키리온: 평타 참격 — 주변(3.5)에 공격력의 60% 불 원소 피해
function rlk:items/proc/kirion_dmg_calc
scoreboard players set #sub itv 1
# 붉은 선분 참격 (공격마다 무작위 방향)
execute anchored eyes rotated ~ 0 run function rlk:items/proc/kirion_line_rand
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 0.45 0.6
playsound minecraft:entity.player.attack.crit master @a ~ ~ ~ 0.38 1.3
execute as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/apply
scoreboard players set #sub itv 0
