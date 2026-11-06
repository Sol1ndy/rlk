# The counter cinematic (the judged deflect; @s = body): cine, invulnerable (only its scripted true damage passes), the
# sequence repel {at:60} after A8 (CS2) / {at:5} after A13 (CS3); its HP steps come through #sq_sig.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #ph hr 5
execute if score #gk hr matches 2 run scoreboard players set #ph hr 10
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
function rlk:mboss/cine/start
scoreboard players set #sqh hr 0
scoreboard players set #gres hr 0
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/core/seq/repel
