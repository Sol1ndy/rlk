# @s = a 수호 (immobile): 1 the cast (guard_cast: collapse 0, bud 7, regrow 16, shields 30), 2 idle; recasts every 240 t on unshielded basics within r 10.
execute if score @s apS matches 1 run return run function rlk:boss/apep/org/guard/cast
scoreboard players remove @s apTok 1
execute if score @s apTok matches 1.. run return 0
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_shd,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,distance=..10] run return run function rlk:boss/apep/org/guard/cast_go
scoreboard players set @s apTok 20
