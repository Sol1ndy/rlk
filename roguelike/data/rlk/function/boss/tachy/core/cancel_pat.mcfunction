# Cancel the running pattern (G3 backfire, reload, tests; @s = body): recovery follows.
function rlk:boss/tachy/core/cancel_d
tag @s remove rlk_tk_core
scoreboard players set #pat tk 0
scoreboard players set #done tk 0
function rlk:boss/tachy/core/stop_move
function rlk:boss/tachy/el/edge
function rlk:boss/tachy/rig/look/chest/off
function rlk:boss/tachy/ai/rec_start
