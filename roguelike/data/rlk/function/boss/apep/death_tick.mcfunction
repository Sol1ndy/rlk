# Hook death_tick (@s = body, #mbT 1.. until cur.death): seq/death (clock #apPT = #mbT - 1), the rig.
scoreboard players operation #apPT mb = #mbT mb
scoreboard players remove #apPT mb 1
function rlk:boss/apep/obj/tick
function rlk:boss/apep/seq/death/tick
function rlk:boss/apep/rig/tick
