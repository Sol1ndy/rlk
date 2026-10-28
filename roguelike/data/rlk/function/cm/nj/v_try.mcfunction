$execute as @e[tag=rlk_c2cur,limit=1] at @e[tag=rlk_body,limit=1] rotated ~$(a) 0 run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/drop
scoreboard players set #wN tmp 6
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/walk
execute if score #wK tmp matches 4.. run scoreboard players set #c2ok tmp 1
