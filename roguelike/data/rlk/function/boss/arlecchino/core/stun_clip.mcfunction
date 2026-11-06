# The stun clip of the form (@s = body).
execute if score #ph kn matches 5 run return run function rlk:boss/arlecchino/rig/play/stun2
function rlk:boss/arlecchino/rig/play/stun
execute at @s run function rlk:boss/arlecchino/fx/snd/stun
