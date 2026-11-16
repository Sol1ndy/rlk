# coda (120 t; clip 5): show tick #cavT, held at 0 and at 120. From char/cine/tick.
scoreboard players operation #t cine = #cavT cine
execute unless score #t cine matches 0.. run scoreboard players set #t cine 0
execute if score #t cine matches 121.. run scoreboard players set #t cine 120
execute if score #cavR cine matches 0.. run function rlk:char/cine/c/coda/rearm
scoreboard players set #cavR cine -1
scoreboard players operation #d cine = #t cine
scoreboard players operation #d cine -= #cavP cine
execute if score #d cine matches 0 run return 0
execute if score #d cine matches 1..20 run return run function rlk:char/cine/c/coda/catch
function rlk:char/cine/c/coda/seek
