# Hook death_start (@s = body; the lethal hit: the framework cleared its libraries, hid the bars, stopped the music):
# every fight state stops, the kit cards go, cine off, the event roll (PLAN §7.3.1), the ending CS4 (seq/ending).
function rlk:boss/scarlet/core/stop_all
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/fx/clear
function rlk:boss/scarlet/fx/hud/warn {on:0}
function rlk:mboss/cine/end
scoreboard players set #mbFloor mb 0
scoreboard players set #ph hr 11
scoreboard players set #hud hr 0
function rlk:boss/scarlet/ev/roll
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
function rlk:boss/scarlet/core/seq/ending
