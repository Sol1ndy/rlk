# 빙결 해제 (@s)
scoreboard players set @s frzT 0
particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.1 20
execute unless score #k36 snd matches 1 run function rlk:snd/f38
execute if entity @s[type=minecraft:player] run attribute @s minecraft:movement_speed modifier remove rlk:frozen
execute if entity @s[type=minecraft:player] run return run attribute @s minecraft:jump_strength modifier remove rlk:frozen
execute on passengers if entity @s[tag=rlk_frz_ice] run kill @s
execute unless entity @s[tag=rlk_noai] run data merge entity @s {NoAI:0b}
tag @s remove rlk_noai
tag @s remove rlk_frz_fix
