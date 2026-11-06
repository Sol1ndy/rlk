# /reload in CS1: its end state = SQ1 tick 0 (crimson, phase p2, music 2, the bars shown).
function rlk:boss/scarlet/seq/cs1/cancel
scoreboard players set #sqn hr 0
execute unless score #mbMusPh mb matches 2 run function rlk:mboss/music/set {ph:2}
function rlk:boss/scarlet/core/sq1/start
scoreboard players set #sq hr -1
