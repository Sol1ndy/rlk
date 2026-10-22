# #mmNew: player cell + zone states + door states folded into one number.
execute store result score #cx mm run data get entity @e[tag=rlk_body,limit=1] Pos[0]
execute store result score #cz mm run data get entity @e[tag=rlk_body,limit=1] Pos[2]
function rlk:minimap/cell_index
scoreboard players operation #pc mm = #idx mm
scoreboard players operation #mmNew mm = #idx mm
scoreboard players set #c31 mm 31
execute as @e[tag=rlk_zone] run function rlk:minimap/sig_zone
execute as @e[tag=rlk_door] run function rlk:minimap/sig_door
