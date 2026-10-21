# cancel P9: its hazards (rlk_mb_az_p9h) expire, its markers and props go
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,tag=rlk_mb_az_p9h] at @s rotated as @s run function rlk:mboss/hz/expire
kill @e[tag=rlk_mb_az_p9m]
# the body comes back up (fight state only: death sets its own proxy state)
execute if score #mbSt mb matches 1 run function rlk:mboss/azhdaha/px/normal
execute if score #mbSt mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/azhdaha/rig/play/idle
