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
execute if score #buHpCol bu matches 1 run function rlk:bossui/run_hp {col:"#C58BFF"}
execute if score #buHpCol bu matches 2 run function rlk:bossui/run_hp {col:"#FF8A3D"}
execute if score #buHpCol bu matches 3 run function rlk:bossui/run_hp {col:"#4FB8FF"}
execute if score #buHpCol bu matches 4 run function rlk:bossui/run_hp {col:"#9FE8F5"}
execute if score #buHpCol bu matches 5 run function rlk:bossui/run_hp {col:"#F2C14E"}
execute if score #buHpCol bu matches 6 run function rlk:bossui/run_hp {col:"#6FE3C1"}
execute if score #buHpCol bu matches 7 run function rlk:bossui/run_hp {col:"#A5D94A"}
execute if score #buHpCol bu matches 8 run function rlk:bossui/run_hp {col:"#E8C35A"}
execute if score #buHpCol bu matches 9 run function rlk:bossui/run_hp {col:"#7BD88F"}
execute if score #buHpCol bu matches 10 run function rlk:bossui/run_hp {col:"#EDCF63"}
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
