# One fight tick (@s = body): the module clock, the look requests, the floor, the state of the phase, invulnerability.
scoreboard players add #clk hr 1
function rlk:boss/scarlet/core/look
execute if score #mbFloorHit mb matches 1 run function rlk:boss/scarlet/core/floor_hit
execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run function rlk:boss/scarlet/core/floor_hit
function rlk:boss/scarlet/core/state
execute if score #mbSt mb matches 1 run function rlk:boss/scarlet/core/inv
