$execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~$(a) 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/pc/lib/drop
scoreboard players set #wN tmp 4
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/pc/lib/walk
execute if score #wK tmp matches 3.. run scoreboard players set #c2ok tmp 1
