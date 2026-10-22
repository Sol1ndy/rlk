# The dungeon box is not loaded yet (forceloaded chunks load within a few ticks): wait, 200 t -> abort.
scoreboard players add #rdBgW rd 1
execute if score #rdBgW rd matches 200.. run return run scoreboard players set #rdBgI rd -1
schedule function rlk:room/raiden/bg/tick 1t replace
