# E7 ST2: the stage origin facing her landing mark (toward the moon when that point passes mv/ok, else as ST) (@s = the body).
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage2"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] at @s rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] at @s facing 889.0 201 -34.0 positioned ^ ^ ^9 if function rlk:mboss/mv/ok at @s facing 889.0 201 -34.0 run tp @s ~ ~ ~ ~ 0
execute store result storage rlk:hr seq.face.yaw float 0.01 run data get entity @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] Rotation[0] 100
