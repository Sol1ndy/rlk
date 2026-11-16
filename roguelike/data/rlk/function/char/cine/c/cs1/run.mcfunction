# cs1 (720 t; clip 2): show tick #cavT, held at 0 and at 720. From char/cine/tick.
scoreboard players operation #t cine = #cavT cine
execute unless score #t cine matches 0.. run scoreboard players set #t cine 0
execute if score #t cine matches 721.. run scoreboard players set #t cine 720
execute if score #cavR cine matches 0.. run function rlk:char/cine/c/cs1/rearm
scoreboard players set #cavR cine -1
scoreboard players operation #d cine = #t cine
scoreboard players operation #d cine -= #cavP cine
execute if score #d cine matches 0 run return 0
execute if score #d cine matches 1..20 run return run function rlk:char/cine/c/cs1/catch
function rlk:char/cine/c/cs1/seek
