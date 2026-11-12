# lead_re {g:"a8"|"a13"} (hr_design §3.3; a restart after a pause / the revive): she stands 8 b away, the refill (+ the banner), the hand to the brim; the gauntlet g at its end. Not locked.
# Start (@s = the body, at it; #sq hr = 0) — macro.
scoreboard players set #sq_g hr 0
$data modify storage rlk:hr seq.g set value "$(g)"
execute if data storage rlk:hr seq{g:"a8"} run function rlk:boss/scarlet/seq/lead_re/g/a8
execute if data storage rlk:hr seq{g:"a13"} run function rlk:boss/scarlet/seq/lead_re/g/a13
function rlk:boss/scarlet/rig/play/lead_re
function rlk:boss/scarlet/fx/hud/warn {on:0}
scoreboard players set #sqdone hr 0
function rlk:boss/scarlet/seq/lead_re/m/place
