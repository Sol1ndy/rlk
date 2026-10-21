# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# 0 emerging (30 t), 1 rolling to the Heart (0.1 b/t) until r 2.6, 2 the fuse (56 t) ->
# the blast (-1400, no progress).
execute if score @s apS matches 0 if score @s apT matches 30.. run scoreboard players set @s apS 1
execute if score @s apS matches 1 if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..2.6,limit=1] run return run function rlk:boss/apep/org/b_arrive
execute if score @s apS matches 1 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run function rlk:mboss/mv/step_flat {spd:0.1}
execute if score @s apS matches 2 if score @s apT matches 56.. run return run function rlk:boss/apep/org/d_blast
