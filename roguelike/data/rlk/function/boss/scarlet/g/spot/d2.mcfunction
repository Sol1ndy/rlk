# Spot d2 (@s = the body): D2 side reappear: 8 b at +55 (low, the player's front-right); else -55 / 0 / +-55 at 6 b. The first candidate passing mv/ok (MOVE_R 22.5, feet and head
# free) gets the marker rlk_hr_gsp; else the guaranteed fallback 8 b from the player toward C (at most 21 b from C), walked toward the axis until mv/ok passes.
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~55 0 positioned ^ ^ ^8 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~-55 0 positioned ^ ^ ^8 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~0 0 positioned ^ ^ ^8 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~55 0 positioned ^ ^ ^6 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @a[tag=player,limit=1] rotated ~-55 0 positioned ^ ^ ^6 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^8 run function rlk:boss/scarlet/g/spot/put
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..21] at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^21 run tp @s ~ ~ ~
scoreboard players set #g_c hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s run function rlk:boss/scarlet/g/spot/clamp
