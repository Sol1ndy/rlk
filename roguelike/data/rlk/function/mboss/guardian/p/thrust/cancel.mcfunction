# P1 cancel (any executor): markers and cubes by tag; a glide of the body stops.
kill @e[tag=rlk_mb_gd_p1]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_mv] run function rlk:mboss/mv/stop
scoreboard players set #gp1S mb 0
