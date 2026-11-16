scoreboard players add #ccN tmp 1
execute if score #c2hs tmp matches 1 run tag @s add rlk_cm_haste
execute if score #c2hs tmp matches 0 run tag @s remove rlk_cm_haste
function rlk:cm/ci/own_tick
execute if score @s cmS matches 1.. run scoreboard players set #ccR tmp 1
execute if score @s cmS matches 0 unless score @s frzT matches 1.. run tag @s add rlk_ci_idle
