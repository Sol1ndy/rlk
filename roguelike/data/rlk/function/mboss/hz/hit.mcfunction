# @s = hazard marker, at @s, inside its active window. Body feet only (never the camera).
scoreboard players set #hzHit mb 0
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #dy mb run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #t mb run data get entity @s Pos[1] 1000
scoreboard players operation #dy mb -= #t mb
execute if score #dy mb < @s mbHzY0 run return 0
execute if score #dy mb > @s mbHzY1 run return 0
execute if score @s mbHzK matches 5 run return run function rlk:mboss/hz/hit_full
execute if score @s mbHzK matches 6 run return run function rlk:mboss/hz/hit_mask
execute unless entity @e[tag=rlk_body,distance=..48,limit=1] run return 0
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #t mb
# Projections on the frozen forward axis (fwd) and its left normal (side), milliblocks.
scoreboard players operation #fwd mb = #dx mb
scoreboard players operation #fwd mb *= @s mbHzFX
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= @s mbHzFZ
scoreboard players operation #fwd mb += #t mb
scoreboard players operation #fwd mb /= #c1000 mb
execute if score @s mbHzK matches 4 run return run function rlk:mboss/hz/k4
# Radial shapes: distance squared (safe from overflow inside 32 blocks).
execute unless entity @e[tag=rlk_body,distance=..32,limit=1] run return 0
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb > @s mbHzRR run return 0
execute if score #r2 mb < @s mbHzRI run return 0
execute if score @s mbHzK matches 1..2 run return run function rlk:mboss/hz/hurt
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/k3
