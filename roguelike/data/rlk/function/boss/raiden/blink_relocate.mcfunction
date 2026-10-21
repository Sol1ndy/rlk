# Hidden middle of a blink (movement/blink_tick). A destination marker wins; otherwise reform 5 blocks ahead of the
# player, or 5 blocks from the player toward the centre.
execute if entity @e[tag=rlk_rd_blink_dest,limit=1] run return run function rlk:boss/raiden/blink_dest
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] run tp @s ~ ~ ~
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
