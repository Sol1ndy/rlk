scoreboard players set #hold tmp 1
# a hit that staggers it during the glint cancels the slash (still counts as an ambush)
execute if score #free tmp matches 0 run return run function rlk:cm/nj/v_cancel
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 5 run particle minecraft:end_rod ^-0.3 ^1.7 ^0.3 0 0 0 0 1
execute if score @s cmT matches ..0 run function rlk:cm/nj/v_slash
