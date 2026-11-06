# whip #azPT 21
execute unless score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:boss/azhdaha/p/whip/l/21
execute if score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:boss/azhdaha/p/whip/r/21
scoreboard players set #azNoPush mb 1
