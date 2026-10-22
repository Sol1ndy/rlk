# @s = body. The slot: start on the tick it was picked, then tick with #bfPT = 1, 2, ... (= clip tick).
execute if score #bfPNew mb matches 1 run return run function rlk:mboss/butterfly/p/begin
scoreboard players add #bfPT mb 1
execute if score #bfPT mb matches 0 run function rlk:mboss/butterfly/p/clip_d
function rlk:mboss/butterfly/p/tick
# the service patterns (15 달빛 해제, 20 transformation) carry core mechanics on their clocks
execute if score #bfPat mb matches 15.. run function rlk:mboss/butterfly/p/svc
execute if score #bfPEnd mb matches 1 run return run function rlk:mboss/butterfly/p/finish
execute if score #bfPT mb >= #bfPMax mb run function rlk:mboss/butterfly/p/finish
