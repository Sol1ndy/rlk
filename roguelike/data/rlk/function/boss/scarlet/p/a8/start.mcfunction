# A8 자영 연참 (the 60 % gauntlet; S4, p_ghost.py): pattern tick 0 (@s = the body, at it; clock #pt hr).
scoreboard players set #done hr 0
function rlk:boss/scarlet/rig/play/g_tell
function rlk:boss/scarlet/rig/look/form/ghost
tag @s add rlk_hr_ghost
execute at @s run playsound minecraft:entity.illusioner.prepare_mirror hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
execute at @s run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
