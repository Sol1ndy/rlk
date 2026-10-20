kill @e[type=minecraft:marker,tag=rlk_az_aft1]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_aft","rlk_az_aft1"]}
execute rotated ~ ~ as @e[type=minecraft:marker,tag=rlk_az_aft1,limit=1] run tp @s ~ ~ ~ ~ ~
scoreboard players operation #azAft1 mb = #azAftF mb
scoreboard players operation #azAftT1 mb = #azClk mb
scoreboard players operation #azAftT1 mb += #azAftD mb
scoreboard players add #azAftN mb 1
