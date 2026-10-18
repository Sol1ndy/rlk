# Module tick / intro_tick / death_tick while #bfTcN >= 1: the engine clock, age every card, recount.
scoreboard players add #bfTcNow mb 1
scoreboard players set #bfTcN mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_tc] run function rlk:mboss/butterfly/tc/tick
