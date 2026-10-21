# 발광하는 파수꾼 cut (any executor; idempotent): its markers, hazards and props go.
kill @e[tag=rlk_mb_ap_p3]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/mv/stop
