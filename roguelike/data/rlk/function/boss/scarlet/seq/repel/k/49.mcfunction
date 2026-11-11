# repel: the timeline at #sq 49 (@s = the body).
function rlk:boss/scarlet/rig/anchor/hat_crown
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/clash_gold
scoreboard players set #sq_sig hr 1
function rlk:boss/scarlet/fx/snd/hat_clash
