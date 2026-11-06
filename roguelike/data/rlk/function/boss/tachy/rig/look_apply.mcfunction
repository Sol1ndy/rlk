# Re-applies every stored look (spawn). @s = the boss.
execute if score @s tkRigForm matches 0 run function rlk:boss/tachy/rig/look/form/cape
execute if score @s tkRigForm matches 1 run function rlk:boss/tachy/rig/look/form/winged
execute if score @s tkRigForm matches 2 run function rlk:boss/tachy/rig/look/form/abyss
function rlk:boss/tachy/rig/lk/visor/restore
function rlk:boss/tachy/rig/lk/edge/restore
function rlk:boss/tachy/rig/lk/chest/restore
execute if score @s tkRigH matches 0 run function rlk:boss/tachy/rig/look/hands/open
execute if score @s tkRigH matches 1 run function rlk:boss/tachy/rig/look/hands/grip
execute if score @s tkRigH matches 2 run function rlk:boss/tachy/rig/look/hands/fist
