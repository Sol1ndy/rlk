# glow #apPT 23
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:16}
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/shadow_glide
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3 run function rlk:boss/apep/fx/p/shadow_glide
