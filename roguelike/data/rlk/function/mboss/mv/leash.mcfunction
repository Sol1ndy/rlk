# @s = body (automatic every fight tick unless #mbNoLeash mb 1): the fight arena's leash. A chapter arena (#mbAr >= 1)
# through F:mboss/ar/<aid>/leash; the plaza's lines (the M0 text, = ar/plaza/leash) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/leash
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_mb_arena,distance=..20,limit=1] run return 0
execute at @s positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..23,limit=1] run return run function rlk:mboss/mv/home
execute at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
