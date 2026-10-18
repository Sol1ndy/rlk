# @s = a live front (from tick, before hz/all): radius 2.5 + 0.55 k b at its k-th active tick (this tick's hit
# test), inner radius r - 2.5 (tenths: r = 25 + 11 k / 2).
scoreboard players operation #hzSzR mb = @s mbHzT
scoreboard players operation #hzSzR mb -= @s mbHzW
scoreboard players add #hzSzR mb 1
execute if score #hzSzR mb matches ..0 run return 0
execute if score #hzSzR mb matches 37.. run return 0
scoreboard players operation #hzSzR mb *= #fgK11 mb
scoreboard players operation #hzSzR mb /= #c2 mb
scoreboard players add #hzSzR mb 25
scoreboard players operation #hzSzR0 mb = #hzSzR mb
scoreboard players remove #hzSzR0 mb 25
scoreboard players set #hzSzW mb 0
function rlk:mboss/hz/resize_s
scoreboard players operation #fgM mb = @s mbHzT
scoreboard players operation #fgM mb %= #fgK2 mb
execute if score #fgM mb matches 0 at @s run function rlk:mboss/fieldgen/p/waves/draw
