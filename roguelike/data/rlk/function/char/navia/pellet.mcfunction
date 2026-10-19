execute if score #ps tmp matches ..0 run return 0
scoreboard players remove #ps tmp 1
execute unless block ~ ~ ~ #rlk:dash_pass run return run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~ ~ 0.1 0.1 0.1 0.1 4
particle minecraft:dust{color:[1.0,0.80,0.35],scale:0.7} ~ ~ ~ 0 0 0 0 1
execute if score #ps tmp matches 20 run particle minecraft:wax_on ~ ~ ~ 0.05 0.05 0.05 0 1
execute positioned ~-0.75 ~-0.75 ~-0.75 run tag @e[tag=rlk_mob,tag=!rlk_mb_px,dx=0.5,dy=0.5,dz=0.5] add rlk_np
execute positioned ~-0.75 ~-0.75 ~-0.75 if entity @e[tag=rlk_mb_px,tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5,limit=1] run tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_np
execute positioned ^ ^ ^0.5 run function rlk:char/navia/pellet
