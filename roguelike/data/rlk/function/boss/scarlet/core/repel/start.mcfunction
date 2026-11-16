# The repel counter (the judge with the gauge at 0; @s = body): cine (her hits refused, no balance damage), invulnerable
# (only its scripted true damage passes), the boss bars stay on; the sequence repel {at:60} after G1 / {at:5} after G2;
# its HP steps come through #sq_sig.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #ph hr 5
execute if score #gk hr matches 2 run scoreboard players set #ph hr 10
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
function rlk:mboss/cine/start
scoreboard players set #sqh hr 0
scoreboard players set #gres hr 0
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
function rlk:boss/scarlet/core/seq/repel
