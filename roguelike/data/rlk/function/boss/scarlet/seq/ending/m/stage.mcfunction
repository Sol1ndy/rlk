# The stage of this sequence (hr_design §3.0; FMAX 12) (@s = the body).
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
function rlk:mboss/mv/dist
execute if score #mbDist mb matches ..6 as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s positioned ^ ^ ^12 unless function rlk:mboss/mv/ok at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
