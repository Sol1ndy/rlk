# ending: the timeline at #sq 70 (@s = the body).
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:1,out:2}
function rlk:boss/scarlet/fx/snd/bolt_crackle
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.5 ^2.1 run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.5 ^2.1 run function rlk:boss/scarlet/fx/p/clash_arc
