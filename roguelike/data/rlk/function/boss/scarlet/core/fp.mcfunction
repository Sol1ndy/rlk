# A fight-phase tick (P1 / P2; @s = body): the phase clock, AI samples, the triggers (A6, the counter, the flinch), then
# the running pattern or the recovery.
scoreboard players add #ai_pht hr 1
scoreboard players operation #t hr = #clk hr
scoreboard players operation #t hr %= #c5 hr
execute if score #t hr matches 0 run function rlk:boss/scarlet/ai/sample
execute if score #a6q hr matches 1 if function rlk:boss/scarlet/ai/a6 run return 0
execute if score #ctr hr matches 1 if score #pat hr matches 0 if function rlk:boss/scarlet/ai/counter run return 0
execute if score #flq hr matches 1 run function rlk:boss/scarlet/core/flinch
execute if score #pat hr matches 1.. run return run function rlk:boss/scarlet/core/pat_tick
execute if score #lock hr matches 1 run return 0
function rlk:boss/scarlet/ai/recover
