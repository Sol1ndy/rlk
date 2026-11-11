# The lead_re {g:"a13"} (a G2 restart) -> A13 (@s = body): invulnerable to the ending (G2) / the repel (G1), no balance damage; the gauge
# is refilled at the sequence's refill beat (#sq_sig refill -> shield/arm); the warning banner belongs to the sequence
# (when #warn: the gauntlet's fail is lethal).
function rlk:boss/scarlet/core/cancel_d
kill @e[tag=rlk_hr_p]
scoreboard players set #pat hr 0
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
scoreboard players set #ph hr 8
scoreboard players set #gk hr 2
scoreboard players set #fl hr 0
scoreboard players set #rvw hr 0
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
scoreboard players set #mbBalOff mb 1
function rlk:mboss/cine/end
function rlk:boss/scarlet/shield/off
scoreboard players set #warn hr 1
function rlk:boss/scarlet/core/seq/lead_re_a13
