# repel at #sq 102 (@s = the body).
function rlk:boss/scarlet/fx/keep_on
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/kick_flash
function rlk:boss/scarlet/fx/keep_off
scoreboard players set #sq_sig hr 3
function rlk:boss/scarlet/fx/snd/kick
