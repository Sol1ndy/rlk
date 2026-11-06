# Every live heal orb (module tick while #bfDewN >= 1): shimmer, pickup.
scoreboard players set #bfDewN mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dew] at @s run function rlk:mboss/butterfly/dew/tick
