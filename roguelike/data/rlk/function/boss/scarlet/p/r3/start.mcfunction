# R3 자영 활강 (P2: the ghost glide, the gauntlets' second block without shield or darkness; S4, p_ghost.py): pattern tick 0 (@s = the body, at it; clock #pt hr).
scoreboard players set #done hr 0
function rlk:boss/scarlet/rig_stub/play/g_tell
function rlk:boss/scarlet/rig_stub/look/form/ghost
tag @s add rlk_hr_ghost
execute at @s run playsound minecraft:entity.illusioner.prepare_mirror hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
execute at @s run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
