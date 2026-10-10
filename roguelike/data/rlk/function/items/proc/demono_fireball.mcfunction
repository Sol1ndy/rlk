# @s = 플레이어, at @s. 서리 화살: 가장 가까운 적(16)에게 얼음 화살 (예전의 추적 화염구. 함수 이름은 그대로 둠)
execute unless entity @e[tag=rlk_mob,distance=..16] run return 0
function rlk:items/proc/demono_dmg
scoreboard players set #elem tmp 4
particle minecraft:snowflake ~ ~1.2 ~ 0.2 0.2 0.2 0.03 10
execute unless score #k161 snd matches 1 run function rlk:snd/f170
execute unless score #k162 snd matches 1 run function rlk:snd/f171
execute as @e[tag=rlk_mob,distance=..16,sort=nearest,limit=1] at @s run function rlk:items/proc/demono_fireball_hit
