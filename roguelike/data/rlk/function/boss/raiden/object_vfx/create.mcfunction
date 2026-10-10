# Call once as every newly created gameplay object, including flower/illusion.
scoreboard players add #rdObjectSerial rd 1
scoreboard players operation @s rdOvId = #rdObjectSerial rd
execute if score @s rdObjKind matches 1 run function rlk:boss/raiden/object_vfx/eye
execute if score @s rdObjKind matches 4 run function rlk:boss/raiden/object_vfx/stake
