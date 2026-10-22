scoreboard players operation #azAftX mb = #azAft6 mb
scoreboard players set #azAft6 mb 0
scoreboard players remove #azAftN mb 1
tag @e[type=minecraft:marker,tag=rlk_az_aft6] add rlk_az_aftrun
tag @e[type=minecraft:marker,tag=rlk_az_aftrun] remove rlk_az_aft6
execute at @e[type=minecraft:marker,tag=rlk_az_aftrun,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_aftrun,limit=1] run function rlk:boss/azhdaha/aft/fn
kill @e[type=minecraft:marker,tag=rlk_az_aftrun]
