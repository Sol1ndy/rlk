# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# /reload in phase 2 (the module entities are gone): the Heart again, the walls cleared, the current wave
# again; progress, wave index, clocks and strikes kept.
function rlk:boss/apep/heart/make
function rlk:boss/apep/wall/clear
execute if score #apStage mb matches 1 if score #apWave mb matches 1.. run function rlk:boss/apep/rev/wave_spawn
scoreboard players set #apHudQ mb 1
