# @s = body. The main slot: start on the tick it was picked, then tick with #apPT = -lead+1 .. 0 (clip) .. ;
# during a lead the body pre-turns <= 6 deg/t (phase 1: 3).
execute if score #apPNew mb matches 1 run return run function rlk:boss/apep/p/begin
scoreboard players add #apPT mb 1
execute if score #apPT mb matches ..-1 if score #apPh mb matches 1 run function rlk:mboss/mv/turn {max:3}
execute if score #apPT mb matches ..-1 if score #apPh mb matches 3 run function rlk:mboss/mv/turn {max:6}
execute if score #apPT mb matches 0 run function rlk:boss/apep/p/clip_d
function rlk:boss/apep/p/tick_d
execute if score #apPEnd mb matches 1 run return run function rlk:boss/apep/p/finish
execute if score #apPT mb >= #apPMax mb run function rlk:boss/apep/p/finish
