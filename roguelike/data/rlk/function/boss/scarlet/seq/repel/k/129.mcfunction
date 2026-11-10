# repel: the timeline at #sq 129 (@s = the body).
function rlk:boss/scarlet/fx/keep_on
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/kick_flash
function rlk:boss/scarlet/fx/keep_off
function rlk:boss/scarlet/fx/snd/kick
execute if score #sq_at hr matches 60 run function rlk:boss/scarlet/seq/repel/m/slide
scoreboard players set #sq_sig hr 3
