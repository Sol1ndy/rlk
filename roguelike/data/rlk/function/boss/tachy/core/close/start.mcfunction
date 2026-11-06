# {q} = the queued chain (pattern id). The gap closer (@s = body): blink out (the blink_out clip, gold burst).
function rlk:boss/tachy/core/stop_move
scoreboard players set #pat tk 56
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
scoreboard players set #core tk 0
$scoreboard players set #cl_q tk $(q)
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/blink_out
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/blink_out
function rlk:boss/tachy/fx/snd/blink_out
function rlk:boss/tachy/hud/sub
