# Hook intro_tick (@s = body, #mbT 1..; untargetable): E (entrance_p1, 110 t; clock #apPT = #mbT - 1).
scoreboard players operation #apPT mb = #mbT mb
scoreboard players remove #apPT mb 1
function rlk:boss/apep/seq/entrance/tick
function rlk:boss/apep/hud/tick
function rlk:boss/apep/rig/tick
function rlk:boss/apep/pxs/tick
execute if score #mbT mb matches 110.. run function rlk:boss/apep/intro/done
