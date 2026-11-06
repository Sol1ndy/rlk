# As the boss, with #buHp #buMax #buSub #buSubMax #buSubCol set: line -> storage rlk:bu line.
execute if score #buMax bu matches ..0 run scoreboard players set #buMax bu 1
execute if score #buHp bu matches ..-1 run scoreboard players set #buHp bu 0
function rlk:bossui/trail
data modify storage rlk:bu line set value []
scoreboard players operation #fill bu = #buHp bu
scoreboard players operation #fill bu *= #bar bu
scoreboard players operation #fill bu /= #buMax bu
execute if score #buHp bu matches 1.. if score #fill bu matches ..0 run scoreboard players set #fill bu 1
scoreboard players operation #tr bu = @s buTrail
scoreboard players operation #tr bu *= #bar bu
scoreboard players operation #tr bu /= #buMax bu
execute if score #tr bu < #fill bu run scoreboard players operation #tr bu = #fill bu
scoreboard players operation #white bu = #tr bu
scoreboard players operation #white bu -= #fill bu
scoreboard players operation #empty bu = #bar bu
scoreboard players operation #empty bu -= #tr bu
execute if score #empty bu matches ..-1 run scoreboard players set #empty bu 0
scoreboard players operation #len bu = #fill bu
execute unless score #buHpCol bu matches 1..10 run function rlk:bossui/run_hp {col:"#E0484B"}
# #buHpCol 1..10: the coloured HP run (bossui/hp_col; a caller without the option pays this one test)
execute if score #buHpCol bu matches 1..10 run function rlk:bossui/hp_col
scoreboard players operation #len bu = #white bu
function rlk:bossui/run_hp {col:"#FFFFFF"}
scoreboard players operation #len bu = #empty bu
function rlk:bossui/run_hp {col:"#2A2A2E"}
# Numbers "hp/max" centred on the bar (#buNoNum 1: none; the cursor already stands at the bar end).
execute unless score #buNoNum bu matches 1.. run function rlk:bossui/nums
# Under bar (shield in its element colour, or a gauge).
execute if score #buSubCol bu matches 1.. if score #buSubMax bu matches 1.. run function rlk:bossui/sub
# The options hold for this draw only.
scoreboard players set #buHpCol bu 0
scoreboard players set #buNoNum bu 0
