# #q4_r kn = the distance in tenths from the chest marker to the execution position (dx dy dz -> Newton square root).
execute store result score #q4_x kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] Pos[0] 10
execute store result score #q4_y kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] Pos[1] 10
execute store result score #q4_z kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] Pos[2] 10
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q4","rlk_kn_q4t"]}
execute store result score #q4_r kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[0] 10
scoreboard players operation #q4_x kn -= #q4_r kn
execute store result score #q4_r kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[1] 10
scoreboard players operation #q4_y kn -= #q4_r kn
execute store result score #q4_r kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[2] 10
scoreboard players operation #q4_z kn -= #q4_r kn
kill @e[type=minecraft:marker,tag=rlk_kn_q4t]
scoreboard players operation #q4_x kn *= #q4_x kn
scoreboard players operation #q4_y kn *= #q4_y kn
scoreboard players operation #q4_z kn *= #q4_z kn
scoreboard players operation #q4_x kn += #q4_y kn
scoreboard players operation #q4_x kn += #q4_z kn
scoreboard players set #q4_r kn 250
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
scoreboard players operation #q4_y kn = #q4_x kn
scoreboard players operation #q4_y kn /= #q4_r kn
scoreboard players operation #q4_r kn += #q4_y kn
scoreboard players operation #q4_r kn /= #c2 kn
execute if score #q4_r kn matches ..0 run scoreboard players set #q4_r kn 1
