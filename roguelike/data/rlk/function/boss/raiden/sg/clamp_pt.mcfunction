# Pull the point markers (rlk_rd_sgpt) in to radius 20 about the arena centre.
execute as @e[tag=rlk_rd_sgpt] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~
