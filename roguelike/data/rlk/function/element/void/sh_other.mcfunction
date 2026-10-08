execute unless score @s rnId matches 1.. run function rlk:element/void/assign_id
scoreboard players operation #shTg tmp = @s rnId
execute at @e[tag=rlk_rnc,limit=1] run function rlk:element/void/sh_spawn
