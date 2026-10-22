# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The stage (re)starts from wave 1 (the test jumps, a failure restart): the clocks and the time-out reset; the
# first wave is due now (its spawn markers, then the organisms 20 t later).
scoreboard players set #apWave mb 0
scoreboard players set #apWT mb 600
function rlk:boss/apep/org/consts
scoreboard players set #apClk mb 0
scoreboard players set #apTo mb 0
scoreboard players set #apToT mb 0
scoreboard players set #apStage mb 1
scoreboard players set #apSlots mb 0
scoreboard players set #apBg0 mb 0
scoreboard players set #apBg1 mb 0
scoreboard players set #apBg2 mb 0
scoreboard players set #apBg3 mb 0
scoreboard players set #apHudQ mb 1
