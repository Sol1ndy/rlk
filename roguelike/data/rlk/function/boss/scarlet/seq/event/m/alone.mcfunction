# The coda without the ending before it: its own stage (ST2 = ST) and stands, camera A on its shot (@s = the body).
function rlk:boss/scarlet/seq/event/m/stage
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage2"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] at @s rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:mboss/cam/spawn
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] run tp @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] ^-0.55 ^1.75 ^-1.3
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] facing ^0 ^1.3 ^0
scoreboard players set #mbCamId mb 1
