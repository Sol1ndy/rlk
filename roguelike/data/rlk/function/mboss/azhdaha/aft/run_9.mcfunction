scoreboard players operation #azAftX mb = #azAft9 mb
scoreboard players set #azAft9 mb 0
scoreboard players remove #azAftN mb 1
tag @e[type=minecraft:marker,tag=rlk_az_aft9] add rlk_az_aftrun
tag @e[type=minecraft:marker,tag=rlk_az_aftrun] remove rlk_az_aft9
execute at @e[type=minecraft:marker,tag=rlk_az_aftrun,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_aftrun,limit=1] run function rlk:mboss/azhdaha/aft/fn
kill @e[type=minecraft:marker,tag=rlk_az_aftrun]
