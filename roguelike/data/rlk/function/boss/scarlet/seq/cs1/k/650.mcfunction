# cs1: the timeline at #sq 650 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^-0.36 ^1.495 ^2.94 facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.3 ^0 run function rlk:boss/scarlet/fx/p/scarlet_line {len:600,yaw:90,roll:13}
function rlk:boss/scarlet/fx/hud/ovl {g:"red_tint",in:0,hold:4,out:20}
function rlk:boss/scarlet/fx/snd/iai_slash
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/petal_burst {r:20}
