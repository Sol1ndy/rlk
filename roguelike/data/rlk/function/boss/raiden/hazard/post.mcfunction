# After the hit: travelling hazards test every tick until their front passed `reach`; follow / field every rdHEv.
execute if score @s rdHK matches 5..7 if score #rdRel rd > @s rdHF run return run function rlk:boss/raiden/hazard/expire
execute if score @s rdHK matches 5..7 run return run function rlk:boss/raiden/hazard/try
execute if score @s rdHK matches 8..9 run function rlk:boss/raiden/hazard/try_every
