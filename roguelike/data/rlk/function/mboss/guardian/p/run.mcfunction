# @s = body. The slot: start on the tick it was picked, then tick with #gdPT = 1, 2, ... (= clip tick).
execute if score #gdPNew mb matches 1 run return run function rlk:mboss/guardian/p/begin
scoreboard players add #gdPT mb 1
function rlk:mboss/guardian/p/tick
execute if score #gdPEnd mb matches 1 run return run function rlk:mboss/guardian/p/finish
execute if score #gdPT mb >= #gdPMax mb run function rlk:mboss/guardian/p/finish
