execute unless block ~ ~ ~ #rlk:view_pass run return run tp @e[tag=rlk_aim,limit=1] ~ ~ ~
execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[tag=rlk_mob,dx=0,dy=0,dz=0,limit=1] run return run tp @e[tag=rlk_aim,limit=1] ~0.5 ~0.5 ~0.5
scoreboard players add #ai view 1
execute if score #ai view matches 64.. run return run tp @e[tag=rlk_aim,limit=1] ~ ~ ~
execute positioned ^ ^ ^0.5 run function rlk:view/aim_step
