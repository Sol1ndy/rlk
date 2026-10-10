execute at @s run tp @s ^ ^ ^0.4
scoreboard players set #pj tmp 0
execute at @s unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #pj tmp 2
execute at @s positioned ~-0.6 ~-0.6 ~-0.6 as @e[tag=rlk_body,dx=0,dy=0,dz=0] positioned ~0.19999999999999996 ~0.19999999999999996 ~0.19999999999999996 if entity @s[dx=0,dy=0,dz=0] run scoreboard players set #pj tmp 1
execute if score #pj tmp matches 1 at @s run return run function rlk:cm/pj/fb_hit
execute if score #pj tmp matches 2 at @s run return run function rlk:cm/pj/fb_wall
scoreboard players remove #pst tmp 1
execute if score #pst tmp matches 1.. run function rlk:cm/pj/fb_step
