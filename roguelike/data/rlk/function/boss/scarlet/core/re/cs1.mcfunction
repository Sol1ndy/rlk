# /reload or a pause in CS1: its end state (crimson, phase p2, music 2, the bars shown) = lead60 from tick 0.
function rlk:boss/scarlet/seq/cs1/cancel
scoreboard players set #sqn hr 0
function rlk:boss/scarlet/rig/look/phase/p2
scoreboard players set #hrLook hr 2
execute unless score #mbMusPh mb matches 2 run function rlk:mboss/music/set {ph:2}
function rlk:boss/scarlet/core/lead60/start
scoreboard players set #sq hr -1
