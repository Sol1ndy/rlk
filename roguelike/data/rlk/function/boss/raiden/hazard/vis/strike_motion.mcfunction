# rdHSm 1 / 2: the strike starts turned SM_SWEEP deg toward her left / right (model +X = her left) and sweeps
# into place behind the blade; 3 drops 1 b; 4 runs out from the origin (rect / to_wall); 5 grows up from the floor.
execute if score @s rdHSm matches 1 run data modify storage rlk:rd v.lr0 set value "[0f,0.42262f,0f,0.90631f]"
execute if score @s rdHSm matches 2 run data modify storage rlk:rd v.lr0 set value "[0f,-0.42262f,0f,0.90631f]"
execute if score @s rdHSm matches 3 run data modify storage rlk:rd v.ty0 set value 1.0f
execute if score @s rdHSm matches 4 store result storage rlk:rd v.sz0 float 0.00015 run scoreboard players get #rdSz rd
execute if score @s rdHSm matches 5 run data modify storage rlk:rd v.sy0 set value 1.20f
