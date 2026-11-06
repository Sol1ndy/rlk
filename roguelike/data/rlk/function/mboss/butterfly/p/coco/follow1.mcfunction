# @s = orb 2, at it: its ring displays (or the rig orb prop) ride along; the kit rings spin.
# (to where the pj step puts the orb this tick: 0.25 b along its flight, so they never lag it)
execute if score @s mbT matches ..39 positioned ^ ^ ^0.25 as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14r1a,limit=1] rotated as @s run tp @s ~ ~ ~ ~15 ~
execute if score @s mbT matches ..39 positioned ^ ^ ^0.25 as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14r1b,limit=1] rotated as @s run tp @s ~ ~ ~ ~-12 ~
execute if score @s mbT matches ..39 positioned ^ ^ ^0.25 as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14v1] run tp @s ~ ~ ~
execute if score @s mbT matches 40.. as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14r1a,limit=1] rotated as @s run tp @s ~ ~ ~ ~6 ~
execute if score @s mbT matches 40.. as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14r1b,limit=1] rotated as @s run tp @s ~ ~ ~ ~-5 ~
