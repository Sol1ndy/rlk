# One fight tick (@s = body): module clock, G3 backfire, the floor, the G1 aura, AI samples, then the running state.
scoreboard players add #clk tk 1
scoreboard players add #ai_pht tk 1
execute if score #core tk matches 2 run function rlk:boss/tachy/el/backfire
execute unless score #mbSt mb matches 1 run return 0
execute if score #mbFloorHit mb matches 1 run function rlk:boss/tachy/core/floor_hit
scoreboard players add #aut tk 1
execute if score #aut tk matches 20.. run function rlk:boss/tachy/el/refresh
scoreboard players add #swt tk 1
scoreboard players operation #t tk = #clk tk
scoreboard players operation #t tk %= #c5 tk
execute if score #t tk matches 0 run function rlk:boss/tachy/ai/sample
execute if score #stag tk matches 1.. run return run function rlk:boss/tachy/core/stag_tick
execute if score #lock tk matches 1 if score #pat tk matches 0 run return 0
execute if score #pat tk matches 1..11 run return run function rlk:boss/tachy/core/pat_tick
execute if score #pat tk matches 50 run return run function rlk:boss/tachy/el/swap_tick
execute if score #pat tk matches 51 run return run function rlk:boss/tachy/mantle/tick
execute if score #pat tk matches 52 run return run function rlk:boss/tachy/mantle/break_tick
execute if score #pat tk matches 53 run return run function rlk:boss/tachy/mantle/nova_tick
execute if score #pat tk matches 54 run return run function rlk:boss/tachy/core/tr/tick
execute if score #pat tk matches 55 run return run function rlk:boss/tachy/core/replay/tick
function rlk:boss/tachy/ai/recover
