execute if score #apSlots mb matches 3.. run return 0
scoreboard players add #apSlots mb 1
execute if entity @s[tag=!rlk_mb_ap_rng] if score @s apT matches ..39 run return 0
execute if entity @s[tag=rlk_mb_ap_rng] if score @s apT matches ..49 run return 0
scoreboard players set @s apT 0
execute if entity @s[tag=rlk_mb_ap_buff] run return run function rlk:boss/apep/heart/sub {v:120}
function rlk:boss/apep/heart/sub {v:60}
