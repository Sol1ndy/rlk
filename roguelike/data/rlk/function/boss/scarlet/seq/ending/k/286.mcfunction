# ending: the timeline at #sq 286 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.25 ^3.55 run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.25 ^3.55 run function rlk:boss/scarlet/fx/p/clash_spark
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.25 ^3.55 run function rlk:boss/scarlet/fx/p/clash_arc
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:3,out:6}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.25 ^3.55 run function rlk:boss/scarlet/fx/snd/air_white
