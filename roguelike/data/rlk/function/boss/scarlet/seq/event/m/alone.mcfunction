# The coda without the ending before it: its own stage (ST2 = ST) and stands, its first shot's stand live at once (@s = the body).
function rlk:boss/scarlet/seq/event/m/stage
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage2"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] at @s rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^0.45 ^1.6 ^1.6
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.55 ^0
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^0.45 ^1.6 ^1.6
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.55 ^0
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
scoreboard players set #mbCamId mb 2
