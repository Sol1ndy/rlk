# @s = body, instead of the hook tick while groggy: the clock, the looks, the ambience, the rig (kipup at the end).
scoreboard players add #clk hr 1
function rlk:boss/scarlet/core/look
function rlk:boss/scarlet/core/amb
function rlk:boss/scarlet/core/inv
execute if score @s grgT matches 20 run function rlk:boss/scarlet/rig/play/kipup
function rlk:boss/scarlet/rig/tick
