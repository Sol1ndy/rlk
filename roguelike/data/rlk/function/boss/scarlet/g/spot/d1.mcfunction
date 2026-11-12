# Spot d1 (@s = the body): D1 far reappear: 14 b at -40 (front-left); else +40 / 0 / +-90 at 10 b. The first candidate passing mv/ok (MOVE_R 22.5, feet and head
# free) gets the marker rlk_hr_gsp; else the guaranteed fallback 14 b from the player toward C (at most 21 b from C), walked toward the axis until mv/ok passes.
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~-40 0 positioned ^ ^ ^14 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~40 0 positioned ^ ^ ^10 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~0 0 positioned ^ ^ ^10 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~90 0 positioned ^ ^ ^10 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~-90 0 positioned ^ ^ ^10 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^14 run function rlk:boss/scarlet/g/spot/put
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..21] at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^21 run tp @s ~ ~ ~
scoreboard players set #g_c hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s run function rlk:boss/scarlet/g/spot/clamp
