kill @e[type=minecraft:marker,tag=rlk_az_aft10]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_aft","rlk_az_aft10"]}
execute rotated ~ ~ as @e[type=minecraft:marker,tag=rlk_az_aft10,limit=1] run tp @s ~ ~ ~ ~ ~
scoreboard players operation #azAft10 mb = #azAftF mb
scoreboard players operation #azAftT10 mb = #azClk mb
scoreboard players operation #azAftT10 mb += #azAftD mb
scoreboard players add #azAftN mb 1
