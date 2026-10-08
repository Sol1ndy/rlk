execute if score #dbgSkip tmp matches 1.. if data storage rlk:dbg list[0] run data remove storage rlk:dbg list[0]
execute if score #dbgSkip tmp matches 1.. run scoreboard players remove #dbgSkip tmp 1
execute if score #dbgSkip tmp matches 1.. run function rlk:items/debug_skip
