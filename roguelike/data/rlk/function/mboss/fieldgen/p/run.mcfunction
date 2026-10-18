# @s = body. The slot: start on the tick it was picked, then tick with #fgPT = 1, 2, ... (= clip tick).
execute if score #fgPNew mb matches 1 run return run function rlk:mboss/fieldgen/p/begin
scoreboard players add #fgPT mb 1
execute if score #fgPT mb matches 0 run function rlk:mboss/fieldgen/p/clip_d
function rlk:mboss/fieldgen/p/tick
# the service patterns (20 field opening, 22 pack-up) carry core mechanics on their clocks
execute if score #fgPat mb matches 20.. run function rlk:mboss/fieldgen/p/svc
execute if score #fgPEnd mb matches 1 run return run function rlk:mboss/fieldgen/p/finish
execute if score #fgPT mb >= #fgPMax mb run function rlk:mboss/fieldgen/p/finish
