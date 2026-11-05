# R3 pattern tick 37.
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=37},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/qi_x {r:25}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=37},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_x
function rlk:boss/scarlet/rig/play/g_reform
