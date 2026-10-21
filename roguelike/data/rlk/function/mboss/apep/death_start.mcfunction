# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, set the proxies dead, stopped the
# music): the slot, domes, walls, organisms, the kit telegraphs and HUD; the cine; the death clip and seq/death.
function rlk:mboss/apep/p/cancel
function rlk:mboss/apep/dome/clear
function rlk:mboss/apep/wall/clear
function rlk:mboss/apep/org/clear
function rlk:mboss/apep/fx/tele/clear
function rlk:mboss/apep/fx/hud/clear
function rlk:mboss/apep/svc/cine_on
scoreboard players set #mbFloor mb 0
scoreboard players set #apTr mb 0
scoreboard players set #apPh mb 9
scoreboard players set #apPT mb 0
function rlk:mboss/apep/u/hide_off
function rlk:mboss/apep/play/death
function rlk:mboss/apep/seq/death/start
