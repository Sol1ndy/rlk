# One tick of a kept tail's move (@s = body; the caller turned her to the player): one step (ai/step,
# mv/ok-checked); the move clock stamp.
function rlk:boss/scarlet/ai/step
scoreboard players operation #ai_tmc hr = #clk hr
