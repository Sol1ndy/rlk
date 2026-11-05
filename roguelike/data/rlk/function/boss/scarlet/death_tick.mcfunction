# Hook death_tick (@s = body, #mbT 1.. until cur.death = H + 122): the ending on #sq; at its end (#sqdone, H) the event
# coda seq/event starts in the same tick (PLAN §7.1.2).
scoreboard players add #sq hr 1
execute if score #sqn hr matches 7 run function rlk:boss/scarlet/core/sq/ending/tick
execute if score #sqn hr matches 8 run function rlk:boss/scarlet/core/sq/event/tick
execute if score #sq_sig hr matches 1.. run scoreboard players set #sq_sig hr 0
execute if score #sqn hr matches 7 if score #sqdone hr matches 1 run function rlk:boss/scarlet/core/seq/event
function rlk:boss/scarlet/core/look
function rlk:boss/scarlet/rig_stub/tick
