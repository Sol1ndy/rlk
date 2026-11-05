# A8 pattern tick 174.
function rlk:boss/scarlet/rig/look/blade/off
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=174},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/p/qi_vert {h:34,yaw:0,c:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=174},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_vert
