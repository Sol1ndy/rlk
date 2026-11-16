# @s = body: beyond 25 b from the axis of ap_oasis slide back 0.45 b/t; beyond 28 b back home.
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_mb_arena,distance=..25,limit=1] run return 0
execute at @s positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..28,limit=1] run return run function rlk:mboss/mv/home
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
