# whip #azPT 25
execute unless score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:mboss/azhdaha/p/whip/l/25
execute if score #aq7S mb matches -1 at @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run function rlk:mboss/azhdaha/p/whip/r/25
scoreboard players set #azNoPush mb 1
