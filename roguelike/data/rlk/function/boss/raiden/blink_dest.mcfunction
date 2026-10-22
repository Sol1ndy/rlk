execute at @e[tag=rlk_rd_blink_dest,limit=1] run tp @s ~ ~ ~
kill @e[tag=rlk_rd_blink_dest]
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
