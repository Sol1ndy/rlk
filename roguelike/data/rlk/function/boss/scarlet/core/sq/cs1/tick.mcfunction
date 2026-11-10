# Stand-in cs1 tick (#sq hr 1..720).
execute if score #sq hr matches 660 run function rlk:boss/scarlet/core/sq/cs1/k/660
execute if score #sq hr matches 676 unless score #mbMusPh mb matches 2 run function rlk:mboss/music/set {ph:2}
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
