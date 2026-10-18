# End of a fight without forgetting cur/ret (won reads them afterwards).
execute if score #mbId mb matches 1.. run function rlk:mboss/d/cleanup
function rlk:mboss/cleanup_aux
function rlk:mboss/arena_sweep
function rlk:mboss/bars_hide
function rlk:mboss/line/clear
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
