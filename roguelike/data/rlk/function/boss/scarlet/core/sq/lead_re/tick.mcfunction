# Stand-in lead_re tick (#sq hr 1..60).
execute if score #sq hr matches 10 run function rlk:boss/scarlet/core/sq/lead_re/k/10
execute if score #sq hr matches 60.. run scoreboard players set #sqdone hr 1
