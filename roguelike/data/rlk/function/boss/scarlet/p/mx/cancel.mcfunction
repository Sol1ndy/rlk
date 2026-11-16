# MX cancel (any executor; idempotent): its hazards and markers, the body glide, the
# body back on the floor when airborne, the stance.
kill @e[tag=rlk_hr_p_mx]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1,tag=rlk_mb_mv] run function rlk:mboss/mv/stop
