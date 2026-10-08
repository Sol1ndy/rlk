# @s = 깃발, at @s. 반경 4칸 영역: 몸이 안에 있으면 공격력 증가(#flagIn), 1초마다 회복
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st8 tmp
execute if score #t1 itv matches 0 run function rlk:items/proc/flag_ring
execute positioned ~ ~-1.2 ~ unless entity @e[tag=rlk_body,distance=..4] run return 0
scoreboard players set #flagIn itv 3
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st20 tmp
execute if score #t1 itv matches 0 as @a[tag=player,limit=1] run function rlk:items/proc/flag_heal
