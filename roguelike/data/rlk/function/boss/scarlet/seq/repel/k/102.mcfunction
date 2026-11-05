# repel at #sq 102 (@s = the body).
function rlk:boss/scarlet/rig/anchor/head
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/kick_flash
scoreboard players set #sq_sig hr 3
function rlk:boss/scarlet/fx/snd/kick
