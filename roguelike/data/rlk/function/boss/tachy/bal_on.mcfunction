# @s = body: the pattern goes (like the G3 backfire, no true damage), she drops to a knee - on the floor: a glide
# stopped mid-arc (the side-step hop of pattern 3) would leave the NoGravity body up to 0.6 b up (review B-08).
execute if score #pat tk matches 1..11 run function rlk:boss/tachy/core/cancel_pat
function rlk:boss/tachy/core/stop_move
function rlk:boss/tachy/core/ground
scoreboard players set #stag tk 100
function rlk:boss/tachy/rig/play/stun
execute at @s run function rlk:boss/tachy/fx/snd/stagger
function rlk:boss/tachy/hud/sub
