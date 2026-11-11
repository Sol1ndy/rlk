# ending: the timeline at #sq 286 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^6.8 ^2.5 run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^6.8 ^2.5 run function rlk:boss/scarlet/fx/snd/air_slash
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:3,out:6}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^6.8 ^2.5 run function rlk:boss/scarlet/fx/snd/air_white
