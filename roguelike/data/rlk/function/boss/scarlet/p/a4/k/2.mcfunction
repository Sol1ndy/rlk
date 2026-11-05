# A4 pattern tick 2
function rlk:boss/scarlet/p/a4/leap
execute at @s run function rlk:boss/scarlet/fx/snd/leap
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:60}
