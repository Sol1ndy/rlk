# A pattern's kept tail starts to move (@s = body; p1 tail(), R1 / R3 at the solid row, R2 after its last release):
# the recovery's move and clip (ai/move_pick on core/fp's last sample, <= 4 t old: walk / P2 glide in beyond 6 b,
# else a strafe; no extra sample, so the rear / far dwell counts stay as they are); the move clock stamp.
function rlk:boss/scarlet/ai/move_pick
scoreboard players operation #ai_tmc hr = #clk hr
