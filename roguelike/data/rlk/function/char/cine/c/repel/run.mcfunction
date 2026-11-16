# repel (140 t; clip 3): show tick #cavT, held at 0 and at 140. From char/cine/tick.
scoreboard players operation #t cine = #cavT cine
execute unless score #t cine matches 0.. run scoreboard players set #t cine 0
execute if score #t cine matches 141.. run scoreboard players set #t cine 140
execute if score #cavR cine matches 0.. run function rlk:char/cine/c/repel/rearm
scoreboard players set #cavR cine -1
scoreboard players operation #d cine = #t cine
scoreboard players operation #d cine -= #cavP cine
execute if score #d cine matches 0 run return 0
execute if score #d cine matches 1..20 run return run function rlk:char/cine/c/repel/catch
function rlk:char/cine/c/repel/seek
