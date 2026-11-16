kill @e[type=minecraft:marker,tag=rlk_az_aft2]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_aft","rlk_az_aft2"]}
execute rotated ~ ~ as @e[type=minecraft:marker,tag=rlk_az_aft2,limit=1] run tp @s ~ ~ ~ ~ ~
scoreboard players operation #azAft2 mb = #azAftF mb
scoreboard players operation #azAftT2 mb = #azClk mb
scoreboard players operation #azAftT2 mb += #azAftD mb
scoreboard players add #azAftN mb 1
