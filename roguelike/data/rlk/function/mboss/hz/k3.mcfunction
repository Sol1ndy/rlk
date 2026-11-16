# Sector angle test: angle(d, forward) <= a  <=>  fwd >= cos(a) |d|, squared without sqrt.
execute if score @s mbHzAng matches 180.. run return run function rlk:mboss/hz/hurt
scoreboard players operation #c mb = @s mbHzC
execute if score #c mb matches ..-1 run scoreboard players operation #c mb *= #cm1 mb
scoreboard players operation #q mb = #r2 mb
scoreboard players operation #q mb /= #c1000 mb
scoreboard players operation #q mb *= #c mb
scoreboard players operation #q mb /= #c1000 mb
scoreboard players operation #q mb *= #c mb
scoreboard players operation #f2 mb = #fwd mb
scoreboard players operation #f2 mb *= #fwd mb
execute if score @s mbHzC matches 0.. if score #fwd mb matches 0.. if score #f2 mb >= #q mb run return run function rlk:mboss/hz/hurt
execute if score @s mbHzC matches ..-1 if score #fwd mb matches 0.. run return run function rlk:mboss/hz/hurt
execute if score @s mbHzC matches ..-1 if score #fwd mb matches ..-1 if score #f2 mb <= #q mb run return run function rlk:mboss/hz/hurt
