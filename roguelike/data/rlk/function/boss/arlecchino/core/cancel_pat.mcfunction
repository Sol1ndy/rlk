# Cancel the running pattern (reload, tests; @s = body): recovery follows; E70 is reserved again.
execute if score #pat kn matches 20 run function rlk:boss/arlecchino/core/e70_reload
function rlk:boss/arlecchino/core/cancel_d
function rlk:boss/arlecchino/core/win_off
scoreboard players set #pat kn 0
scoreboard players set #done kn 0
function rlk:boss/arlecchino/core/stop_move
function rlk:boss/arlecchino/core/looks_rest
function rlk:boss/arlecchino/core/ground
function rlk:boss/arlecchino/ai/rec_start
function rlk:boss/arlecchino/hud/sub
