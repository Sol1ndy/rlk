# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The stage again: 2700, wave 1, the clocks and the time-out reset; the Heart back to its idle look.
scoreboard players set #apHt mb 2700
function rlk:boss/apep/rev/start
execute if entity 524c4b4d-4150-4800-8000-000000000000 run function rlk:boss/apep/om/heart/look/heart_bulb/idle
execute if entity 524c4b4d-4150-4800-8000-000000000000 run function rlk:boss/apep/om/heart/play/heart_idle
function rlk:boss/apep/p/end
