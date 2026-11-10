# KCUT pattern tick 20
function rlk:boss/scarlet/rig/look/blade/off
function rlk:boss/scarlet/p/kcut/dash
execute at @s run function rlk:boss/scarlet/fx/snd/kcut_go
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:100}
