# Stand-in cs1 tick (#sq hr 1..213).
execute if score #sq hr matches 173 run function rlk:boss/scarlet/rig_stub/look/phase/p2
execute if score #sq hr matches 179 unless score #mbMusPh mb matches 2 run function rlk:mboss/music/set {ph:2}
execute if score #sq hr matches 213.. run scoreboard players set #sqdone hr 1
