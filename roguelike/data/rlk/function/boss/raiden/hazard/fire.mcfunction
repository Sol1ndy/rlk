# The hit / launch tick: the decal goes, the strike visual comes (static kinds), the test runs.
execute if score @s rdHDk matches 1.. unless score @s rdHK matches 8..9 run function rlk:boss/raiden/hazard/vis/decal_off
execute if score @s rdHSv matches 1.. unless score @s rdHK matches 5..8 run function rlk:boss/raiden/hazard/vis/strike
execute if score @s rdHSnd matches 1.. unless score @s rdHK matches 5..9 run function rlk:boss/raiden/hazard/snd
function rlk:boss/raiden/hazard/try
