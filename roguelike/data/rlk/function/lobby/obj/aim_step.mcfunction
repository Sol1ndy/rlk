execute as @e[tag=rlk_lobj,distance=..1.0,limit=1,sort=nearest] run return run tag @s add rlk_lhover
scoreboard players add #lray lob 1
execute if score #lray lob matches 50.. run return 0
execute positioned ^ ^ ^0.35 run function rlk:lobby/obj/aim_step
