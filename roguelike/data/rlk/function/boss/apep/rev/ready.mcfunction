# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# Phase 2 ready (the test jumps through ph/ready_2): the Heart in the full cradle, the stage markers, the
# dressing (the gold swirl, the ley lines), progress 2700 (the stage clocks start in rev/start).
function rlk:boss/apep/heart/play_state
function rlk:boss/apep/org/marks
execute positioned 440 201 8 run function rlk:boss/apep/fx/dress/swirl {r:35}
execute positioned 440 201 8 run function rlk:boss/apep/fx/dress/ley {n:7}
scoreboard players set #apHt mb 2700
scoreboard players set #apHudQ mb 1
