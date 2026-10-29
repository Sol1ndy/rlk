# C3 cancel (any executor; idempotent): its hazards and markers, the body glide, the looks.
kill @e[tag=rlk_tk_p_c3]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1,tag=rlk_mb_mv] run function rlk:mboss/mv/stop
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/rig_stub/look/chest/off
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/el/edge
