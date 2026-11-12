# The cast was cut (test, reload, a new cast): its markers, props and live hazards go (selectors only).
kill @e[tag=rlk_mb_az_p32]
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p32h] at @s run function rlk:mboss/hz/expire
