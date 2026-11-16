# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The stage gone (cleanup, the phase jumps): the Heart, the stage markers, the pending spawns, the dressing, the
# stage scores.
function rlk:boss/apep/heart/clear
function rlk:boss/apep/org/marks_kill
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]
function rlk:boss/apep/fx/dress/clear
scoreboard players set #apHt mb 0
scoreboard players set #apWave mb 0
scoreboard players set #apClk mb 0
scoreboard players set #apWT mb 0
scoreboard players set #apTo mb 0
scoreboard players set #apToT mb 0
scoreboard players set #apFail mb 0
scoreboard players set #apStage mb 0
scoreboard players set #apAlive mb 0
scoreboard players set #apSlots mb 0
scoreboard players set #apOArg mb 0
scoreboard players set #apOrgN mb 0
scoreboard players set #apHtP mb 0
scoreboard players set #apWid mb 0
scoreboard players set #apBg0 mb 0
scoreboard players set #apBg1 mb 0
scoreboard players set #apBg2 mb 0
scoreboard players set #apBg3 mb 0
scoreboard players set #apDNear mb 0
scoreboard players set #apPChain mb 0
scoreboard players set #apClk2 mb 0
scoreboard players set #apClk8 mb 0
scoreboard players set #apClk40 mb 0
scoreboard players set #apq40L mb 0
