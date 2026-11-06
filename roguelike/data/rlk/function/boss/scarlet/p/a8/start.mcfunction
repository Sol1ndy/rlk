# A8 자영 연참 (the 60 % gauntlet; S4, p_ghost.py): pattern tick 0 (@s = the body, at it; clock #pt hr).
scoreboard players set #done hr 0
function rlk:boss/scarlet/rig/play/g_tell
function rlk:boss/scarlet/rig/look/form/ghost
tag @s add rlk_hr_ghost
execute at @s run function rlk:boss/scarlet/fx/snd/g_tell
