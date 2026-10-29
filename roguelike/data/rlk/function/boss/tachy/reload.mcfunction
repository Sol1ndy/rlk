# Hook reload (@s = body after /reload: the rig parts, hazards, markers and kit cards are gone; scores are kept).
# intro -> its end; a pattern -> cancelled + recovery; a swap -> finished; a mantle -> gauge and time kept;
# a break / stun goes on; a nova -> the transition; a transition -> finished; the intro replay -> ended.
function rlk:boss/tachy/init
function rlk:boss/tachy/rig_stub/init
function rlk:boss/tachy/rig_stub/spawn
scoreboard players set #lock tk 0
execute if score #ph tk matches 0 run return run function rlk:boss/tachy/core/intro/reload
execute if score #ph tk matches 8 run return 0
execute if score #pat tk matches 1..11 run function rlk:boss/tachy/core/cancel_pat
execute if score #pat tk matches 50 run function rlk:boss/tachy/el/swap_end
execute if score #pat tk matches 51..53 run function rlk:boss/tachy/mantle/reload
execute if score #pat tk matches 54 run function rlk:boss/tachy/core/tr/end
execute if score #pat tk matches 55 run function rlk:boss/tachy/core/replay/end
execute if score #stag tk matches 1.. run function rlk:boss/tachy/rig_stub/play/stagger
function rlk:boss/tachy/core/looks
execute unless entity @s[tag=rlk_tk_mantle] run function rlk:boss/tachy/el/badge
function rlk:boss/tachy/hud/sub
execute if score #pat tk matches 0 if score #stag tk matches 0 run function rlk:boss/tachy/ai/rec_start
