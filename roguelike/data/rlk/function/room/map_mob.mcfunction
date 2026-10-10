scoreboard players add #mdi tmp 1
execute store result storage rlk:room mt.i int 1 run scoreboard players get #mdi tmp
execute store result storage rlk:room mt.x int 1 run data get entity @s Pos[0]
execute store result storage rlk:room mt.z int 1 run data get entity @s Pos[2]
data modify storage rlk:room mt.t set value "minecraft:target_point"
execute if entity @s[tag=boss] run data modify storage rlk:room mt.t set value "minecraft:red_x"
execute if entity @s[tag=miniboss] run data modify storage rlk:room mt.t set value "minecraft:red_x"
function rlk:room/map_mob2 with storage rlk:room mt
