# Q2 stage main tick 20
function rlk:boss/arlecchino/p/q2/wheel
execute at @s run function rlk:boss/arlecchino/fx/snd/wheel_throw
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/wheel_trail {len:150}
