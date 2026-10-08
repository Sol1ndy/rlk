# @s = 군기, at @s. 반경 4칸 안에 몸이 있으면 #gflagIn (방어력·바위 원소 피해 증가)
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st8 tmp
execute if score #t1 itv matches 0 positioned ~ ~-1.0 ~ run function rlk:items/proc/gflag_ring
execute positioned ~ ~-1.2 ~ if entity @e[tag=rlk_body,distance=..4] run scoreboard players set #gflagIn itv 3
