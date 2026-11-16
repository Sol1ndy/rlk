# Hook reload (@s = body after /reload: the rig parts, hazards, markers, orbs and kit cards are gone; scores are kept).
# intro -> its end; a pattern -> cancelled + recovery (E70 before its brand: reserved again); T -> finished; the
# intro replay -> ended; a stun -> the rest of it (the clip again).
function rlk:boss/arlecchino/init
function rlk:boss/arlecchino/rig/init
function rlk:boss/arlecchino/rig/spawn
scoreboard players set #lock kn 0
execute if score #ph kn matches 0 run return run function rlk:boss/arlecchino/core/intro/reload
execute if score #ph kn matches 6 run return 0
execute if score #pat kn matches 1..49 run function rlk:boss/arlecchino/core/cancel_pat
execute if score #pat kn matches 51 run function rlk:boss/arlecchino/core/tr/end
execute if score #pat kn matches 52 run function rlk:boss/arlecchino/core/replay/end
function rlk:boss/arlecchino/core/looks
function rlk:boss/arlecchino/core/wisps
execute if score #stun kn matches 1 run function rlk:boss/arlecchino/core/stun_clip
function rlk:boss/arlecchino/hud/sub
execute if score #pat kn matches 0 run function rlk:boss/arlecchino/ai/rec_start
