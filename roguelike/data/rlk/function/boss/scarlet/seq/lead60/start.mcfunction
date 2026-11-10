# lead60 (hr_design §3.3; after CS1): the gauge full, she straightens, the hand to the brim; G1 at its end. Not locked.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/rig/play/lead60
function rlk:boss/scarlet/fx/hud/warn {on:0}
scoreboard players set #sqdone hr 0
function rlk:boss/scarlet/fx/snd/shield_refill
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/shield_refill
