# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, stopped the music): every state
# stops, the kit cards go, the death sequence (seq/death or the clip) on #sq; the special win path follows.
function rlk:boss/tachy/core/stop_all
scoreboard players set #mbFloor mb 0
scoreboard players set #ph tk 8
scoreboard players set #sq tk 0
scoreboard players set #sqdone tk 0
function rlk:boss/tachy/core/stop_move
function rlk:boss/tachy/core/sq/death/start
