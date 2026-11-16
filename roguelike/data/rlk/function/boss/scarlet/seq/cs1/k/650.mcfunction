# cs1: the timeline at #sq 650 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.15 ^0.857 ^1.06 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.934 ^0.722 ^1.186 run tp @s ~ ~ ~
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.3 ^0 run function rlk:boss/scarlet/fx/p/scarlet_line {len:600,yaw:90,roll:13}
function rlk:boss/scarlet/fx/hud/ovl {g:"red_tint",in:0,hold:4,out:20}
function rlk:boss/scarlet/fx/snd/iai_slash
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/petal_burst {r:20}
