# G2 mantle tick (#pat 51): hold clip, timers, aura alternation every 60 t (in sync with the veins),
# a feather every 36 t (S4 p/mantle/feather), the gauge HUD; break at 0, failure at the time limit.
scoreboard players add #pt tk 1
execute if score #pt tk matches 24 run function rlk:boss/tachy/rig_stub/play/mantle_hold
execute if score #shicd tk matches 1.. run scoreboard players remove #shicd tk 1
scoreboard players remove #sht tk 1
scoreboard players operation #t tk = #pt tk
scoreboard players operation #t tk %= #c60 tk
execute if score #t tk matches 0 run function rlk:boss/tachy/el/flip
execute unless score #sh tk = #hud_g tk run function rlk:boss/tachy/mantle/gauge
execute if score #sh tk matches ..0 run return run function rlk:boss/tachy/mantle/break
execute if score #sht tk matches ..0 run return run function rlk:boss/tachy/mantle/fail
