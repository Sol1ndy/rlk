# Before the hit: travelling cards appear at rel rdHSp (min(tell, gap) ticks before the launch); a decal with its
# own life ends.
execute if score @s rdHK matches 5..7 if score #rdRel rd = @s rdHSp run function rlk:boss/raiden/hazard/vis/travel
execute if score @s rdHDl matches 1.. if score @s rdHAge = @s rdHDl run function rlk:boss/raiden/hazard/vis/decal_off
