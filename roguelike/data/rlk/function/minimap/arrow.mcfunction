# The map rows (storage base) + the player arrow + the trailing position space -> boss bar.
scoreboard players operation #mmDirS mm = #mmDir mm
data modify storage rlk:mm line set from storage rlk:mm base
execute if score #pc mm matches 0.. run function rlk:minimap/arrow_put
execute if score #mmX mm matches ..-1 run function rlk:minimap/offset
bossbar set rlk:minimap name {nbt:"line[]",storage:"rlk:mm",interpret:true,separator:""}
