# cancel P5: its hazards (rlk_mb_az_p5h) expire, its markers and props go
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,tag=rlk_mb_az_p5h] at @s rotated as @s run function rlk:mboss/hz/expire
kill @e[tag=rlk_mb_az_p5m]
