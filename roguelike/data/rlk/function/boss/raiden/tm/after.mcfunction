# @s = the boss when a phase-2 pattern ends (finish, ON_FINISH): the idle clip, the rear-cone check for 20
# (+-60 deg of her back, <= 9 b: three discs inscribed in the cone) and the 40 % chain after 16 (17 or 11, cool 4).
function rlk:boss/raiden/tm/idle
tag @s remove rlk_rd_tm_rear
execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^2 if entity @e[tag=rlk_body,distance=..1.7] run tag @s add rlk_rd_tm_rear
execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^4.2 if entity @e[tag=rlk_body,distance=..3.6] run tag @s add rlk_rd_tm_rear
execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^6.5 if entity @e[tag=rlk_body,distance=..5.6] run tag @s add rlk_rd_tm_rear
execute at @s unless entity @e[tag=rlk_body,distance=..9] run tag @s remove rlk_rd_tm_rear
scoreboard players set @s rdTmChain 0
execute unless score @s rdPrev matches 16 run return 0
execute store result score #rdTmR rd run random value 0..99
execute if score #rdTmR rd matches ..19 run scoreboard players set @s rdTmChain 17
execute if score #rdTmR rd matches 20..39 run scoreboard players set @s rdTmChain 11
execute if score @s rdTmChain matches 1.. run scoreboard players set @s rdCool 4
