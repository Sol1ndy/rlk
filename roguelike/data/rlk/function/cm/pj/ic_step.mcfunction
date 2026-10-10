execute at @s run tp @s ~ ~-0.35 ~
scoreboard players set #pj tmp 0
execute at @s unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #pj tmp 2
execute at @s positioned ~-0.55 ~-0.55 ~-0.55 as @e[tag=rlk_body,dx=0,dy=0,dz=0] positioned ~0.1 ~0.1 ~0.1 if entity @s[dx=0,dy=0,dz=0] run scoreboard players set #pj tmp 1
execute if score #pj tmp matches 1.. at @s run return run function rlk:cm/pj/ic_boom
scoreboard players remove #pst tmp 1
execute if score #pst tmp matches 1.. run function rlk:cm/pj/ic_step
