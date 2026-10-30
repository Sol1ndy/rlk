# @s = body: to the arena centre at once, facing the player (the field).
tp @s @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
