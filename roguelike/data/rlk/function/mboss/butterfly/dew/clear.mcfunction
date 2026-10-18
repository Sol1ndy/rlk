# Every heal orb fades (the butterfly form ended).
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dew] at @s run particle minecraft:poof ~ ~ ~ 0.2 0.2 0.2 0.02 6 force @a[tag=player]
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]
scoreboard players set #bfDewN mb 0
