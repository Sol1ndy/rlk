# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# @s = body (phase 2, the module tick; the core stepped the Heart's and the walls' clips before it). The stage stops
# while a service (fail / CS) runs. Order: the clocks, the walls' clocks, the pending spawns, the organisms, the
# bolts, the Heart limits (CS / failure strike), the
# waves (every 8 t: due on <= 1 alive or the wave clock; a due wave waits for the cap), the
# time-out, the ambience.
execute if score #apPid mb matches 1.. run return 0
execute unless score #apStage mb matches 1 run return 0
scoreboard players add #apClk mb 1
scoreboard players add #apWT mb 1
scoreboard players operation #apClk2 mb = #apClk mb
scoreboard players operation #apClk2 mb %= #apK2 mb
scoreboard players operation #apClk8 mb = #apClk mb
scoreboard players operation #apClk8 mb %= #apK8 mb
scoreboard players operation #apClk40 mb = #apClk mb
scoreboard players operation #apClk40 mb %= #apK40 mb
function rlk:boss/apep/wall/tick
function rlk:boss/apep/org/pend_tick
function rlk:boss/apep/org/tick
function rlk:boss/apep/org/bolts
execute if score #apHt mb matches 10000.. run return run function rlk:boss/apep/svc/req_cs
execute if score #apHt mb matches ..0 run return run function rlk:boss/apep/svc/req_fail
execute if score #apClk8 mb matches 0 run function rlk:boss/apep/rev/wave_due
execute if score #apWave mb matches 0 unless score #apClk8 mb matches 0 run function rlk:boss/apep/rev/wave_due
execute if score #apClk mb matches 2000.. run function rlk:boss/apep/rev/timeout
execute if score #apClk mb matches 1.. if score #apClk40 mb matches 0 positioned 440 201 8 run function rlk:boss/apep/fx/p/gold_motes
scoreboard players operation #apM mb = #apClk mb
scoreboard players operation #apM mb %= #apK10 mb
execute if score #apM mb matches 0 positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_withered
