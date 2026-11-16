# @s = body, positioned at a proposed step: there if it stays inside the glide disc r 16 (yaw kept).
execute positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..16,limit=1] run return fail
tp @s ~ 201 ~
