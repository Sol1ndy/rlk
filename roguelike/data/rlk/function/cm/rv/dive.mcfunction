scoreboard players operation @s cmT -= #eStep tmp
execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_rv_tsel
execute unless entity @e[tag=rlk_rv_tsel,limit=1] run return run function rlk:cm/rv/d_abort
scoreboard players set #c2s tmp 3
execute if score #eStep tmp matches 2 run scoreboard players add #c2s tmp 1
function rlk:cm/rv/dv_step
execute at @s run particle minecraft:flame ~ ~0.7 ~ 0.25 0.25 0.25 0.02 4
execute at @s run particle minecraft:large_smoke ~ ~0.7 ~ 0.15 0.15 0.15 0.01 1
execute if score @s cmS matches 3 if score @s cmT matches ..0 run function rlk:cm/rv/d_abort
tag @e[tag=rlk_rv_tsel] remove rlk_rv_tsel
