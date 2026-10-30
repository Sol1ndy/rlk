# End of a fight without forgetting cur/ret (won reads them afterwards).
execute if score #mbId mb matches 1.. run function rlk:mboss/d/cleanup
function rlk:mboss/cleanup_aux
function rlk:mboss/ar/sweep
function rlk:mboss/bars_hide
function rlk:mboss/line/clear
function rlk:mboss/music/stop
scoreboard players set #mbOn mb 0
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
scoreboard players set #mbPause mb 0
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #mbLive mb 0
function rlk:mboss/player_reset
data modify storage rlk:mboss sub set value []
data modify storage rlk:mboss extra set value []
# chapter mode (AZ-CM): per-fight chapter state; #mbAr keeps its value until the next fight_vars (cb/won reads it)
scoreboard players set #mbMode mb 0
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
scoreboard players set #mbCine mb 0
scoreboard players set #mbPushOn mb 0
scoreboard players set #mbPoolPct mb 100
scoreboard players set #mbRamp mb 0
scoreboard players set #mbHitEv mb 0
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
scoreboard players set #mbPart mb 0
scoreboard players set #mbPx mb 0
scoreboard players set #mbLost mb 0
scoreboard players set #cbWait mb 0
scoreboard players set #mbNoRx mb 0
scoreboard players reset #hzPmL mb
data remove storage rlk:mboss px
data remove storage rlk:mboss push
data remove storage rlk:mboss lv
