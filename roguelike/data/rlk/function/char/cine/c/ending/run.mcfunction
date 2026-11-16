# ending (1372 t; clip 4): show tick #cavT, held at 0 and at 1372. From char/cine/tick.
scoreboard players operation #t cine = #cavT cine
execute unless score #t cine matches 0.. run scoreboard players set #t cine 0
execute if score #t cine matches 1373.. run scoreboard players set #t cine 1372
execute if score #cavR cine matches 0.. run function rlk:char/cine/c/ending/rearm
scoreboard players set #cavR cine -1
scoreboard players operation #d cine = #t cine
scoreboard players operation #d cine -= #cavP cine
execute if score #d cine matches 0 run return 0
execute if score #d cine matches 1..20 run return run function rlk:char/cine/c/ending/catch
function rlk:char/cine/c/ending/seek
