# A10 pattern tick 10
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run function rlk:boss/scarlet/fx/p/yellow_tell {t:8}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
