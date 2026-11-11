# @s = body, instead of the hook tick while groggy: the clock, the looks, the ambience; a floor reached now is
# reserved and cuts the groggy to its kip-up (grgT 20); down (loop) once grog_in ended, kipup in the last 20 t;
# hittable all along. Her hits' events are dropped (no gauge charge while groggy).
scoreboard players add #clk hr 1
function rlk:boss/scarlet/core/look
execute if score #mbFloorHit mb matches 1 run function rlk:boss/scarlet/core/floor_hit
execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run function rlk:boss/scarlet/core/floor_hit
execute if score #fl hr matches 1.. if score @s grgT matches 21.. run scoreboard players set @s grgT 20
function rlk:boss/scarlet/core/amb
function rlk:boss/scarlet/core/inv
function rlk:boss/scarlet/core/ev0
execute if score @s grgT matches 88 run function rlk:boss/scarlet/rig/play/down
execute if score @s grgT matches 20 run function rlk:boss/scarlet/rig/play/kipup
function rlk:boss/scarlet/rig/tick
