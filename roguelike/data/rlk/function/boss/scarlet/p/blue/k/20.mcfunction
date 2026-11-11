# BLUE pattern tick 20
function rlk:boss/scarlet/p/blue/dash
execute at @s run function rlk:boss/scarlet/fx/snd/lunge
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:90}
