scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 8
scoreboard players operation #shFrame tmp %= #shDiv tmp
scoreboard players set #shDiv tmp 2
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
scoreboard players add #shPose tmp 40
# Sparks are tied to the actual shield edge and disappear when the shield breaks.
execute if score @s cmSh matches 1.. rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-0.7 ^0.045 ^0.9 run particle minecraft:crit ~ ~ ~ 0.04 0.005 0.08 0.025 2
