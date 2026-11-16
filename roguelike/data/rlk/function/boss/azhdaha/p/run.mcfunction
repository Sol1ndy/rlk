# @s = body. The main slot: start on the tick it was picked, then tick with #azPT = -lead+1 .. 0 (clip) .. ;
# during a front pattern's lead the body pre-turns <= 4 deg/t.
execute if score #azPNew mb matches 1 run return run function rlk:boss/azhdaha/p/begin
scoreboard players add #azPT mb 1
execute if score #azPT mb matches ..-1 run function rlk:mboss/mv/turn {max:4}
execute if score #azPT mb matches 0 run function rlk:boss/azhdaha/p/clip_d
function rlk:boss/azhdaha/p/tick_d
execute if score #azPEnd mb matches 1 run return run function rlk:boss/azhdaha/p/finish
execute if score #azPT mb >= #azPMax mb run function rlk:boss/azhdaha/p/finish
