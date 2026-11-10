# The lead_re {g:"a8"} (an A8 restart) -> A8 (@s = body): invulnerable to CS4 (A13) / CS2 (A8); the shield off until the refill beat
# (#sq_sig refill -> shield/arm); the warning banner belongs to the sequence (when #warn: the gauntlet's fail is lethal).
function rlk:boss/scarlet/core/cancel_d
kill @e[tag=rlk_hr_p]
scoreboard players set #pat hr 0
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
scoreboard players set #ph hr 8
scoreboard players set #gk hr 1
scoreboard players set #fl hr 0
scoreboard players set #flw hr 0
scoreboard players set #rvw hr 0
scoreboard players set #kip hr 0
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
function rlk:boss/scarlet/shield/off
function rlk:mboss/cine/end
scoreboard players set #warn hr 0
function rlk:boss/scarlet/core/seq/lead_re_a8
