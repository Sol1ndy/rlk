# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, stopped the music): every state
# stops, the kit cards go, her bond is taken back, the death sequence (seq/death or the stand-in) on #sq.
function rlk:boss/arlecchino/core/stop_all
function rlk:boss/arlecchino/bond/cleanup
scoreboard players set #mbFloor mb 0
scoreboard players set #ph kn 6
scoreboard players set #sq kn 0
scoreboard players set #sqdone kn 0
function rlk:boss/arlecchino/core/stop_move
function rlk:boss/arlecchino/core/ground
function rlk:boss/arlecchino/core/sq/death/start
