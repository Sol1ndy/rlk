# As the boss: the hands drift after the player (slower than a sprint).
execute as @e[tag=rlk_rd_clap] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.3 unless entity @e[tag=rlk_body,distance=..0.4] run tp @s ~ 201 ~
execute as @e[tag=rlk_rd_clap] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_raiden,limit=1] feet
execute as @e[tag=rlk_rd_clap] at @s rotated ~180 0 run tp @s ~ ~ ~ ~ 0
