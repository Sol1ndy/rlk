# Stand-in ending tick (#sq hr 1..1042).
execute if score #sq hr matches 300 run function rlk:mboss/music/set {ph:3}
execute if score #sq hr matches 1042.. run scoreboard players set #sqdone hr 1
