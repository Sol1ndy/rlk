# @s = body: the pattern goes (like the G3 backfire, no true damage), she drops to a knee.
execute if score #pat tk matches 1..11 run function rlk:boss/tachy/core/cancel_pat
function rlk:boss/tachy/core/stop_move
scoreboard players set #stag tk 100
function rlk:boss/tachy/rig/play/stun
execute at @s run function rlk:boss/tachy/fx/snd/stagger
function rlk:boss/tachy/hud/sub
