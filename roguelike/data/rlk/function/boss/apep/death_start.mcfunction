# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, set the proxies dead, stopped the
# music): the slot, domes, walls, organisms, the kit telegraphs and HUD; the cine; the death clip and seq/death.
function rlk:boss/apep/p/cancel
function rlk:boss/apep/dome/clear
function rlk:boss/apep/wall/clear
function rlk:boss/apep/org/clear
function rlk:boss/apep/fx/tele/clear
function rlk:boss/apep/fx/hud/clear
function rlk:boss/apep/svc/cine_on
scoreboard players set #mbFloor mb 0
scoreboard players set #apTr mb 0
scoreboard players set #apPh mb 9
scoreboard players set #apPT mb 0
function rlk:boss/apep/u/hide_off
function rlk:boss/apep/play/death
function rlk:boss/apep/seq/death/start
