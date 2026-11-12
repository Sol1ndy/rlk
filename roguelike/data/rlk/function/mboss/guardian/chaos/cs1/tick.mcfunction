# Stream 1 (any executor). Followers tail first: each takes its predecessor's place of the last tick
# (or the lead's, once the predecessor popped); then the lead moves; then the pop at a landed lead.
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run return run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_11,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_10,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_11,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_10,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_10,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_9,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_10,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_9,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_9,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_8,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_9,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_8,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_8,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_7,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_8,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_7,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_7,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_6,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_7,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_6,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_6,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_5,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_6,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_5,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_5,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_4,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_5,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_4,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_4,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_3,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_4,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_3,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_3,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_2,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_3,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_2,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_2,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_1,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_2,limit=1] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_1,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_1,limit=1] at @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] at @s run function rlk:mboss/guardian/chaos/cs_head
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] if entity @s[tag=rlk_mb_gd_csend] at @s as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1,tag=!rlk_mb_gd_csh,distance=..0.05] at @s run function rlk:mboss/guardian/chaos/cs_pop
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] if entity @s[tag=rlk_mb_gd_csend] unless entity @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1,tag=!rlk_mb_gd_csh] run kill @s
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1_0,limit=1] if score @s mbT matches 80.. run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs1]
