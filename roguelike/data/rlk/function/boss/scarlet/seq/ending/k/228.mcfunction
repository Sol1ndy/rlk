# ending: the timeline at #sq 228 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.45 ^3.5 run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.45 ^3.5 run function rlk:boss/scarlet/fx/p/clash_spark
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.45 ^3.5 run function rlk:boss/scarlet/fx/p/clash_arc
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.45 ^3.5 run function rlk:boss/scarlet/fx/snd/air_slash
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:1,out:2}
