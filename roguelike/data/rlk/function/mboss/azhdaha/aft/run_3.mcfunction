scoreboard players operation #azAftX mb = #azAft3 mb
scoreboard players set #azAft3 mb 0
scoreboard players remove #azAftN mb 1
execute at @e[type=minecraft:marker,tag=rlk_az_aft3,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_az_aft3,limit=1] run function rlk:mboss/azhdaha/aft/fn
kill @e[type=minecraft:marker,tag=rlk_az_aft3]
