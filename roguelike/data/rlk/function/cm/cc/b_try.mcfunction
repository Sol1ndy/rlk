$execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~$(a) 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #wN tmp 12
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cc/lib/walk
execute if score #wK tmp matches 8.. run scoreboard players set #c2ok tmp 1
