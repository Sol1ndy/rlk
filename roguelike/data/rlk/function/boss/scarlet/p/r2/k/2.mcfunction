# R2 pattern tick 2.
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/scarlet/fx/p/yellow_tell {t:8}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
