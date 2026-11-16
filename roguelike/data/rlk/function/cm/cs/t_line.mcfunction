execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #n tmp 7
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.1 ^0.6 run function rlk:cm/cs/t_lstep
