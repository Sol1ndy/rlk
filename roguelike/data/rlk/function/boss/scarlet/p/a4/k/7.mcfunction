# A4 pattern tick 7
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/a4_glint
