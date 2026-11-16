# Back on the floor at once if she is above it (@s = body; a cancelled glide / hop): the spot below when it
# passes mv/ok, else the arena centre (never into a block, never below the floor).
execute store result score #t tk run data get entity @s Pos[1] 100
execute if score #t tk matches ..20104 run return 0
execute at @s positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run tp @s ~ ~ ~
