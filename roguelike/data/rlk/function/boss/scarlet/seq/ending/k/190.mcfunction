# ending: the timeline at #sq 190 (@s = the body).
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:6,out:6}
function rlk:boss/scarlet/fx/snd/clash_big
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.5 ^3.25 run function rlk:boss/scarlet/fx/p/clash_gold
