# Q4 cancel (any executor; idempotent): its hazards, markers and props, the shared lock /
# probe markers, the glide; she is back on the floor (inside mv/ok) with the rest looks.
kill @e[tag=rlk_kn_p_q4]
kill @e[type=minecraft:marker,tag=rlk_kn_lock]
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
kill @e[type=minecraft:marker,tag=rlk_mb_lock]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1,tag=rlk_mb_mv] run function rlk:mboss/mv/stop
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/arlecchino/core/ground
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/arlecchino/core/looks_rest
scoreboard players set #q4_s kn 0
