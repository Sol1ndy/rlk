execute as @e[tag=rlk_obj,distance=..0.95,limit=1,sort=nearest] run return run tag @s add rlk_ohover
scoreboard players add #oray tmp 1
execute if score #oray tmp >= #rObj view run return 0
execute positioned ^ ^ ^0.35 run function rlk:room/obj/aim_step
