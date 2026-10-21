# World: as each hazard at its origin and frozen yaw. #rdRel = ticks since the hit / launch (negative before).
scoreboard players add @s rdHAge 1
execute if score @s rdHAge >= @s rdHLife run return run function rlk:boss/raiden/hazard/expire
scoreboard players operation #rdRel rd = @s rdHAge
scoreboard players operation #rdRel rd -= @s rdWind
execute if score @s rdHK matches 8 run function rlk:boss/raiden/hazard/k/follow_move
execute if score #rdRel rd matches ..-1 run return run function rlk:boss/raiden/hazard/pre
execute if score #rdRel rd matches 0 run return run function rlk:boss/raiden/hazard/fire
function rlk:boss/raiden/hazard/post
