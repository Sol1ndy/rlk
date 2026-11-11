# KCUT pattern tick 3
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/yellow_tell {t:110}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/yellow_chime
