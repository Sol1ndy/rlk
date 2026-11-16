# B1 pattern tick 28
function rlk:boss/arlecchino/p/b1/wheel
function rlk:boss/arlecchino/rig/look/weapon_r/gone
execute at @s run function rlk:boss/arlecchino/fx/snd/wheel_throw
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/wheel_trail {len:160}
