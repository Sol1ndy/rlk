execute unless data storage rlk:dbg list[0] run return 0
execute if score #dbgShown tmp matches 12.. run return 0
data modify storage rlk:dbg id set from storage rlk:dbg list[0]
scoreboard players add #dbgIdx tmp 1
scoreboard players add #dbgShown tmp 1
execute store result storage rlk:dbg idx int 1 run scoreboard players get #dbgIdx tmp
function rlk:items/debug_color with storage rlk:dbg
function rlk:items/debug_line with storage rlk:dbg
data remove storage rlk:dbg list[0]
function rlk:items/debug_loop
