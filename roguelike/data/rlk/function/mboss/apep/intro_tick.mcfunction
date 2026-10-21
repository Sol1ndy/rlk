# Hook intro_tick (@s = body, #mbT 1..; untargetable): E (entrance_p1, 110 t; clock #apPT = #mbT - 1).
scoreboard players operation #apPT mb = #mbT mb
scoreboard players remove #apPT mb 1
function rlk:mboss/apep/seq/entrance/tick
function rlk:mboss/apep/hud/tick
function rlk:mboss/apep/rig_stub/tick
function rlk:mboss/apep/pxs/tick
execute if score #mbT mb matches 110.. run function rlk:mboss/apep/intro/done
