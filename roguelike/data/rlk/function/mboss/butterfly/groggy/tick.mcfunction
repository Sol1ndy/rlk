scoreboard players add #bfT mb 1
# still debuffed after 달빛 해제: one new 달빛 이슬 during the groggy
execute if score #bfT mb matches 20 if score #bfCoc mb matches 1 run function rlk:mboss/butterfly/dew/spawn1
scoreboard players operation #bfM mb = #bfT mb
scoreboard players operation #bfM mb %= #bfK10 mb
execute if score #bfM mb matches 0 run function rlk:mboss/butterfly/fx/groggy
scoreboard players operation #bfM mb = #bfT mb
scoreboard players operation #bfM mb %= #bfK40 mb
execute if score #bfM mb matches 0 positioned ~ ~1.6 ~ run function rlk:mboss/butterfly/fx/p/motes
execute if score #bfT mb matches 300.. run function rlk:mboss/butterfly/recover/begin
