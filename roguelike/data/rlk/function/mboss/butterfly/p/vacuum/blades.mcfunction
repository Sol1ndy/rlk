# Core hook (ai/state, while #bp4B >= 1): every flying vacuum blade, then their count.
scoreboard players set #bp4B mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4b] at @s run function rlk:mboss/butterfly/p/vacuum/blade
