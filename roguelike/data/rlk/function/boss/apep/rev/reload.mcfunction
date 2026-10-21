# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# /reload in phase 2 (every rlk_mb_aux entity is gone): the Heart in the cradle again, the stage markers, the walls
# cleared (the recorded blocks lost their markers: the safety sweep), the current wave marked again; the progress,
# the wave index, the clocks and the strikes kept (the core re-made the dressing).
function rlk:boss/apep/heart/play_state
function rlk:boss/apep/org/marks
function rlk:boss/apep/wall/clear
function rlk:boss/apep/org/consts
scoreboard players set #apSlots mb 0
execute if score #apStage mb matches 1 if score #apWave mb matches 1.. run function rlk:boss/apep/rev/wave_marks
scoreboard players set #apHudQ mb 1
