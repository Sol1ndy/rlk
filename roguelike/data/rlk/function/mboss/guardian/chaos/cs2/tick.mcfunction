# Stream 2 (any executor). Followers tail first: each takes its predecessor's place of the last tick
# (or the lead's, once the predecessor popped); then the lead moves; then the pop at a landed lead.
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run return run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_11,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_10,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_11,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_10,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_10,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_9,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_10,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_9,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_9,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_8,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_9,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_8,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_8,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_7,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_8,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_7,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_7,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_6,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_7,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_6,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_6,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_5,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_6,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_5,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_5,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_4,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_5,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_4,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_4,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_3,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_4,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_3,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_3,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_2,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_3,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_2,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_2,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_1,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_2,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_1,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_1,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] at @s run function rlk:mboss/guardian/chaos/cs_head
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] if entity @s[tag=rlk_mb_gd_csend] at @s as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2,tag=!rlk_mb_gd_csh,distance=..0.05] at @s run function rlk:mboss/guardian/chaos/cs_pop
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] if entity @s[tag=rlk_mb_gd_csend] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2,tag=!rlk_mb_gd_csh] run kill @s
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2_0,limit=1] if score @s mbT matches 80.. run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs2]
