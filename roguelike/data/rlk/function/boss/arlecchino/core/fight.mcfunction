# One fight tick (@s = body): the module clock, the floor, the bond (events of the last tick, the shock resolve),
# AI samples every 5 t, then the running state (hold, stun, pattern, transition, replay, recovery).
scoreboard players add #clk kn 1
scoreboard players add #ai_pht kn 1
execute unless score #mbSt mb matches 1 run return 0
execute if score #mbFloorHit mb matches 1 run function rlk:boss/arlecchino/core/floor_hit
execute if score #mbFloor mb matches 1.. run function rlk:boss/arlecchino/core/hp_floor
function rlk:boss/arlecchino/bond/tick
execute unless score #mbSt mb matches 1 run return 0
scoreboard players operation #t kn = #clk kn
scoreboard players operation #t kn %= #c5 kn
execute if score #t kn matches 0 run function rlk:boss/arlecchino/ai/sample
execute if score #pat kn matches 50 run return run function rlk:boss/arlecchino/core/stun_tick
execute if score #pat kn matches 51 run return run function rlk:boss/arlecchino/core/tr/tick
execute if score #pat kn matches 52 run return run function rlk:boss/arlecchino/core/replay/tick
execute if score #pat kn matches 1..49 run return run function rlk:boss/arlecchino/core/pat_tick
execute if score #lock kn matches 1 run return 0
function rlk:boss/arlecchino/ai/recover
