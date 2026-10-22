# @s = body: beyond 27 b from the axis of az_cavern slide back 0.45 b/t; beyond 30 b back home.
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_mb_arena,distance=..27,limit=1] run return 0
execute at @s positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..30,limit=1] run return run function rlk:mboss/mv/home
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
