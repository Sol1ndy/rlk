# Before the hit: travelling cards appear one tick before the launch; a decal with its own life ends.
execute if score #rdRel rd matches -1 if score @s rdHK matches 5..7 run function rlk:boss/raiden/hazard/vis/travel
execute if score @s rdHDl matches 1.. if score @s rdHAge = @s rdHDl run function rlk:boss/raiden/hazard/vis/decal_off
